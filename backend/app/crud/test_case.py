from sqlalchemy.orm import Session
from app.models.database import TestCase

def create_test_case(db: Session, title: str, requirement: str, content: str, ai_model: str):
    """创建测试用例"""
    db_test_case = TestCase(
        title=title,
        requirement=requirement,
        content=content,
        ai_model=ai_model
    )
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case

def get_test_cases(db: Session, skip: int = 0, limit: int = 100):
    """获取测试用例列表"""
    return db.query(TestCase).order_by(TestCase.created_at.desc()).offset(skip).limit(limit).all()

def get_test_case(db: Session, test_case_id: int):
    """根据ID获取单个测试用例"""
    return db.query(TestCase).filter(TestCase.id == test_case_id).first()

def delete_test_case(db: Session, test_case_id: int):
    """删除测试用例"""
    db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if db_test_case:
        db.delete(db_test_case)
        db.commit()
        return True
    return False
