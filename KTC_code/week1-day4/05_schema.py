from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

app = FastAPI()

# 클라이언트가 보내는 요청 데이터 구조 (비밀번호 포함)
class MessageRequest(BaseModel):
    user_id: int
    content: str = Field(min_length=1, max_length=5)
    password: str

# 서버가 밖으로 내보내는 응답 데이터 구조
class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime
    status: str
    # password 필드는 없음 → response_model에 의해 자동으로 클라이언트에게 숨겨짐

@app.post("/messages", response_model=MessageResponse)
def create_message(request: MessageRequest):
    return MessageResponse(
        id=1,
        user_id=request.user_id,
        content=request.content,
        created_at=datetime.now(),
        status="sent",
    )

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    email: EmailStr       # 이메일 형식 자동 검증
    age: int = Field(ge=0, le=150)
    bio: str = Field(default="", max_length=500)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    bio: str

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return UserResponse(
        id=1,
        name=user.name,
        email=user.email,
        age=user.age,
        bio=user.bio,
    )