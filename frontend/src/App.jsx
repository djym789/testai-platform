import { useState } from 'react'
import { Input, Button, Card, Spin, Typography, message, Layout } from 'antd'
import axios from 'axios'
import 'antd/dist/reset.css'

const { Title, Paragraph, Text } = Typography
const { TextArea } = Input
const { Header, Content } = Layout

// 后端 API 地址
const API_BASE_URL = 'http://127.0.0.1:8000'

function App() {
  const [requirement, setRequirement] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      message.error('请输入测试需求')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/test-cases/generate`, {
        requirement: requirement
      })
      
      if (response.data.status === 'success') {
        setResult(response.data.data)
        message.success('测试用例生成成功！')
      } else {
        message.error('生成失败')
      }
    } catch (error) {
      console.error('Error:', error)
      message.error(error.response?.data?.detail || '请求失败，请检查后端服务是否运行')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <Header style={{ background: 'rgba(255, 255, 255, 0.1)', backdropFilter: 'blur(10px)' }}>
        <Title level={3} style={{ color: 'white', margin: '16px 0', textAlign: 'center' }}>
          🤖 TestAI - 智能测试用例生成平台
        </Title>
      </Header>
      
      <Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        <Card 
          title="输入测试需求" 
          style={{ marginBottom: 24, borderRadius: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
        >
          <TextArea
            rows={6}
            placeholder="请输入功能需求描述，例如：用户登录功能，支持手机号和验证码登录，验证码5分钟有效，需要验证手机号格式..."
            value={requirement}
            onChange={(e) => setRequirement(e.target.value)}
            style={{ fontSize: 16, borderRadius: 8 }}
          />
          <Button 
            type="primary" 
            size="large"
            onClick={handleGenerate}
            loading={loading}
            style={{ 
              marginTop: 16, 
              width: '100%', 
              height: 48,
              fontSize: 18,
              borderRadius: 8,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none'
            }}
          >
            {loading ? 'AI 正在生成中...' : '🚀 生成测试用例'}
          </Button>
        </Card>

        {result && (
          <Card 
            title="✅ 生成的测试用例" 
            style={{ 
              marginBottom: 24, 
              borderRadius: 12, 
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
              background: '#f6ffed',
              border: '1px solid #b7eb8f'
            }}
          >
            <div style={{ 
              whiteSpace: 'pre-wrap', 
              fontFamily: 'monospace', 
              overflowY: 'auto',
              maxHeight: '400px',
              padding: '10px'
            }}>
              {result}
            </div>
          </Card>
        )}

        <Paragraph type="secondary" style={{ textAlign: 'center', color: 'rgba(255,255,255,0.8)' }}>
          Powered by FastAPI + React + Kimi AI
        </Paragraph>
      </Content>
    </Layout>
  )
}

export default App
