# week05_Docker Compose와 RDS로 배포 환경 감각 잡기

## 🗓 이번 주 개요
- 주차: Week 05
- 키워드: #Docker #Container #Dockerfile #DockerCompose #EnvironmentVariable #Volume #Network #FastAPI #MySQL #RDS #AWS

## 📚 이번 주 학습한 것

### 1. Docker 컨테이너와 가상머신의 차이
- **핵심 개념**: VM은 각 실행 환경이 Guest OS를 포함하는 방식이고, 컨테이너는 Host OS 커널을 공유하면서 애플리케이션 실행 환경만 격리하는 방식이다.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - 지금까지 개발을 하면서 자주 만나는 문제가 “내 컴퓨터에서는 되는데 다른 환경에서는 안 되는” 상황이었다. Docker는 애플리케이션 코드뿐 아니라 실행에 필요한 라이브러리, 설정, 런타임을 이미지로 묶어 이 문제를 줄여주는 도구라고 이해했다.
  - 컨테이너는 완전한 가상 컴퓨터라기보다는 리눅스 커널의 `namespace`, `cgroup`, `chroot` 같은 기능을 조합해서 독립된 서버처럼 보이게 만든 실행 환경이다. `namespace`는 프로세스, 네트워크, 호스트명 같은 세계를 분리하고, `cgroup`은 CPU나 메모리 같은 자원 사용량을 제한한다.
  - VM보다 격리 수준은 낮을 수 있지만, OS 전체를 매번 띄우지 않기 때문에 훨씬 가볍고 빠르다. 그래서 개발 환경을 맞추거나 여러 서비스를 나눠 띄우는 상황에서는 컨테이너가 훨씬 실용적이라는 감이 왔다.

### 2. Docker 기본 명령어와 Dockerfile 흐름
- **핵심 개념**: `docker build`, `docker run`, `docker ps`, `docker exec`, `docker rm` 명령어와 Dockerfile의 기본 역할.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - Docker 이미지는 컨테이너를 실행하기 위한 읽기 전용 템플릿이고, 컨테이너는 그 이미지를 실제로 실행한 상태다. 그래서 `docker build -t my-app .`은 Dockerfile을 읽어 이미지를 만드는 과정이고, `docker run`은 그 이미지를 기반으로 컨테이너를 생성하고 실행하는 과정이다.
  - `docker run -p 8080:80 nginx`에서 `-p` 옵션은 호스트의 8080 포트로 들어온 요청을 컨테이너 내부 80 포트로 넘겨주는 포트 매핑이다. 단순히 컨테이너를 실행했다고 해서 브라우저에서 바로 접속되는 것이 아니라, 외부와 연결할 포트를 명시해야 한다는 점이 중요했다.
  - `docker exec -it <container> bash`는 새 컨테이너를 만드는 것이 아니라 이미 실행 중인 컨테이너 안으로 들어가 작업하는 명령이다. `run`과 `exec`의 차이를 구분하니 실습 중 “새로 띄우는 것”과 “이미 떠 있는 것에 접속하는 것”이 명확해졌다.

### 3. Docker Compose로 FastAPI와 MySQL을 함께 실행하기
- **핵심 개념**: 여러 컨테이너를 `docker-compose.yml` 하나로 정의하고, `services`, `ports`, `environment`, `volumes`, `depends_on`, `healthcheck` 등을 통해 실행 구조를 관리한다.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - 실제 애플리케이션은 보통 웹 서버 하나로 끝나지 않고, FastAPI 서버와 MySQL DB처럼 여러 프로세스가 함께 동작한다. 이들을 하나의 컨테이너에 억지로 넣으면 실행 순서, 로그, 배포, 장애 관리가 복잡해진다. 그래서 기능별로 컨테이너를 나누고 Compose로 묶는 방식이 자연스럽다.
  - `services` 아래에 `web`, `db` 같은 이름을 붙이면 Compose가 같은 네트워크 안에서 이 서비스 이름을 hostname처럼 사용할 수 있게 해준다. Day 2에서 `DATABASE_URL=mysql+pymysql://todo_user:todo_pass@db:3306/todo_db`처럼 `db`로 접속할 수 있었던 이유가 바로 이 Compose 네트워크 덕분이었다.
  - `depends_on`은 실행 순서를 정의하고, `healthcheck`는 DB가 단순히 컨테이너만 켜진 상태가 아니라 실제로 연결 가능한 상태인지 확인하는 역할을 한다. 서버와 DB 조합에서는 “먼저 실행됨”과 “정상적으로 준비됨”이 다르기 때문에 이 차이를 구분해야 한다는 점이 기억에 남았다.

