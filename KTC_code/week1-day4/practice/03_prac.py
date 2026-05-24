from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="카카오 데이터 검증 실습")

class MessageRequest(BaseModel):
    # 1. 사용자 ID (필수, 정수형)
    user_id: int
    
    # 2. 메시지 내용 (최소 1자 / 최대 5자)
    content: str = Field(# TODO)
    
    # 3. 최대 토큰 값 (기본값: 500, 최소 100 이상 / 최대 2000 이하)
    max_tokens: int = Field(# TODO)
    
    # 4. 인공지능 창의성 온도 (기본값: 0.7, 0.0 초과 / 1.0 미만)
    # 💡 주의: '이상/이하'가 아닌 '초과/미만' 조건을 사용해야 합니다!
    temperature: float = Field(# TODO)


@app.post("/message")
def create_message(request: MessageRequest):
    return request