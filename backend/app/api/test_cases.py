"""
测试用例 API 路由
提供 AI 生成测试用例的接口
"""
from fastapi import APIRouter, HTTPException
from app.services.ai_service import AIService
from pydantic import BaseModel, Field

router = APIRouter()

class RequirementInput(BaseModel):
    requirement: str = Field(
        ..., 
        description="用户的功能需求描述",
        example="用户登录功能，支持手机号和验证码登录，验证码5分钟有效"
    )

@router.post("/generate")
def generate_test_case(input: RequirementInput):  # 去掉 async，改成普通函数
    """
    基于需求自动生成测试用例
    """
    try:
        ai_service = AIService()
        result = ai_service.generate_test_case(input.requirement)  # 去掉 await
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "data": result["content"],
            "requirement": input.requirement,
            "ai_model": result["model"]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"服务配置错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.get("/hello")
def hello():  # 去掉 async
    return {
        "message": "TestAI API 运行中", 
        "status": "ok",
        "service": "Kimi AI Test Case Generator"
    }
