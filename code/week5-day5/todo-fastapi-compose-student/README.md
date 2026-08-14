# Day 4 — FastAPI + RDS 실습 코드

이 폴더는 Day 2 정답 코드를 Day 4 실습 출발점으로 정리한 학생용 자료입니다.

Day 4의 목표는 Docker Compose를 처음부터 작성하는 것이 아니라, 이미 동작하는 FastAPI 앱의 DB 연결 대상을 로컬 MySQL 컨테이너에서 AWS RDS MySQL로 바꾸는 것입니다.

## 1. 로컬 DB로 먼저 실행

```bash
docker compose up -d
docker compose ps
```

브라우저에서 접속합니다.

```text
http://localhost:8000
```

로컬 MySQL 컨테이너에서 데이터 확인:

```bash
docker exec -it todo-db mysql -u todo_user -ptodo_pass todo_db
```

```sql
SHOW TABLES;
SELECT * FROM todos;
EXIT;
```

## 2. RDS 연결로 바꾸기

`.env.example`을 참고해서 `.env` 파일을 만들고, `DATABASE_URL`을 강사가 제공한 RDS 값으로 바꿉니다.

```env
DATABASE_URL=mysql+pymysql://ktc_001:<password>@<rds-endpoint>:3306/ktc_001_db
```

컨테이너 재실행:

```bash
docker compose down
docker compose up -d --build web
docker compose logs -f web
```

## 3. RDS에서 SELECT 확인

Windows PowerShell:

```powershell
docker run --rm -it mysql:8.0 mysql -h <rds-endpoint> -P 3306 -u ktc_001 -p ktc_001_db
```

macOS/Linux:

```bash
docker run --rm -it mysql:8.0 mysql \
  -h <rds-endpoint> \
  -P 3306 \
  -u ktc_001 \
  -p \
  ktc_001_db
```

MySQL shell:

```sql
SELECT DATABASE();
SELECT CURRENT_USER();
SHOW TABLES;
SELECT * FROM todos;
EXIT;
```

## 주의

- `.env` 파일에는 비밀번호가 들어가므로 GitHub에 올리지 않습니다.
- RDS endpoint와 password를 공개 채팅방에 남기지 않습니다.
- 수업 후 강사의 안내에 따라 계정 접근이 회수될 수 있습니다.
