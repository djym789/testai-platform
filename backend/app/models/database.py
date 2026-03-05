"""
数据库模型：TestCase（测试用例）
使用 SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 使用 SQLite（文件存储，当前目录下的 testai.db）
DATABASE_URL = "sqlite:///./testai.db"

# 创建引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()


# ==================== TestCase 测试用例模型 ====================

class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    requirement = Column(Text)
    content = Column(Text)
    ai_model = Column(String(50))
    tags = Column(String(255), default="")  # 标签，以逗号分隔
    category = Column(String(50), default="功能测试")  # 分类
    priority = Column(String(20), default="中")  # 优先级
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "requirement": self.requirement,
            "content": self.content,
            "ai_model": self.ai_model,
            "tags": self.tags,
            "category": self.category,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 创建所有表
def create_tables():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
