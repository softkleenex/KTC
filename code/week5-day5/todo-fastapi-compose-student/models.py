from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class TodoModel(Base):
    __tablename__ = "todos"

    id        = Column(Integer, primary_key=True, index=True)
    text      = Column(String(500), nullable=False)  # MySQL은 VARCHAR 길이 필수
    completed = Column(Boolean, default=False, nullable=False)
