from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

app = FastAPI()

router = APIRouter(prefix="/sessions", tags=["sessions"])
sessions = {}

class SessionCreate(BaseModel):
    user_id: int
    bot_name: str

@router.post("/")
def create_session(request: SessionCreate):
    session_id = len(sessions) + 1
    # ✏️ [실습 1] sessions 딕셔너리에 새 세션을 저장하세요.
    # 키는 session_id, 값은 id/user_id/bot_name/messages 필드를 가진 딕셔너리입니다.
    sessions[session_id] = {
        # 여기에 세션 정보를 채워보세요
    }
    return sessions[session_id]

@router.get("/{session_id}")
def get_session(session_id: int):
    # ✏️ [실습 2] session_id가 sessions에 없으면 404 에러를 반환하세요.
    # 여기에 조건문과 HTTPException을 작성하세요
    return sessions[session_id]

@router.delete("/{session_id}")
def delete_session(session_id: int):
    # ✏️ [실습 3] sessions에서 session_id를 삭제하세요.
    # pop(key, None)을 사용하면 키가 없어도 에러 없이 처리됩니다.
    # 여기에 삭제 코드를 작성하세요
    return {"status": "deleted", "session_id": session_id}