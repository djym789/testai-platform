# 🤖 TestAI - 智能测试平台

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🏗️ 技术架构

```mermaid
flowchart TB
    subgraph Frontend["前端层 - React"]
        UI1[测试用例管理]
        UI2[AI生成控制台]
        UI3[报告可视化]
    end

    subgraph Backend["后端服务层 - FastAPI"]
        API[API Gateway]
        CM[用例管理模块]
        EX[测试执行模块]
        RG[报告生成模块]
    end

    subgraph AI["AI服务层"]
        AG[AI生成引擎]
        OPT[优化引擎]
        LLM[(GPT-4/Claude)]
    end

    subgraph Data["数据存储层"]
        DB[(PostgreSQL)]
        Cache[(Redis)]
        File[(MinIO)]
    end

    Frontend --> API
    API --> CM & EX & RG
    CM --> AG
    AG --> LLM
    Backend --> Data
```

## 🚀 快速开始
###  环境要求
Python 3.11+
Node.js 18+
PostgreSQL 14+
Redis 6+
OpenAI API Key（或 Claude API Key）

###  1. 克隆项目

git clone https://github.com/djym789/testai-platform.git

cd testai-platform

###  2. 启动依赖服务（Docker）

docker-compose up -d postgres redis minio

###  3. 配置环境变量
cp backend/.env.example backend/.env

编辑 .env 文件，设置以下变量：

OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/testai
REDIS_URL=redis://localhost:6379
###  4. 启动后端服务
cd backend

python -m venv venv


pip install -r requirements.txt

alembic upgrade head  # 数据库迁移

uvicorn app.main:app --reload --port 8000

后端服务运行在 http://localhost:8000

API 文档：http://localhost:8000/docs

###  5. 启动前端服务
cd frontend
npm install
npm run dev
前端服务运行在 http://localhost:5173

## 📂 项目结构

```text
testai-platform/
├── backend/               # 后端服务
│   ├── app/
│   │   ├── api/          # API路由
│   │   └── services/     # 业务逻辑
│   └── main.py           # 入口
├── frontend/              # 前端服务
│   └── src/
└── README.md
```


## 🎯 核心功能

🤖 AI生成测试用例：基于需求文档自动生成测试用例，效率提升70%

🚀 自动化测试执行：支持API和UI自动化测试

📊 可视化报告：实时展示测试进度、通过率、覆盖率

🔍 智能分析：失败用例自动分类和根因分析

## 📧 联系

项目主页：https://github.com/djym789/testai-platform

问题反馈：https://github.com/djym789/testai-platform/issues

如果这个项目对你有帮助，请给个 ⭐ Star！