### 4. 환경변수, 볼륨, 네트워크가 배포 환경에서 중요한 이유
- **핵심 개념**: 환경변수는 실행 환경별 설정을 분리하고, 볼륨은 컨테이너 데이터의 영속성을 보장하며, 네트워크는 컨테이너 간 통신 방식을 결정한다.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - 컨테이너는 삭제되면 내부에 저장된 데이터도 사라질 수 있다. MySQL 컨테이너를 그냥 띄우기만 하면 컨테이너 삭제와 함께 DB 데이터가 날아갈 수 있으므로, 유지해야 하는 데이터는 Volume이나 Bind Mount를 통해 컨테이너 바깥에 보관해야 한다.
  - Bind Mount는 내가 지정한 호스트 디렉토리를 컨테이너에 직접 연결하는 방식이라 개발 중 소스코드를 실시간으로 공유할 때 유용하다. 반면 Volume은 Docker가 관리하는 저장 공간을 사용하는 방식이라 DB 파일이나 로그처럼 Docker 안에서 안정적으로 관리할 데이터에 더 적합하다고 이해했다.
  - 네트워크에서는 기본 bridge와 사용자 정의 bridge의 차이가 중요했다. 기본 bridge에서는 IP로는 통신할 수 있지만 컨테이너 이름 기반 DNS 통신이 제한될 수 있고, 사용자 정의 네트워크에서는 같은 네트워크 안의 컨테이너끼리 이름으로 통신할 수 있다. Compose가 여러 서비스를 편하게 연결해주는 이유도 이 네트워크 추상화와 연결된다.

### 5. 로컬 MySQL 컨테이너에서 AWS RDS MySQL로 연결 대상 바꾸기
- **핵심 개념**: FastAPI 앱 코드를 크게 바꾸지 않고 `DATABASE_URL` 환경변수만 변경하여 로컬 MySQL 컨테이너 대신 AWS RDS MySQL에 연결한다.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - Day 2 구조에서는 FastAPI 컨테이너가 Compose 내부의 `db:3306`으로 MySQL 컨테이너에 접속했다. Week 05 실습에서는 이 `db` 자리에 RDS endpoint를 넣어, DB 위치만 로컬 컨테이너에서 클라우드 관리형 DB로 바꿨다.
  - RDS 연결에는 endpoint, port, database name, username, password, security group이 모두 맞아야 한다. 특히 endpoint와 DB 계정 정보가 맞아도 보안 그룹에서 3306 포트를 허용하지 않으면 `connection timed out`이 발생할 수 있다. DB 연결은 코드만의 문제가 아니라 네트워크 접근 제어까지 포함한다는 점이 확실히 와닿았다.
  - 데이터 확인 방식도 달라졌다. 로컬 DB 컨테이너는 `docker exec -it todo-db mysql ...`로 들어갈 수 있지만, RDS는 내 Compose 안의 컨테이너가 아니기 때문에 `docker run --rm -it mysql:8.0 mysql -h <rds-endpoint> ...`처럼 MySQL client 컨테이너를 잠깐 띄워 접속해야 했다.

## 🧱 막혔던 지점 & 해결 과정

### 1. Compose 내부 hostname `db`와 RDS endpoint의 차이가 처음에는 헷갈림
- **문제 상황**: Day 2에서는 `DATABASE_URL` 안의 host가 `db`였고, Week 05 RDS 실습에서는 host가 긴 RDS endpoint로 바뀌었다. 처음에는 둘 다 DB 주소처럼 보이는데 왜 하나는 짧은 이름이고 하나는 외부 주소인지 헷갈렸다.
- **시도한 방법**:
  * `docker-compose.yml`의 `services` 구조를 다시 확인했다.
  * `web` 서비스와 `db` 서비스가 같은 Compose 네트워크에 있고, Compose가 service 이름을 DNS 이름처럼 해석해준다는 점을 정리했다.
  * RDS는 내 Compose 네트워크 안에 있는 서비스가 아니라 AWS 쪽에 존재하는 외부 DB이므로, 실제 endpoint 주소와 보안 그룹 설정이 필요하다고 구분했다.
- **최종 해결 및 왜 그 해결책이 작동하는가**:
  * `db`는 Docker Compose 내부에서만 통하는 서비스 이름이고, RDS endpoint는 외부 네트워크에서 접근하는 실제 DB 주소라는 기준으로 나누니 이해가 됐다.
  * 결국 `DATABASE_URL`은 같은 형식이지만 host 부분이 가리키는 대상이 바뀐 것이다. 애플리케이션은 환경변수만 읽기 때문에 코드 변경 없이도 로컬 DB와 클라우드 DB를 전환할 수 있다.

