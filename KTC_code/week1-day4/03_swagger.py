from fastapi import FastAPI
from pydantic import BaseModel

# 문서의 제목과 버전을 명시할 수 있습니다.
app = FastAPI(title="카카오 AI API", version="0.1.0")

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    sentiment: str
    confidence: float

@app.post("/ai/analyze", response_model=AnalyzeResponse)
def analyze_sentiment(request: AnalyzeRequest):
    positive_words = ["행복", "좋아", "최고", "감사"]
    is_positive = any(word in request.text for word in positive_words)

    return AnalyzeResponse(
        sentiment="positive" if is_positive else "neutral",
        confidence=0.95 if is_positive else 0.6,
    )
    # POST {"text": "오늘 너무 행복하다"}
    # → {"sentiment": "positive", "confidence": 0.95}
