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

# 测试用例模型
class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # 用例标题
    requirement = Column(Text)                # 原始需求
    content = Column(Text)                     # 生成的完整内容
    ai_model = Column(String(50))            # 使用的AI模型
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "requirement": self.requirement,
            "content": self.content,
            "ai_model": self.ai_model,
            "created_at": self.created_at.isoformat() if self.created_at else None
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
