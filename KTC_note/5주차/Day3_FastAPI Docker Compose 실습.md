---

## 01. 실습 목표

Day3 실습의 목표는 FastAPI 앱과 MySQL DB를 Docker Compose로 함께 실행하는 것이다. 이전까지는 컨테이너 하나를 직접 실행하는 흐름을 봤다면, 이번에는 웹 서버와 DB 서버를 하나의 애플리케이션 구성으로 묶는다.

```text
[FastAPI container] ---> [MySQL container]
        web                    db
```

여기서 중요한 것은 FastAPI 코드 자체보다 실행 환경이다. 애플리케이션은 `DATABASE_URL` 환경변수를 읽어 DB에 연결하고, Compose는 `web`과 `db` 컨테이너가 같은 네트워크에서 통신할 수 있게 만든다.

---

## 02. docker-compose.yml 구조

FastAPI + MySQL 구성은 보통 다음 형태가 된다.

```yaml
services:
  db:
    image: mysql:8.0
    container_name: todo-db
    environment:
      MYSQL_DATABASE: todo_db
      MYSQL_USER: todo_user
      MYSQL_PASSWORD: todo_pass
      MYSQL_ROOT_PASSWORD: root_pass
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

  web:
    build: .
    container_name: todo-web
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://todo_user:todo_pass@db:3306/todo_db
    depends_on:
      db:
        condition: service_healthy

volumes:
  mysql-data:
```

---

## 03. `db`라는 이름으로 접속할 수 있는 이유

`DATABASE_URL`을 보면 DB host가 `localhost`가 아니라 `db`다.

```text
mysql+pymysql://todo_user:todo_pass@db:3306/todo_db
```

처음에는 이상해 보이지만, Compose 내부에서는 service 이름이 hostname처럼 동작한다. `web` 컨테이너와 `db` 컨테이너가 같은 Compose 네트워크에 있으므로, `web` 컨테이너는 `db:3306`으로 MySQL 컨테이너에 접근할 수 있다.

이때 `localhost`를 쓰면 안 된다. `web` 컨테이너 안에서 `localhost`는 내 컴퓨터가 아니라 `web` 컨테이너 자기 자신을 의미한다.

---

## 04. healthcheck와 depends_on

DB 컨테이너가 “실행됨”과 “접속 가능함”은 다르다. MySQL은 컨테이너가 시작된 뒤에도 초기화 시간이 필요할 수 있다.

`healthcheck`는 컨테이너 내부에서 주기적으로 명령을 실행해 실제 서비스가 준비됐는지 검사한다.

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 5s
  timeout: 3s
  retries: 10
```

`depends_on`의 `condition: service_healthy`를 사용하면 `db`가 healthy 상태가 된 뒤 `web`을 시작할 수 있다.

```yaml
depends_on:
  db:
    condition: service_healthy
```

이 설정은 FastAPI가 DB 준비 전에 먼저 떠서 연결 실패하는 문제를 줄여준다.

---

## 05. 실행과 확인

Compose 실행은 다음 명령으로 한다.

```bash
docker compose up -d --build
```

상태 확인:

```bash
docker compose ps
```

로그 확인:

```bash
docker compose logs -f web
docker compose logs -f db
```

DB 컨테이너 내부에서 직접 SQL을 확인할 수도 있다.

```bash
docker exec -it todo-db mysql -u todo_user -ptodo_pass todo_db
```

MySQL shell 안에서는 다음을 확인한다.

```sql
SHOW TABLES;
SELECT * FROM todos;
SELECT COUNT(*) AS todo_count FROM todos;
```

---

## 06. 자주 헷갈리는 지점

| 상황 | 확인할 것 |
| --- | --- |
| 브라우저에서 FastAPI 접속 안 됨 | `ports` 설정이 있는지 확인 |
| FastAPI가 DB 연결 실패 | `DATABASE_URL`의 host가 `db`인지 확인 |
| DB 데이터가 사라짐 | Volume을 사용하고 있는지 확인 |
| 컨테이너는 켜졌지만 앱이 오류 | `docker compose logs -f web` 확인 |
| DB가 아직 준비되지 않음 | `healthcheck`, `depends_on` 확인 |

---

## 오늘의 정리

FastAPI + MySQL Compose 실습의 핵심은 여러 컨테이너가 하나의 서비스처럼 동작하게 만드는 것이다.

- `web`은 FastAPI 앱 컨테이너다.
- `db`는 MySQL 컨테이너다.
- Compose 네트워크 안에서는 `db`라는 service 이름으로 DB에 접근할 수 있다.
- DB 데이터는 Volume으로 보존한다.
- `healthcheck`와 `depends_on`은 DB 준비 전 앱이 먼저 떠버리는 문제를 줄인다.

> [!note]- 📚 강의 자료 보기
> ![[[수업 자료] Docker Compose]]
