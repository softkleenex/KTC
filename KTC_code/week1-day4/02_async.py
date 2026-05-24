import asyncio
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

async def call_ai_api(message: str) -> str:
    await asyncio.sleep(3)  # AI API 호출 시뮬레이션 (3초 대기)
    return f"AI 답변: {message}에 대한 응답"


@app.post("/chat")
async def chat(request: ChatRequest):
    # 요청이 서버에 들어온 딱 그 순간의 시간(초) 기록
    start_time = datetime.now().strftime("%H시 %M분 %S초")

    # 3초 동안 대기하며 AI 응답을 받아옵니다.
    response = await call_ai_api(request.message)

    # 처리가 완전히 끝난 순간의 시간 기록
    end_time = datetime.now().strftime("%H시 %M분 %S초")

    return {
        "start_time": start_time,
        "end_time": end_time,
        "response": response
    }


import asyncio
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

async def call_ai_api(message: str) -> str:
    await asyncio.sleep(3)  # AI API 호출 시뮬레이션 (3초 대기)
    return f"AI 답변: {message}에 대한 응답"


@app.post("/chat")
async def chat(request: ChatRequest):
    # 요청이 서버에 들어온 순간의 시간(초) 기록
    start_time = datetime.now().strftime("%H시 %M분 %S초")

    # 3초 동안 대기하며 AI 응답을 받아옵니다.
    response = await call_ai_api(request.message)

    # 처리가 완전히 끝난 순간의 시간 기록
    end_time = datetime.now().strftime("%H시 %M분 %S초")

    return {
        "start_time": start_time,
        "end_time": end_time,
        "response": response
    }
