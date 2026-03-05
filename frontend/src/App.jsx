import { useState, useEffect } from 'react'
import { Input, Button, Card, Spin, Typography, message, Layout, Tabs, Form, Table, Tag, Space, Modal, Popconfirm, Descriptions, Tooltip, Badge, Divider, Empty } from 'antd'
import { ExportOutlined, HistoryOutlined, MoonOutlined, SunOutlined, EyeOutlined, EditOutlined, DeleteOutlined, ReloadOutlined, FilterOutlined, FileTextOutlined } from '@ant-design/icons'
import axios from 'axios'
import 'antd/dist/reset.css'
import { ConfigProvider, theme } from 'antd'

const { Title, Text, Paragraph } = Typography
const { Header, Content } = Layout
const { TabPane } = Tabs
const { TextArea } = Input

// API 配置
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

// 请求拦截器：添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      message.error('登录已过期，请重新登录')
      localStorage.removeItem('token')
      window.location.reload()
    } else if (error.response?.status >= 500) {
      message.error('服务器错误，请稍后重试')
    } else {
      message.error(error.response?.data?.detail || '请求失败')
    }
    return Promise.reject(error)
  }
)

function App() {
  // ============ 状态管理 ============
  const [requirement, setRequirement] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true'
  })
  
  // 历史记录相关状态
  const [historyData, setHistoryData] = useState([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [detailModalVisible, setDetailModalVisible] = useState(false)
  const [selectedRecord, setSelectedRecord] = useState(null)
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [editingRecord, setEditingRecord] = useState(null)
  const [editForm] = Form.useForm()

  // ============ 副作用 ============
  // 暗黑模式切换
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light')
    localStorage.setItem('darkMode', darkMode)
  }, [darkMode])

  // 获取历史记录
  const fetchHistory = async () => {
    setHistoryLoading(true)
    try {
      const response = await api.get('/api/v1/test-cases/db/list')
      if (response.data.status === 'success') {
        setHistoryData(response.data.data || [])
      }
    } catch (error) {
      message.error('获取历史记录失败')
      console.error('Fetch history error:', error)
    } finally {
      setHistoryLoading(false)
    }
  }

  // 初始加载和刷新历史记录
  useEffect(() => {
    fetchHistory()
  }, [])

  // ============ 事件处理 ============
  const handleGenerate = async () => {
    if (!requirement.trim()) {
      message.error('请输入测试需求')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/api/v1/test-cases/generate', {
        requirement: requirement
      })

      setResult(response.data.data?.content || response.data.content)
      message.success('测试用例生成成功！')
      // 生成成功后刷新历史记录
      fetchHistory()
    } catch (error) {
      message.error(error.response?.data?.detail || '生成失败')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = (format) => {
    if (!result) {
      message.error('请先生成测试用例')
      return
    }

    let content = ''
    let filename = ''
    let mimeType = ''

    switch (format) {
      case 'markdown':
        content = result
        filename = 'test-case.md'
        mimeType = 'text/markdown'
        break
      case 'pdf':
        // PDF 生成需要额外处理，这里简化
        message.info('PDF 导出功能开发中')
        return
      case 'excel':
        // Excel 生成需要额外处理
        message.info('Excel 导出功能开发中')
        return
      default:
        content = result
        filename = 'test-case.txt'
        mimeType = 'text/plain'
    }

    // 创建下载
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)

    message.success(`已导出为 ${format.toUpperCase()} 格式`)
  }

  // 查看详情
  const handleViewDetail = (record) => {
    setSelectedRecord(record)
    setDetailModalVisible(true)
  }

  // 打开编辑弹窗
  const handleEdit = (record) => {
    setEditingRecord(record)
    editForm.setFieldsValue({
      title: record.title,
      requirement: record.requirement,
      content: record.content
    })
    setEditModalVisible(true)
  }

  // 保存编辑
  const handleSaveEdit = async (values) => {
    try {
      // 由于没有更新API，这里只在前端更新
      const updatedData = historyData.map(item => 
        item.id === editingRecord.id 
          ? { ...item, ...values }
          : item
      )
      setHistoryData(updatedData)
      message.success('更新成功')
      setEditModalVisible(false)
      setEditingRecord(null)
    } catch (error) {
      message.error('更新失败')
      console.error('Update error:', error)
    }
  }

  // 删除测试用例
  const handleDelete = async (id) => {
    try {
      await api.delete(`/api/v1/test-cases/db/${id}`)
      message.success('删除成功')
      // 刷新列表
      fetchHistory()
    } catch (error) {
      message.error('删除失败')
      console.error('Delete error:', error)
    }
  }

  // ============ 渲染 ============
  return (
    <ConfigProvider theme={{
      algorithm: darkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
    }}>
      <div style={{ 
        minHeight: '100vh',
        background: darkMode ? '#141414' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}>
        <Card style={{ width: 900, borderRadius: 12, maxHeight: '90vh', overflow: 'auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <Title level={3}>🤖 TestAI 智能测试平台</Title>
            <Text type="secondary">基于大语言模型的测试用例智能生成工具</Text>
          </div>

          <Tabs defaultActiveKey="generate" centered>
            <TabPane tab="生成用例" key="generate">
              <div style={{ marginBottom: 16 }}>
                <TextArea
                  rows={5}
                  placeholder="请输入功能需求描述，例如：用户登录功能，支持手机号和验证码登录，验证码5分钟有效..."
                  value={requirement}
                  onChange={(e) => setRequirement(e.target.value)}
                  showCount
                  maxLength={1000}
                />
              </div>
              
              <Button 
                type="primary" 
                size="large"
                loading={loading}
                onClick={handleGenerate}
                block
                icon={!loading && '🚀'}
              >
                {loading ? 'AI 生成中...' : '生成测试用例'}
              </Button>

              {result && (
                <Card 
                  title="生成结果" 
                  style={{ marginTop: 20 }}
                  extra={
                    <Space>
                      <Button icon={<ExportOutlined />} onClick={() => handleExport('markdown')}>
                        导出 Markdown
                      </Button>
                    </Space>
                  }
                >
                  <div style={{ maxHeight: 400, overflow: 'auto' }}>
                    <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'monospace' }}>
                      {result}
                    </pre>
                  </div>
                </Card>
              )}
            </TabPane>

            <TabPane 
              tab={<span><HistoryOutlined /> 历史记录 ({historyData.length})</span>} 
              key="history"
            >
              <div style={{ marginBottom: 16 }}>
                <Space>
                  <Button icon={<ReloadOutlined />} onClick={fetchHistory} loading={historyLoading}>
                    刷新
                  </Button>
                </Space>
              </div>
              
              <Table 
                dataSource={historyData}
                loading={historyLoading}
                rowKey="id"
                pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `共 ${total} 条` }}
                scroll={{ y: 400 }}
                columns={[
                  { 
                    title: 'ID', 
                    dataIndex: 'id', 
                    width: 60,
                    render: (id) => <Tag color="blue">#{id}</Tag>
                  },
                  { 
                    title: '标题', 
                    dataIndex: 'title',
                    ellipsis: true,
                    render: (title, record) => (
                      <Tooltip title={title}>
                        <span style={{ cursor: 'pointer', color: '#1890ff' }} onClick={() => handleViewDetail(record)}>
                          {title}
                        </span>
                      </Tooltip>
                    )
                  },
                  { 
                    title: 'AI 模型', 
                    dataIndex: 'ai_model', 
                    width: 120,
                    render: (model) => <Tag color="green">{model || 'kimi'}</Tag>
                  },
                  { 
                    title: '创建时间', 
                    dataIndex: 'created_at', 
                    width: 170,
                    render: (time) => new Date(time).toLocaleString('zh-CN')
                  },
                  { 
                    title: '操作', 
                    key: 'action', 
                    width: 150,
                    render: (_, record) => (
                      <Space size="small">
                        <Tooltip title="查看">
                          <Button 
                            type="text" 
                            icon={<EyeOutlined />} 
                            onClick={() => handleViewDetail(record)}
                          />
                        </Tooltip>
                        <Tooltip title="编辑">
                          <Button 
                            type="text" 
                            icon={<EditOutlined />} 
                            onClick={() => handleEdit(record)}
                          />
                        </Tooltip>
                        <Tooltip title="删除">
                          <Popconfirm
                            title="确认删除"
                            description="确定要删除这个测试用例吗？此操作不可恢复。"
                            onConfirm={() => handleDelete(record.id)}
                            okText="删除"
                            cancelText="取消"
                            okButtonProps={{ danger: true }}
                          >
                            <Button type="text" danger icon={<DeleteOutlined />} />
                          </Popconfirm>
                        </Tooltip>
                      </Space>
                    )
                  }
                ]}
              />
            </TabPane>
          </Tabs>
        </Card>

        {/* 详情弹窗 */}
        <Modal
          title="测试用例详情"
          open={detailModalVisible}
          onCancel={() => setDetailModalVisible(false)}
          footer={[
            <Button key="close" onClick={() => setDetailModalVisible(false)}>
              关闭
            </Button>
          ]}
          width={800}
        >
          {selectedRecord && (
            <div>
              <Descriptions bordered column={2}>
                <Descriptions.Item label="ID">#{selectedRecord.id}</Descriptions.Item>
                <Descriptions.Item label="AI 模型">{selectedRecord.ai_model || 'kimi'}</Descriptions.Item>
                <Descriptions.Item label="创建时间">{new Date(selectedRecord.created_at).toLocaleString('zh-CN')}</Descriptions.Item>
                <Descriptions.Item label="标题" span={2}>{selectedRecord.title}</Descriptions.Item>
              </Descriptions>
              
              <Divider orientation="left">需求描述</Divider>
              <div style={{ background: '#f5f5f5', padding: 12, borderRadius: 4, marginBottom: 16 }}>
                <Text>{selectedRecord.requirement}</Text>
              </div>
              
              <Divider orientation="left">测试用例内容</Divider>
              <div style={{ maxHeight: 400, overflow: 'auto', background: '#f5f5f5', padding: 12, borderRadius: 4 }}>
                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'monospace', margin: 0 }}>
                  {selectedRecord.content}
                </pre>
              </div>
            </div>
          )}
        </Modal>

        {/* 编辑弹窗 */}
        <Modal
          title="编辑测试用例"
          open={editModalVisible}
          onCancel={() => {
            setEditModalVisible(false)
            setEditingRecord(null)
            editForm.resetFields()
          }}
          onOk={() => {
            editForm.validateFields().then(values => {
              handleSaveEdit(values)
            })
          }}
          okText="保存"
          cancelText="取消"
          width={700}
        >
          <Form form={editForm} layout="vertical">
            <Form.Item
              name="title"
              label="标题"
              rules={[{ required: true, message: '请输入标题' }]}
            >
              <Input placeholder="测试用例标题" />
            </Form.Item>
            <Form.Item
              name="requirement"
              label="需求描述"
              rules={[{ required: true, message: '请输入需求描述' }]}
            >
              <TextArea rows={4} placeholder="功能需求描述" />
            </Form.Item>
            <Form.Item
              name="content"
              label="测试用例内容"
              rules={[{ required: true, message: '请输入测试用例内容' }]}
            >
              <TextArea rows={8} placeholder="测试用例详细内容" style={{ fontFamily: 'monospace' }} />
            </Form.Item>
          </Form>
        </Modal>
      </div>
    </ConfigProvider>
  )
}

export default App
