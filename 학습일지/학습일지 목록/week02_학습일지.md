# week02 데이터의 영구 저장(SQL)부터 화면(HTML/CSS/JS)까지의 여정

## 🗓 이번 주 개요
- 주차: Week 02 (5/25~5/29)
- 키워드: #SQL #Database #SQLite #FastAPI #Pydantic #HTML #CSS #JavaScript

## 📚 이번 주 학습한 것

### 1. SQL과 DML 및 관계형 데이터베이스 기초
- **핵심 개념**: 관계형 데이터베이스(RDBMS)의 설계, Primary Key(기본키)와 Foreign Key(외래키)를 이용한 테이블 관계(1:N) 구성, 그리고 SQL을 통한 데이터 조회 및 조작.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - **HAVING과 WHERE의 실행 순서 차이**: 쿼리 실행 시 `WHERE`는 그룹화(`GROUP BY`)를 하기 전에 개별 행들을 먼저 필터링합니다. 반면 `HAVING`은 그룹화가 완료된 결과(집계된 데이터)에 대해 필터링을 수행합니다. 데이터베이스 엔진 관점에서는 **불필요한 데이터를 그룹화하기 전에 `WHERE`로 먼저 쳐내는 것이 메모리와 연산량 측면에서 훨씬 효율적**이기 때문에 이 순서로 동작합니다. 따라서 `COUNT()`, `SUM()` 같은 집계 함수는 `WHERE` 절에 사용할 수 없고, 반드시 `HAVING` 절에 사용해야 합니다.
  - **LEFT JOIN에서 NULL이 발생하는 이유**: `INNER JOIN`은 양쪽 테이블 모두에 매칭되는 데이터가 있을 때만 결과 행을 반환합니다. 하지만 `LEFT JOIN`은 왼쪽 테이블을 기준으로 삼고 오른쪽 테이블에 매칭되는 행이 없더라도 왼쪽 행을 유지합니다. 이때 오른쪽 테이블의 값들은 존재하지 않으므로 **데이터베이스 엔진이 빈 자리를 `NULL`로 채워 일관된 테이블 구조를 유지**해 줍니다. 이 특성을 이용하면 `WHERE messages.id IS NULL`과 같은 조건으로 '아직 메시지를 하나도 쓰지 않은 사용자 목록' 등을 쉽게 찾아낼 수 있습니다.
- **관련 코드/링크**:
  ```sql
  -- users 테이블과 messages 테이블을 LEFT JOIN하여 메시지가 없는 유저까지 포함해 조회
  SELECT users.username, messages.content
  FROM users
  LEFT JOIN messages ON users.id = messages.user_id;
  ```

### 2. FastAPI와 SQLite DB 연동 및 Pydantic 데이터 검증
- **핵심 개념**: 경량 관계형 DB인 SQLite를 Python 내장 `sqlite3` 라이브러리를 통해 FastAPI에 연동하고, Pydantic 모델을 이용하여 API 입출력 데이터를 안전하게 검증하고 구조화하는 방법.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - **SQL 인젝션 예방과 플레이스홀더(`?`)**: SQL 인젝션은 사용자의 입력값이 SQL 명령어로 해석되어 쿼리 구조가 변조되는 공격입니다. f-string 등을 사용해 동적으로 쿼리 문자열을 조립하면 입력값과 명령어가 결합되지만, `?` 플레이스홀더를 사용하면 데이터베이스가 **먼저 쿼리의 구조(Syntax)를 컴파일(구문 분석)한 뒤, 전달된 파라미터는 순수한 데이터 값(Literal)으로만 바인딩**합니다. 따라서 입력값에 악성 SQL 구문이 포함되어 있더라도 단순한 문자열 데이터로 취급되므로 안전합니다.
  - **Request와 Response DTO(BaseModel)의 분리**: 데이터 생성 시 클라이언트가 보낸 데이터와 실제 DB에 저장된 후 돌려주는 데이터의 생명주기와 형태는 다릅니다. 예컨대 생성할 때는 ID가 없지만(DB가 Auto-increment로 생성하므로), 응답할 때는 생성된 ID를 포함해야 합니다. 하나의 모델을 공용으로 쓰면 불필요한 필드가 노출되거나 클라이언트가 악의적으로 ID를 지정해 보내는 보안 취약점이 생길 수 있어, **입력 검증용(Request) 모델과 출력 포맷팅용(Response) 모델을 철저히 분리하여 데이터의 정합성과 보안을 강화**합니다.
- **관련 코드/링크**:
  ```python
  @app.post("/messages", response_model=MessageResponse)
  def create_message(request: MessageRequest):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO messages (user_id, content) VALUES (?, ?)",
          (request.user_id, request.content)
      )
      conn.commit()
      new_id = cursor.lastrowid
      conn.close()
      return {"id": new_id, "user_id": request.user_id, "content": request.content, "status": "saved"}
  ```

