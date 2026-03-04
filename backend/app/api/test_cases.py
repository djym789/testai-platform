"""
测试用例 API 路由
提供 AI 生成测试用例的接口
"""
from fastapi import APIRouter, HTTPException
from app.services.ai_service import AIService
from pydantic import BaseModel, Field

router = APIRouter()

class RequirementInput(BaseModel):
    """
    需求输入模型
    """
    requirement: str = Field(
        ..., 
        description="用户的功能需求描述",
        example="用户登录功能，支持手机号和验证码登录，验证码5分钟有效"
    )

@router.post(
    "/generate", 
    summary="AI 生成测试用例",
    description="基于用户需求，使用 Kimi AI 自动生成详细的测试用例"
)
def generate_test_case(input: RequirementInput):
    """
    基于需求自动生成测试用例
    
    - **requirement**: 用户的功能需求描述
    - **返回**: AI 生成的测试用例内容
    """
    try:
        # 初始化 AI 服务
        ai_service = AIService()
        
        # 调用 AI 生成（同步版本）
        result = ai_service.generate_test_case(input.requirement)
        
        # 检查是否成功
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # 返回成功结果
        return {
            "status": "success",
            "data": result["content"],
            "requirement": input.requirement,
            "ai_model": result["model"]
        }
        
    except ValueError as e:
        # 配置错误（如 API Key 未设置）
        raise HTTPException(status_code=500, detail=f"服务配置错误: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        # 其他未预料的错误
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.get(
    "/hello",
    summary="服务健康检查",
    description="测试 API 服务是否正常运行"
)
def hello():
    """
    简单的健康检查接口
    """
    return {
        "message": "TestAI API 运行中", 
        "status": "ok",
        "service": "Kimi AI Test Case Generator",
        "version": "0.1.0"
    }
