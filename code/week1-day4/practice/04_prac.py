from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

# 1. 공통 모델 정의
class PostBase(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    content: str = Field(min_length=5)
    is_anonymous: bool = True

# 2. 요청 모델 (상속 + IP 추가)
class PostCreate(PostBase):
    author_ip: str

# 3. 응답 모델 (상속 + id, 시간 추가 / IP는 제외)
class PostResponse(PostBase):
    id: int
    created_at: datetime

# 4. 엔드포인트 완성
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    # 사용자가 보낸 데이터에 서버 정보를 추가한 딕셔너리
    db_data = {
        "id": 101,
        "title": post.title,
        "content": post.content,
        "is_anonymous": post.is_anonymous,
        "author_ip": post.author_ip, # PostResponse에 없으므로 자동 필터링됨
        "created_at": datetime.now()
    }
    return db_data
