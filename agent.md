# TestAI - 智能测试平台 Agent 配置

> 本文件是 AI Agent 的行为约束，不是项目 README。
> Agent 读取本文件后应知道：能做什么、不能做什么、怎么验证。

**技术栈**: FastAPI 3.11 + React 18 + Vite + Ant Design 5.x + SQLAlchemy 2.0 + Kimi (Moonshot) API

---

## 项目地图

testai-platform/ # 项目根目录 ├── backend/ # 后端代码（Python） │ ├── app/ │ │ ├── api/ # API 路由（FastAPI endpoints） │ │ │ ├── test_cases.py # AI 生成接口（原有） │ │ │ └── test_case_db.py # 数据库管理接口（新增） │ │ ├── crud/ # 数据库 CRUD 操作（SQLAlchemy） │ │ │ └── test_case.py │ │ ├── models/ # 数据模型定义 │ │ │ └── database.py # SQLAlchemy 模型（TestCase 表定义） │ │ ├── services/ # 业务逻辑 │ │ │ └── ai_service.py # Kimi AI 调用封装 │ │ └── main.py # FastAPI 入口、CORS、生命周期、路由注册 │ ├── requirements.txt # Python 依赖（FastAPI、SQLAlchemy等） │ ├── .env # ⚠️ 环境变量（API Key等，不提交Git） │ └── testai.db # ⚠️ SQLite 数据库文件（自动生成，不提交Git） ├── frontend/ # 前端代码（React） │ ├── src/ │ │ ├── App.jsx # 主页面（测试用例生成UI） │ │ └── main.jsx # React入口 │ └── package.json # Node依赖 ├── .gitignore # Git忽略配置（已排除.env和*.db） ├── README.md # 项目说明文档（给用户看的） └── agent.md # 本文件（给AI看的开发规范）


> 本地图是语义摘要，非完整文件列表。新增模块时更新此处。

---

## 核心规则

### 1. 前后端同步

前后端是一个整体。以下变更必须双向检查：

| 后端变更 | 必须检查前端 |
|----------|-------------|
| API 路由路径/参数变更 | Axios 调用点是否同步更新 |
| 响应结构变更（字段增删改） | 前端解析和渲染是否适配 |
| 新增 API 端点 | 前端是否有对应调用入口 |

**违反此规则 = 制造 bug。没有例外。**

### 2. 先理解再动手

每次修改前问三个问题：
1. **这是真实需求还是我的猜测？** — 不确定就问用户
2. **有更简单的方案吗？** — 永远先写最简实现
3. **会破坏现有功能吗？** — 改 API 前检查所有调用方

### 3. 范围约束

遇到当前任务范围外的问题（环境配置、第三方服务异常、架构重构），**立即停止并询问用户**。不要擅自添加 workaround 或超出范围的代码。

---

## 禁止行为

| 编号 | 禁止 | 原因 |
|------|------|------|
| F-01 | **硬编码 API Key 或密钥到源码** | 安全风险，密钥只能通过 `.env` 引入 |
| F-02 | **在 commit message / 日志中泄露敏感信息** | 版本历史永久保留 |
| F-03 | **不看错误信息就猜测修复** | 浪费时间，引入新 bug |
| F-04 | **失败后不分析原因直接重跑** | 重跑不是调试 |
| F-05 | **修改 API 接口不检查前端调用方** | 制造运行时错误 |
| F-06 | **绕过 ORM 直接拼 SQL 字符串** | SQL 注入风险 |
| F-07 | **`git add .` 提交所有文件** ⚠️ **特别注意** | **`.env`、数据库文件、虚拟环境目录必须排除** |
| F-08 | **修改数据库模型不说明迁移方式** | 数据丢失风险 |

**特别强调 F-07：**
- ✅ `.env` 已在 `.gitignore` 中，正常情况不会被提交
- ✅ `*.db` 已在 `.gitignore` 中，正常情况不会被提交  
- ⚠️ **但 `git add .` 是危险操作**，建议明确添加：`git add backend/app/api/test_case_db.py` 等具体文件

---

## 编码规范

### Python（后端）

```python
# 导入顺序：标准库 → 第三方 → 本地（空行分隔）
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.models.database import TestCase
from app.services.ai_service import AIService
所有函数必须有类型注解（参数 + 返回值）
错误处理：API 层捕获异常并返回明确的 HTTP 状态码和错误描述，不要返回裸 500
数据库操作：只通过 SQLAlchemy ORM，禁止原生 SQL 拼接
环境变量：通过 os.getenv() 或 pydantic Settings 读取，不硬编码
JavaScript/React（前端）
组件命名：大驼峰 (PascalCase)，如 TestCaseGenerator
变量/函数命名：小驼峰 (camelCase)
状态管理：使用 useState, useEffect
异步处理：使用 async/await，配合 try-catch
调试协议
测试或功能出问题时，按以下顺序排查，不要跳步：

1. 读错误信息  → 理解报错的具体位置和类型
2. 检查 API    → 后端 /docs (Swagger) 中手动测试对应接口
3. 检查前端    → 浏览器 DevTools Network 看请求/响应
4. 检查数据    → 确认数据库中数据状态是否符合预期
5. 定位修复    → 基于以上证据修改代码
禁止：

不看日志直接改代码（盲修）
报错后不分析直接重启服务（盲跑）
前端报错只看前端、后端报错只看后端（必须看完整链路）
数据库变更规则
SQLAlchemy 模型修改需要注意：

新增字段：设置 default 或 nullable=True，避免已有数据报错
删除/重命名字段：告知用户需要迁移或重建数据库，确认后再执行
开发环境使用 SQLite（testai.db），该文件已在 .gitignore 中
生产环境使用 PostgreSQL，模型变更需配合 Alembic migration
任何可能导致数据丢失的操作，必须先询问用户。

测试策略
后端测试
# 在 backend/ 目录下执行
python -m pytest tests/ -v
API 端点：使用 FastAPI TestClient 测试请求/响应
业务逻辑：单元测试 services/ 中的函数，mock AI API 调用
数据库操作：使用内存 SQLite 隔离测试数据
前端测试
组件渲染：确认核心交互流程可用
API 集成：mock Axios 响应，验证组件状态更新
必须测试的场景
场景	验证内容
AI 生成成功	返回结构化测试用例，前端正确渲染
AI 生成失败（API 超时/额度不足）	后端返回明确错误码，前端展示友好提示
空输入	前后端都有校验，不发送无效请求
数据库 CRUD	创建/读取/更新/删除均正常
安全清单
 .env 在 .gitignore 中，不提交到版本控制
 API Key 通过环境变量注入，代码中无硬编码
 CORS 配置明确限定允许的 origin（生产环境不用 *）
 用户输入在后端有校验（长度、格式）
 数据库操作通过 ORM，不拼接 SQL
常用命令
# === 后端 ===
cd backend
python -m venv venv && source venv/bin/activate  # Linux/Mac
# venv\Scripts\Activate.ps1                      # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# === 前端 ===
cd frontend
npm install
npm run dev

# === Git（提交前检查） ===
git status                    # 确认不包含 .env 和 *.db 文件
git add <具体文件>            # 不要用 git add .
git commit -m "type: 描述"    # type: feat/fix/refactor/docs/test
git push
功能扩展建议
 用户认证系统（登录/注册）
 测试用例导出（PDF、Excel、Markdown）
 批量生成多个测试用例
 测试用例分类和标签
 团队协作（共享测试用例）
 集成 CI/CD 自动测试