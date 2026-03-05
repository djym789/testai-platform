from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db, TestCase, create_tables
from app.crud.test_case import (
    create_test_case, get_test_cases, get_test_case, 
    delete_test_case, update_test_case, get_categories, get_tags
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
    tags: str = "",
    category: str = "功能测试",
    priority: str = "中",
    db: Session = Depends(get_db)
):
    """保存测试用例到数据库"""
    try:
        test_case = create_test_case(
            db=db,
            title=title,
            requirement=requirement,
            content=content,
            ai_model=ai_model,
            tags=tags,
            category=category,
            priority=priority
        )
        return {
            "status": "success",
            "message": "测试用例保存成功",
            "data": test_case.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")

@router.get("/list", response_model=dict)
async def list_test_cases(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    category: Optional[str] = Query(None, description="按分类筛选"),
    tag: Optional[str] = Query(None, description="按标签筛选"),
    db: Session = Depends(get_db)
):
    """获取测试用例列表，支持分页和筛选"""
    try:
        test_cases = get_test_cases(
            db, 
            skip=skip, 
            limit=limit, 
            category=category, 
            tag=tag
        )
        return {
            "status": "success",
            "count": len(test_cases),
            "data": [tc.to_dict() for tc in test_cases]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.get("/categories", response_model=dict)
async def list_categories(db: Session = Depends(get_db)):
    """获取所有分类列表"""
    try:
        categories = get_categories(db)
        return {
            "status": "success",
            "data": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分类失败: {str(e)}")

@router.get("/tags", response_model=dict)
async def list_tags(db: Session = Depends(get_db)):
    """获取所有标签列表"""
    try:
        tags = get_tags(db)
        return {
            "status": "success",
            "data": tags
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取标签失败: {str(e)}")

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

@router.put("/{test_case_id}", response_model=dict)
async def update_test_case_endpoint(
    test_case_id: int,
    title: str = None,
    requirement: str = None,
    content: str = None,
    tags: str = None,
    category: str = None,
    priority: str = None,
    db: Session = Depends(get_db)
):
    """更新测试用例"""
    try:
        test_case = update_test_case(
            db, 
            test_case_id=test_case_id,
            title=title,
            requirement=requirement,
            content=content,
            tags=tags,
            category=category,
            priority=priority
        )
        if not test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return {
            "status": "success",
            "message": "测试用例更新成功",
            "data": test_case.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

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