### 3. 웹 프론트엔드의 기초: HTML, CSS & JavaScript
- **핵심 개념**: 웹페이지의 구조를 구성하는 HTML, 스타일링을 입히는 CSS, 그리고 동적인 동작을 부여하는 JavaScript의 기초.
- **내가 이해한 방식 (왜 그렇게 동작하는가)**:
  - **Semantic HTML을 써야 하는 실질적 이유**: 브라우저나 검색엔진 봇은 단순 `<div>`만으로는 해당 영역이 상단 헤더인지 하단 카피라이트인지 구분하지 못합니다. `<header>`, `<main>`, `<nav>` 같은 의미론적 태그를 사용하면 **HTML 문서 자체가 구조화된 의미 정보(Metadata)를 제공하므로 검색엔진의 크롤링 및 인덱싱 효율(SEO)이 극대화**되고, 스크린 리더 등 웹 접근성 도구의 동작 신뢰성도 올라갑니다.
  - **JavaScript에서 빈 배열(`[]`)과 빈 객체(`{}`)가 Truthy인 이유**: 자바스크립트의 조건문 평가에서 Falsy 값(`false`, `0`, `""`, `null`, `undefined`, `NaN`)을 제외한 모든 것은 Truthy로 취급됩니다. 빈 배열과 객체는 비어 있을지라도 **메모리상의 특정 주소를 가리키는 유효한 참조형(Reference) 객체**이기 때문에 평가 시 참(Truthy)으로 해석됩니다. 따라서 배열이 비었는지 판단하려면 단순히 `if (arr)`로 검증하면 안 되고, 반드시 `arr.length === 0`처럼 배열의 속성을 직접 확인해야 의도한 대로 동작합니다.

## 🧱 막혔던 지점 & 해결 과정

### 1. SQLite 쿼리에 단일 변수 바인딩 시 튜플 문법 오류
- **문제 상황**: sqlite3를 사용할 때 단일 변수를 파라미터로 넘겼으나 `Incorrect number of bindings supplied` 또는 `ValueError` 계열의 오류가 반복 발생함.
- **시도한 방법**:
  * `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id))` 형식으로 소괄호로 감싸 튜플로 넘겨주려 시도함.
  * 하지만 파이썬 컴파일러는 원소가 1개인 소괄호를 단순한 연산 우선순위 괄호로 판단하여 `user_id` 변수의 기본 타입(예: `int`)으로 처리해 버려, 데이터베이스 드라이버가 이를 다중 값의 이터러블로 해석하지 못했음.
- **최종 해결 및 왜 그 해결책이 작동하는가**:
  * 단일 원소를 가진 튜플을 선언할 때는 반드시 원소 뒤에 쉼표를 붙여 `(user_id,)` 형태로 작성해야 합니다. **끝에 붙은 쉼표(`,`)를 보고 파이썬 인터프리터가 이를 단순 괄호가 아닌 `tuple` 클래스의 인스턴스로 정확히 인식**하게 되며, 데이터베이스 드라이버도 에러 없이 튜플의 첫 번째 값을 플레이스홀더에 바인딩할 수 있게 됩니다.

### 2. FastAPI 통신 중 `422 Unprocessable Entity` 에러 발생
- **문제 상황**: 클라이언트(Swagger UI 혹은 프론트엔드 코드)에서 POST 요청을 보낼 때 API 호출이 실패하며 `422 Unprocessable Entity` 에러와 함께 상세 에러 메시지가 반환됨.
- **시도한 방법**:
  * API 경로(Path)나 메서드가 틀렸나 싶어 `/messages` URI를 검사했으나 경로 문제는 아니었음.
  * 요청 Body를 dictionary 형태로 직접 던졌으나 매칭 실패.
- **최종 해결 및 왜 그 해결책이 작동하는가**:
  * 422 에러는 FastAPI가 **클라이언트로부터 받은 JSON 본문을 Pydantic 모델로 변환(역직렬화 및 유효성 검증)하는 과정에서 타입 불일치나 필수 필드 누락이 발견되었을 때 발생시키는 규격화된 에러**입니다.
  * 디버깅 결과 클라이언트에서 보낸 키값(`userId`)과 Pydantic 모델에 선언된 변수명(`user_id`, 스네이크 케이스)이 일치하지 않았던 것이 원인이었습니다.
  * Pydantic `BaseModel` 구조와 클라이언트 요청 Body의 키/타입을 정확히 일치시켜 해결하였으며, 이를 통해 컴파일 타임 및 런타임 진입 단계에서 데이터 유효성을 선제적으로 완벽히 검증할 수 있었습니다.

## 🔁 이번 주 회고 (KPT)
- **Keep** 유지하고 싶은 습관: 백엔드 API 설계부터 DB 연결까지의 전 과정을 로컬에 직접 띄우고 Swagger UI(/docs)를 활용해 데이터의 CRUD 흐름을 눈으로 직접 보며 검증하는 습관.
- **Problem** 아쉬웠던 점: JavaScript의 느슨한 타입 변환 규칙(예: `'' == false`가 참이 되는 현상 등)이나 Truthy/Falsy 구분을 명확히 짚고 넘어가지 않아 초기에 헷갈렸음.
  실시간 강의의 속도를 따라가지 못했음,,, 아이패드를 가지고는 실시간 강의를 듣는데에 에러사항이 있어 맥북을 들고다녀야 할 것 같음
- **Try** 다음 주에 시도할 것: 프론트엔드 기초를 배운 만큼, 이제 실제로 HTML/CSS/JS 화면 단에서 FastAPI 백엔드 API를 비동기 호출(`fetch` 등)하여 화면이 갱신되는 완전한 풀스택 웹 앱 흐름을 완성해보기.

## 🎯 다음 주 목표
- [ ] HTML/CSS/JS 화면에서 FastAPI 백엔드 API를 호출해 동적으로 데이터를 주고받기
- [ ] 관계형 데이터베이스에서 조금 더 복잡한 N:M 관계의 JOIN 문을 자유롭게 구사하기

---

## 🔗 관련 GitHub 저장소 링크
- [KTC 2주차 학습 노트 (GitHub)](https://github.com/softkleenex/KTC/tree/main/KTC_note/2%EC%A3%BC%EC%B0%A8)
