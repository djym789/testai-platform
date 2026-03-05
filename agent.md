# TestAI - 智能测试平台 Agent 配置

## 项目概述

**TestAI** 是一个基于大语言模型的智能测试用例生成平台，采用前后端分离架构。

- **核心功能**：输入自然语言需求，AI 自动生成结构化测试用例
- **AI 引擎**：Kimi (Moonshot) 大语言模型
- **目标用户**：软件测试工程师、开发团队

---

## 技术栈

### 后端
- **框架**：FastAPI (Python 3.11)
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **ORM**：SQLAlchemy 2.0
- **AI 调用**：HTTP Requests (同步)
- **API 文档**：Swagger/OpenAPI (自动生成)

### 前端
- **框架**：React 18
- **构建工具**：Vite
- **UI 组件库**：Ant Design 5.x
- **HTTP 客户端**：Axios
- **样式**：CSS-in-JS (内联样式)

### 开发工具
- **版本控制**：Git
- **包管理**：pip (Python) / npm (Node.js)
- **虚拟环境**：venv

---

## 项目结构

testai-platform/ ├── backend/ # 后端代码 │ ├── app/ │ │ ├── api/ # API 路由 │ │ │ ├── test_cases.py # AI 生成接口 │ │ │ └── test_case_db.py # 数据库管理接口 │ │ ├── crud/ # 数据库 CRUD 操作 │ │ │ └── test_case.py │ │ ├── models/ # 数据模型 │ │ │ └── database.py # SQLAlchemy 模型 │ │ ├── services/ # 业务逻辑 │ │ │ └── ai_service.py # Kimi AI 调用 │ │ └── main.py # FastAPI 入口 │ ├── requirements.txt # Python 依赖 │ └── .env # 环境变量 (不提交到 Git) ├── frontend/ # 前端代码 │ ├── src/ │ │ ├── App.jsx # 主页面 │ │ └── main.jsx # 入口 │ ├── package.json # Node 依赖 │ └── ... ├── testai.db # SQLite 数据库文件 (自动生成) └── README.md # 项目说明


---

## 开发规范

### Python (后端)

1. **导入顺序**：
   - 标准库 (os, sys, datetime)
   - 第三方库 (fastapi, sqlalchemy)
   - 本地模块 (from app.models...)

2. **类型注解**：函数参数和返回值使用类型提示
   ```python
   def generate_test_case(self, requirement: str) -> dict:
异步/同步：
数据库操作用 SQLAlchemy ORM（同步）
HTTP 调用用 requests（同步，简单稳定）
API 路由可以用 async（FastAPI 支持）
错误处理：使用 try-except 包裹可能出错的操作，返回友好的错误信息
JavaScript/React (前端)
组件命名：大驼峰 (PascalCase)，如 TestCaseGenerator
变量命名：小驼峰 (camelCase)
状态管理：使用 useState, useEffect
异步处理：使用 async/await，配合 try-catch
常用命令
启动开发环境
后端：

cd F:\testai-platform\backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
前端：

cd F:\testai-platform\frontend
npm run dev
安装依赖
后端：

pip install -r requirements.txt
前端：

npm install
Git 操作
# 查看状态
git status

# 添加文件
git add .

# 提交
git commit -m "feat: 描述"

# 推送
git push
环境变量 (.env 文件)
在项目根目录 backend/.env：

# Kimi (Moonshot) API Key
# 从 https://platform.moonshot.cn/ 获取
MOONSHOT_API_KEY=sk-xxxxxxxxxxxxxxxx

# 数据库配置（可选，默认使用 SQLite）
# DATABASE_URL=postgresql://user:password@localhost:5432/testai

# 环境设置
ENVIRONMENT=development
DEBUG=true
⚠️ 重要：.env 文件不要提交到 Git，已添加到 .gitignore

调试技巧
查看 API 文档：启动后端后访问 http://127.0.0.1:8000/docs
检查数据库：使用 VS Code SQLite 插件查看 testai.db
查看日志：后端控制台会输出请求和错误信息
前端调试：浏览器 F12 打开开发者工具，查看 Console 和 Network
常见问题
Q: 前端无法连接到后端？ A: 检查后端是否运行在 http://127.0.0.1:8000，并检查 CORS 配置。

Q: Kimi API 调用失败？ A: 检查 MOONSHOT_API_KEY 是否正确，账户是否有余额。

Q: 数据库表没有创建？ A: 确保重启了后端服务，SQLAlchemy 会在启动时自动创建表。

功能扩展建议
 用户认证系统（登录/注册）
 测试用例导出（PDF、Excel、Markdown）
 批量生成多个测试用例
 测试用例分类和标签
 团队协作（共享测试用例）
 集成 CI/CD 自动测试