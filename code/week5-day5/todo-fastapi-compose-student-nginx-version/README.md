# Day 4 확장 실습 - Nginx frontend + FastAPI backend

이 폴더는 기본 Day4 실습이 일찍 끝났을 때 사용할 수 있는 확장 버전입니다.
기본 버전은 FastAPI가 `index.html`까지 직접 내려주지만, 이 버전은 역할을 분리합니다.

- `frontend`: Nginx가 HTML/CSS/JS 정적 파일을 배포합니다.
- `backend`: FastAPI가 `/api` JSON API만 제공합니다.
- `db`: MySQL 컨테이너입니다. RDS로 전환하면 이 컨테이너 대신 AWS RDS를 바라보게 됩니다.

## 구조

```text
browser
  -> http://localhost:8080
  -> nginx frontend
      -> static/index.html, static/style.css, static/script.js
      -> /api/* proxy
          -> fastapi backend:8000
              -> MySQL db or AWS RDS
```

## 실행

```bash
docker compose up --build
```

브라우저 접속:

```text
http://localhost:8080
```

FastAPI API 직접 확인:

```text
http://localhost:8000/api/health
http://localhost:8000/api/todos
```

Nginx 프록시 경유 확인:

```text
http://localhost:8080/api/health
http://localhost:8080/api/todos
```

## 파일별 역할

| 파일 | 역할 |
| --- | --- |
| `docker-compose.yml` | `db`, `backend`, `frontend` 세 컨테이너를 묶어 실행합니다. |
| `Dockerfile` | FastAPI 백엔드 이미지를 만듭니다. 정적 파일은 복사하지 않습니다. |
| `nginx.conf` | `/`는 정적 파일, `/api/`는 FastAPI로 프록시합니다. |
| `main.py` | FastAPI API 서버입니다. HTML 렌더링 라우트는 없습니다. |
| `static/` | Nginx가 배포하는 프론트엔드 파일입니다. |
| `.env.example` | 로컬 DB 또는 RDS 접속 문자열 예시입니다. |

## RDS로 전환하기

1. `.env.example`을 `.env`로 복사합니다.
2. `DATABASE_URL`을 강사가 제공한 RDS 값으로 바꿉니다.
3. 컨테이너를 다시 시작합니다.

```bash
docker compose down
docker compose up --build
```

예시:

```env
DATABASE_URL=mysql+pymysql://ktc_001:<password>@<rds-endpoint>:3306/ktc_001_db
```

주의할 점:

- RDS 보안 그룹에서 TCP 3306 인바운드가 열려 있어야 합니다.
- Docker Compose 내부 MySQL을 쓸 때는 host가 `db`입니다.
- RDS를 쓸 때는 host가 `<rds-endpoint>`입니다.
- `.env` 파일에는 비밀번호가 들어가므로 Git에 올리지 않습니다.

## 왜 CORS를 열어두나요?

수업 중에는 다음처럼 접속 경로가 자주 바뀔 수 있습니다.

- `localhost:8080`에서 Nginx로 접속
- `localhost:8000`에서 FastAPI 직접 확인
- 학생별 PC, 포트, 네트워크 환경 차이

그래서 `main.py`에서는 실습이 CORS 때문에 막히지 않도록 모든 Origin, Method, Header를 허용합니다.
운영 환경에서는 실제 프론트엔드 도메인만 허용하도록 줄여야 합니다.

## 수업에서 설명할 핵심 문장

- FastAPI는 이제 화면을 렌더링하지 않고 API만 제공합니다.
- Nginx는 정적 파일을 빠르게 배포하고 `/api` 요청을 백엔드로 넘깁니다.
- 브라우저는 backend라는 컨테이너 이름을 모릅니다. backend 이름은 Nginx 컨테이너가 Docker Compose 네트워크 안에서 사용하는 이름입니다.
- RDS 전환의 핵심은 코드를 바꾸는 것이 아니라 `DATABASE_URL`의 host를 바꾸는 것입니다.