### 2. 데이터가 어디에 저장되는지 추적하는 감각이 부족했음
- **문제 상황**: 컨테이너를 띄우면 DB도 같이 생기고 데이터도 저장되니, 처음에는 데이터가 컨테이너 내부에 있는지, 볼륨에 있는지, RDS에 있는지 구분이 흐릿했다.
- **시도한 방법**:
  * 로컬 MySQL 컨테이너에서는 `docker exec`로 접속해 `SHOW TABLES;`, `SELECT * FROM todos;`, `SELECT COUNT(*) AS todo_count FROM todos;`를 실행하는 흐름을 복습했다.
  * RDS 실습에서는 MySQL client 컨테이너를 별도로 띄워 `SELECT DATABASE();`, `SELECT CURRENT_USER();`, `SHOW TABLES;`로 실제 접속 대상이 어디인지 확인했다.
- **최종 해결 및 왜 그 해결책이 작동하는가**:
  * 애플리케이션에서 todo를 생성한 뒤 SQL로 직접 조회해보니, “화면에서 보이는 데이터”와 “DB에 실제 저장된 데이터”가 연결되는 흐름이 분명해졌다.
  * 특히 RDS로 바꾼 뒤에도 같은 FastAPI 앱이 동작한다는 점을 보며, 애플리케이션 코드는 DB 연결 설정에 의존하고 실제 데이터 위치는 환경변수와 네트워크 설정이 결정한다는 점을 이해했다.

### 3. 배포 환경에서는 민감정보 관리가 더 중요해짐
- **문제 상황**: RDS 연결 문자열에는 username, password, endpoint, database name이 한 줄에 모두 들어간다. 실습을 따라가다 보면 편의상 값을 그대로 복사하게 되는데, 이 값이 GitHub나 공개 채팅방에 올라가면 문제가 될 수 있다.
- **시도한 방법**:
  * `.env.example`을 `.env`로 복사하고, 실제 비밀번호와 endpoint는 `.env`에만 넣는 흐름으로 정리했다.
  * 학습일지에는 실제 endpoint나 password를 적지 않고 `<rds-endpoint>`, `<password>` 같은 placeholder만 남기는 방식으로 작성했다.
- **최종 해결 및 왜 그 해결책이 작동하는가**:
  * 코드에는 설정값을 직접 박아 넣지 않고, 실행 환경에서 환경변수로 주입하는 방식이 안전하다.
  * 특히 RDS는 로컬 실습 DB보다 운영 환경에 가까우므로, 보안 그룹과 DB 계정, 비밀번호 관리까지 개발자가 신경 써야 한다는 점을 배웠다.

## 🔁 이번 주 회고 (KPT)
- **Keep** 유지하고 싶은 습관: 개념을 명령어 단위로만 외우지 않고, “왜 이 명령어가 필요한가”를 실행 흐름과 연결해서 정리한 점. `docker run`, `exec`, `compose up`, `compose logs`, `docker run mysql:8.0 mysql ...` 같은 명령어가 각각 어느 상황에서 쓰이는지 구분하려고 한 점은 계속 유지하고 싶다.
- **Problem** 아쉬웠던 점: Docker는 명령어가 많고 옵션도 비슷해서 처음에는 암기 과목처럼 느껴졌다. 특히 포트 매핑, 볼륨, 네트워크, 환경변수가 동시에 등장하면 어느 부분에서 문제가 난 것인지 바로 판단하기 어려웠다. RDS 연결도 단순히 URL만 바꾸는 실습처럼 보였지만, 실제로는 보안 그룹, DB 계정, 포트, DB 이름이 모두 맞아야 해서 확인할 지점이 많았다.
- **Try** 다음 주에 시도할 것: 문제가 생겼을 때 무작정 재실행하기보다 `docker compose ps`로 상태 확인, `docker compose logs -f web`으로 로그 확인, DB client로 직접 SQL 조회, 환경변수 값 확인 순서로 디버깅 루틴을 정해두기. Docker 관련 에러는 “컨테이너가 떠 있는가 → 포트가 연결됐는가 → 네트워크 이름이 맞는가 → 환경변수가 적용됐는가 → DB가 실제로 응답하는가” 순서로 점검해보고 싶다.

## 🎯 다음 주 목표
- [ ] `docker-compose.yml`에서 `services`, `environment`, `ports`, `volumes`, `depends_on` 역할을 코드 없이 설명할 수 있을 정도로 복습하기
- [ ] FastAPI + MySQL Compose 실습을 한 번 더 실행하면서 로컬 DB와 RDS DB 연결 차이를 직접 비교하기
- [ ] Docker 로그와 DB SQL 조회를 함께 사용해 데이터 저장 문제를 디버깅하는 연습하기
- [ ] 환경변수와 민감정보를 GitHub에 올리지 않는 습관을 `.env`, `.env.example`, `.gitignore` 기준으로 정리하기

---

## 🔗 관련 GitHub 저장소 링크
- [5주차 학습 노트](../../notes/5주차)
