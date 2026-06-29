import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 환경변수에서 DB URL을 읽어옴 (docker-compose에서 주입)
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://todo_user:todo_pass@localhost:3306/todo_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# FastAPI 의존성(Dependency)으로 사용할 DB 세션 생성기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
