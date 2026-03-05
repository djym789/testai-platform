from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db, TestCase, create_tables
from app.crud.test_case import (
    create_test_case, get_test_cases, get_test_case, 
    delete_test_case
)

router = APIRouter()

# 确保数据库表已创建
@router.on_event("startup")
async def startup_event():
    create_tables()

@router.post("/save", response_model=dict)
async def save_test_case(
    title: str,
    requirement: str,
    content: str,
    ai_model: str = "kimi",
    db: Session = Depends(get_db)
):
    """保存测试用例到数据库"""
    try:
        test_case = create_test_case(
            db=db,
            title=title,
            requirement=requirement,
            content=content,
            ai_model=ai_model
        )
        return {
            "status": "success",
            "message": "测试用例保存成功",
            "data": test_case.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")

@router.get("/list", response_model=dict)
async def list_test_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取测试用例列表"""
    try:
        test_cases = get_test_cases(db, skip=skip, limit=limit)
        return {
            "status": "success",
            "count": len(test_cases),
            "data": [tc.to_dict() for tc in test_cases]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.get("/{test_case_id}", response_model=dict)
async def get_test_case_detail(test_case_id: int, db: Session = Depends(get_db)):
    """获取单个测试用例详情"""
    try:
        test_case = get_test_case(db, test_case_id=test_case_id)
        if not test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return {
            "status": "success",
            "data": test_case.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.delete("/{test_case_id}", response_model=dict)
async def delete_test_case_by_id(test_case_id: int, db: Session = Depends(get_db)):
    """删除测试用例"""
    try:
        success = delete_test_case(db, test_case_id=test_case_id)
        if not success:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return {
            "status": "success",
            "message": "测试用例删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
