---

## 01. 실습 목표

Day4의 목표는 로컬 MySQL 컨테이너 대신 AWS RDS MySQL에 FastAPI 앱을 연결하는 것이다.

Day3까지의 구조는 다음과 같았다.

```text
[FastAPI container] ---> [MySQL container]
        web                    db
```

Day4에서는 DB 위치만 바뀐다.

```text
[FastAPI container] ---> [AWS RDS MySQL]
        web                    <rds-endpoint>:3306
```

핵심은 코드를 갈아엎는 것이 아니라 `DATABASE_URL` 환경변수가 가리키는 DB 주소를 바꾸는 것이다.

---

## 02. RDS 연결에 필요한 값

RDS MySQL에 연결하려면 다음 값이 필요하다.

| 값 | 의미 | 예시 |
| --- | --- | --- |
| endpoint | RDS 접속 주소 | `xxxx.ap-northeast-2.rds.amazonaws.com` |
| port | MySQL 포트 | `3306` |
| database name | 사용할 DB 이름 | `ktc_001_db` |
| username | DB 사용자 | `ktc_001` |
| password | DB 비밀번호 | 제공된 임시 비밀번호 |
| security group | 네트워크 접근 제어 | 3306 허용 규칙 |

연결 문자열은 다음 형식이다.

```text
mysql+pymysql://<username>:<password>@<rds-endpoint>:3306/<database-name>
```

비밀번호와 endpoint는 민감정보다. GitHub, 블로그, 공개 채팅방에 그대로 올리면 안 된다.

---

## 03. 로컬 DB와 RDS DB의 차이

Day3에서 `db`는 Docker Compose 안의 service 이름이었다.

```text
mysql+pymysql://todo_user:todo_pass@db:3306/todo_db
```

`web` 컨테이너와 `db` 컨테이너가 같은 Compose 네트워크 안에 있었기 때문에 `db`라는 이름으로 접속할 수 있었다.

RDS는 내 Compose 네트워크 안에 있는 컨테이너가 아니다. AWS에 있는 외부 DB이므로 실제 RDS endpoint를 사용해야 한다.

```text
mysql+pymysql://ktc_001:<password>@<rds-endpoint>:3306/ktc_001_db
```

즉, 연결 문자열의 형식은 같지만 host 부분이 `db`에서 `<rds-endpoint>`로 바뀐다.

---

## 04. .env로 DATABASE_URL 바꾸기

실제 비밀번호가 들어간 값은 코드에 직접 쓰지 않고 `.env`에 둔다.

```bash
cp .env.example .env
```

기존 값:

```env
DATABASE_URL=mysql+pymysql://todo_user:todo_pass@db:3306/todo_db
```

RDS 연결 값:

```env
DATABASE_URL=mysql+pymysql://ktc_001:<password>@<rds-endpoint>:3306/ktc_001_db
```

확인할 것:

- username이 본인 계정인지
- password가 정확한지
- endpoint를 빠뜨리지 않았는지
- `:3306` 포트가 있는지
- 마지막 database name이 맞는지
- 공백이 섞이지 않았는지

---

## 05. 앱 컨테이너 재실행

환경변수를 바꿨다면 컨테이너를 다시 실행해야 한다.

```bash
docker compose down
docker compose up -d --build web
docker compose logs -f web
```

`web`만 실행하기 어렵다면 전체를 다시 올린다.

```bash
docker compose up -d --build
docker compose logs -f web
```

로그에서 DB 연결 오류가 없는지 확인한다. 연결이 실패하면 대부분 endpoint, username/password, database name, security group 중 하나가 원인이다.

---

## 06. MySQL client 컨테이너로 RDS 접속하기

RDS는 로컬 `todo-db` 컨테이너가 아니므로 `docker exec todo-db`로 들어갈 수 없다. 대신 MySQL client가 들어있는 컨테이너를 잠깐 실행해 RDS에 접속한다.

```bash
docker run --rm -it mysql:8.0 mysql \
  -h <rds-endpoint> \
  -P 3306 \
  -u ktc_001 \
  -p \
  ktc_001_db
```

접속 후 확인:

```sql
SELECT DATABASE();
SELECT CURRENT_USER();
SHOW TABLES;
SELECT * FROM todos;
SELECT COUNT(*) AS todo_count FROM todos;
```

FastAPI에서 생성한 todo가 SQL 조회 결과에도 보이면 앱이 RDS에 정상 저장하고 있다는 뜻이다.

---

## 07. 자주 만나는 에러

| 에러 | 흔한 원인 | 확인할 것 |
| --- | --- | --- |
| `connection timed out` | 보안 그룹에서 3306 미허용 | RDS security group |
| `Access denied` | 계정 또는 비밀번호 오류 | username/password |
| `Unknown database` | DB 이름 오타 | database name |
| `Unknown MySQL server host` | endpoint 오타 | RDS endpoint |
| 계속 로컬 DB에 저장됨 | 환경변수 변경 미적용 | 컨테이너 재실행 |
| `mysql` 명령어 없음 | web 컨테이너에 MySQL CLI 없음 | MySQL client 컨테이너 사용 |

---

## 오늘의 정리

Day4의 핵심은 애플리케이션 코드보다 실행 환경이다.

- 로컬 Compose DB는 `db:3306`으로 접근한다.
- RDS는 `<rds-endpoint>:3306`으로 접근한다.
- `DATABASE_URL`만 바꿔도 같은 FastAPI 앱이 다른 DB에 연결된다.
- RDS 연결은 DB 계정뿐 아니라 security group 같은 네트워크 설정도 맞아야 한다.
- 실제 저장 여부는 FastAPI 화면만 보지 말고 SQL로 직접 확인해야 한다.

> 애플리케이션은 환경변수만 바꿔도 다른 DB에 연결할 수 있고, 운영 환경에서는 그 연결을 계정과 네트워크로 통제한다.

> [!note]- 📚 강의 자료 보기
> ![[22. 클라우드 DB 연동]]
