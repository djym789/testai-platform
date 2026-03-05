from sqlalchemy.orm import Session
from app.models.database import TestCase


def create_test_case(
    db: Session, 
    title: str, 
    requirement: str, 
    content: str, 
    ai_model: str = "kimi",
    tags: str = "",
    category: str = "功能测试",
    priority: str = "中"
):
    """创建测试用例"""
    db_test_case = TestCase(
        title=title,
        requirement=requirement,
        content=content,
        ai_model=ai_model,
        tags=tags,
        category=category,
        priority=priority
    )
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case


def get_test_cases(db: Session, skip: int = 0, limit: int = 100, category: str = None, tag: str = None):
    """获取测试用例列表，支持按分类和标签筛选"""
    query = db.query(TestCase)
    
    if category:
        query = query.filter(TestCase.category == category)
    
    if tag:
        query = query.filter(TestCase.tags.contains(tag))
    
    return query.order_by(TestCase.created_at.desc()).offset(skip).limit(limit).all()


def get_test_case(db: Session, test_case_id: int):
    """获取单个测试用例"""
    return db.query(TestCase).filter(TestCase.id == test_case_id).first()


def update_test_case(
    db: Session, 
    test_case_id: int, 
    title: str = None, 
    requirement: str = None, 
    content: str = None,
    tags: str = None,
    category: str = None,
    priority: str = None
):
    """更新测试用例"""
    db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not db_test_case:
        return None
    
    if title is not None:
        db_test_case.title = title
    if requirement is not None:
        db_test_case.requirement = requirement
    if content is not None:
        db_test_case.content = content
    if tags is not None:
        db_test_case.tags = tags
    if category is not None:
        db_test_case.category = category
    if priority is not None:
        db_test_case.priority = priority
    
    db.commit()
    db.refresh(db_test_case)
    return db_test_case


def delete_test_case(db: Session, test_case_id: int):
    """删除测试用例"""
    db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not db_test_case:
        return False
    
    db.delete(db_test_case)
    db.commit()
    return True


def get_categories(db: Session):
    """获取所有分类"""
    categories = db.query(TestCase.category).distinct().all()
    return [c[0] for c in categories if c[0]]


def get_tags(db: Session):
    """获取所有标签"""
    all_tags = db.query(TestCase.tags).all()
    tag_set = set()
    for tags_str in all_tags:
        if tags_str[0]:
            for tag in tags_str[0].split(','):
                tag_set.add(tag.strip())
    return sorted(list(tag_set))