FROM python:3.11-slim

WORKDIR /app

# 백엔드 컨테이너는 FastAPI API 서버만 실행합니다.
# 프론트엔드 정적 파일은 Dockerfile에 복사하지 않고,
# docker-compose.yml에서 Nginx 컨테이너에 ./static 폴더를 마운트합니다.

# 의존성 먼저 복사하면 requirements.txt가 바뀌지 않는 한 pip install 레이어를 재사용할 수 있습니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 백엔드 실행에 필요한 파일만 복사합니다.
# 이렇게 분리하면 "API 서버"와 "프론트엔드 서버"의 역할 차이가 더 잘 보입니다.
COPY database.py .
COPY main.py .
COPY models.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
