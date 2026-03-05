"""
TestAI - 智能测试平台后端主入口
基于 FastAPI 和 Kimi AI 构建
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import test_cases
from app.api import test_case_db

# 创建 FastAPI 应用实例
app = FastAPI(
    title="TestAI - 智能测试平台",
    description="""
    基于 Kimi (Moonshot) 大语言模型的智能测试用例生成平台。
    
    ## 核心功能
    * **AI 生成测试用例**：基于自然语言需求描述，自动生成详细的测试用例
    * **Kimi AI 驱动**：利用 Moonshot 大模型的中文理解能力，生成精准的测试场景
    * **RESTful API**：标准化的 API 设计，支持前后端分离架构
    
    ## 技术栈
    * **后端**：Python, FastAPI, Uvicorn
    * **AI 引擎**：Kimi (Moonshot) v1-8k
    * **通信**：RESTful API, WebSocket (预留)
    """,
    version="0.1.0",
    contact={
        "name": "TestAI Team",
        "url": "https://github.com/djym789/testai-platform",
    },
    license_info={
        "name": "MIT License",
    },
)

# 配置 CORS 中间件（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(
    test_cases.router,
    prefix="/api/v1/test-cases",
    tags=["测试用例生成"],
    responses={
        500: {"description": "服务器内部错误"},
        422: {"description": "请求参数验证失败"},
    },
)

# 数据库相关的测试用例管理
app.include_router(
    test_case_db.router,
    prefix="/api/v1/test-cases/db",
    tags=["测试用例数据库管理"]
)


# 根路径端点（服务状态检查）
@app.get(
    "/",
    summary="服务根路径",
    description="返回服务基本信息和文档链接"
)
def root():
    return {
        "message": "TestAI API 运行中",
        "status": "ok",
        "service": "智能测试用例生成平台",
        "ai_engine": "Kimi (Moonshot AI)",
        "version": "0.1.0",
        "documentation": "/docs",
        "health_check": "/health",
    }

# 健康检查端点
@app.get(
    "/health",
    summary="健康检查",
    description="用于负载均衡和监控的健康检查端点"
)
def health_check():
    return {
        "status": "healthy",
        "service": "TestAI API",
        "timestamp": "running",
    }
