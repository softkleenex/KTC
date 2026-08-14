---

## 01. 환경변수

환경변수는 프로세스가 실행될 때 참조하는 값이다. 서버 포트, DB 주소, 비밀번호, 실행 모드처럼 환경에 따라 달라지는 값을 코드에 직접 넣지 않고 외부에서 주입할 때 사용한다.

Docker에서는 여러 시점에 환경변수를 정의할 수 있다.

| 방식 | 시점 | 예시 |
| --- | --- | --- |
| `ENV` | 이미지 빌드 및 컨테이너 실행 시 기본값 | Dockerfile |
| `ARG` | 이미지 빌드 시점 | `docker build --build-arg` |
| `-e` | 컨테이너 실행 시점 | `docker run -e KEY=value` |
| `--env-file` | 컨테이너 실행 시점 | `.env` 파일 |

이미지 빌드 시점에만 필요한 값은 `ARG`, 컨테이너 실행 중 애플리케이션이 읽어야 하는 값은 `ENV`나 실행 시점 환경변수로 주입하는 것이 자연스럽다.

---

## 02. 컨테이너 데이터의 휘발성

컨테이너 내부에 저장한 데이터는 컨테이너가 삭제되면 함께 사라질 수 있다. MySQL 컨테이너를 띄웠는데 데이터를 컨테이너 내부에만 저장하면, 컨테이너 삭제와 함께 DB 데이터도 잃을 수 있다.

그래서 유지해야 하는 데이터는 컨테이너 바깥에 저장해야 한다. 이를 데이터 영속화라고 한다.

---

## 03. Volume과 Bind Mount

Docker에서 데이터를 영속화하는 대표 방식은 Volume과 Bind Mount다.

| 구분 | Bind Mount | Volume |
| --- | --- | --- |
| 저장 위치 | 사용자가 지정한 호스트 경로 | Docker가 관리하는 저장소 |
| 관리 주체 | 사용자 | Docker |
| 접근성 | Finder/탐색기에서 바로 접근 가능 | Docker 명령을 통해 관리 |
| 주요 용도 | 소스코드 공유, 개발 중 실시간 반영 | DB 데이터, 로그, 설정값 보존 |

개발 중 코드 변경을 컨테이너에 바로 반영하려면 Bind Mount가 편하다. 반면 MySQL 데이터처럼 Docker가 안정적으로 관리해야 하는 데이터는 Volume이 더 적합하다.

```bash
docker run -v my-volume:/var/lib/mysql mysql:8.0
```

위 예시는 `my-volume`이라는 Docker volume을 컨테이너의 `/var/lib/mysql`에 연결한다.

---

## 04. Docker Network

컨테이너는 기본적으로 격리되어 있다. 여러 컨테이너가 서로 통신하려면 네트워크가 필요하다.

Docker의 기본 bridge 네트워크에서는 IP 주소로 컨테이너 간 통신이 가능하다. 하지만 컨테이너 이름으로 통신하려면 사용자 정의 bridge 네트워크를 사용하는 것이 좋다.

```bash
docker network create app-network

docker run -d --name web1 --network app-network nginx
docker run -d --name web2 --network app-network nginx
```

같은 사용자 정의 네트워크에 연결된 컨테이너들은 이름을 DNS처럼 사용할 수 있다.

```text
web1 컨테이너 → web2:80 으로 접근 가능
```

이 개념이 Docker Compose에서 `db`라는 서비스 이름으로 MySQL에 접속할 수 있었던 이유와 연결된다.

---

## 05. 다중 컨테이너

실제 애플리케이션은 보통 하나의 프로세스로 끝나지 않는다.

```text
Frontend 컨테이너
Backend 컨테이너
Database 컨테이너
```

이렇게 기능별로 컨테이너를 나누면 실행 주기, 배포, 확장, 장애 대응을 독립적으로 관리할 수 있다. API 서버만 부하가 높으면 API 서버 컨테이너만 늘릴 수 있고, DB는 별도의 데이터 저장 정책을 둘 수 있다.

---

## 06. Docker Compose

여러 컨테이너를 `docker run` 명령어로 하나씩 실행하면 옵션이 길어지고 공유하기 어렵다. Docker Compose는 여러 컨테이너 실행 구성을 하나의 YAML 파일로 정의하게 해준다.

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://todo_user:todo_pass@db:3306/todo_db
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: todo_db
      MYSQL_USER: todo_user
      MYSQL_PASSWORD: todo_pass
      MYSQL_ROOT_PASSWORD: root_pass
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

Compose에서 중요한 속성은 다음과 같다.

| 속성 | 역할 |
| --- | --- |
| `services` | 실행할 컨테이너 묶음 정의 |
| `build` | Dockerfile 기반 이미지 빌드 |
| `image` | 사용할 이미지 지정 |
| `ports` | 호스트 포트와 컨테이너 포트 연결 |
| `environment` | 컨테이너 환경변수 주입 |
| `volumes` | 데이터 영속화 또는 파일 공유 |
| `depends_on` | 서비스 간 실행 순서 정의 |
| `healthcheck` | 컨테이너가 실제로 준비됐는지 검사 |

---

## 07. Compose 기본 명령어

```bash
docker compose up -d
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose exec db bash
docker compose down
docker compose down -v
```

`up -d`는 백그라운드 실행, `--build`는 이미지를 새로 빌드한 뒤 실행한다. `down`은 컨테이너와 네트워크를 내리고, `down -v`는 볼륨까지 삭제하므로 DB 데이터를 지울 수 있어 주의해야 한다.

---

## 오늘의 정리

- 환경변수는 실행 환경마다 달라지는 값을 코드 밖에서 주입하는 방법이다.
- 컨테이너 내부 데이터는 휘발될 수 있으므로 Volume이나 Bind Mount로 영속화해야 한다.
- 사용자 정의 네트워크에서는 컨테이너 이름으로 통신할 수 있다.
- Docker Compose는 다중 컨테이너 구성을 YAML 파일 하나로 관리한다.
- DB가 있는 Compose 구성에서는 `depends_on`과 `healthcheck`로 준비 상태를 확인하는 것이 중요하다.

> [!note]- 📚 강의 자료 보기
> ![[[수업 자료] Docker Compose]]
