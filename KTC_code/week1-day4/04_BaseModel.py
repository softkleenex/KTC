from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class MessageRequest(BaseModel):
    user_id: int
    content: str = Field(min_length=1, max_length=5)   # 1~5자
    max_tokens: int = Field(default=500, ge=1, le=2000)  # 1~2000 사이만 허용

@app.post("/message")
def create_message(request: MessageRequest):
    return request