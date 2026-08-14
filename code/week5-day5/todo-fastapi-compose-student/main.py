from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import TodoModel

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

# 정적 파일 서빙 (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Pydantic 스키마 ────────────────────────────────────────────
class TodoCreate(BaseModel):
    text: str

class Todo(BaseModel):
    id: int
    text: str
    completed: bool

    class Config:
        from_attributes = True  # SQLAlchemy 모델 → Pydantic 변환 허용


# ── 라우트: 정적 페이지 ─────────────────────────────────────────
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


# ── API 라우트: 모든 Todo 가져오기 ──────────────────────────────
@app.get("/api/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


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
