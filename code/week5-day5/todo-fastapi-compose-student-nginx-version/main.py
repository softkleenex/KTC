from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import TodoModel

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

# Nginx 확장 실습에서는 FastAPI가 HTML/CSS/JS를 직접 렌더링하지 않습니다.
# FastAPI는 /api 로 시작하는 JSON API만 담당하고,
# index.html, style.css, script.js 같은 프론트엔드 파일은 Nginx가 배포합니다.
#
# 수업에서는 localhost, 컨테이너 포트, RDS 전환 등으로 Origin이 자주 바뀔 수 있습니다.
# CORS 때문에 실습이 막히지 않도록 모든 Origin/Method/Header를 허용합니다.
# 운영 환경에서는 allow_origins를 실제 프론트엔드 도메인으로 좁혀야 합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic 스키마 ────────────────────────────────────────────
class TodoCreate(BaseModel):
    text: str

class Todo(BaseModel):
    id: int
    text: str
    completed: bool

    class Config:
        from_attributes = True  # SQLAlchemy 모델 → Pydantic 변환 허용


# ── API 라우트: 모든 Todo 가져오기 ──────────────────────────────
@app.get("/api/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


# ── 상태 확인 라우트 ────────────────────────────────────────────
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "todo-api"}


# ── API 라우트: 새 Todo 추가 ────────────────────────────────────
@app.post("/api/todos", response_model=Todo, status_code=201)
def create_todo(body: TodoCreate, db: Session = Depends(get_db)):
    if not body.text or not body.text.strip():
        raise HTTPException(status_code=400, detail="Todo 텍스트가 필요합니다.")

    new_todo = TodoModel(text=body.text.strip(), completed=False)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# ── API 라우트: Todo 완료 상태 토글 ────────────────────────────
@app.patch("/api/todos/{todo_id}", response_model=Todo)
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다.")

    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


# ── API 라우트: Todo 삭제 ───────────────────────────────────────
@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo를 찾을 수 없습니다.")

    db.delete(todo)
    db.commit()


# ── 직접 실행 시 ────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
