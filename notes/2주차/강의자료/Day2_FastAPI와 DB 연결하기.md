

## 🔌 FastAPI와 DB를 연결하는 법

![[IMG_2065 1.jpeg]]



```

- **SQLAlchemy(ORM 방식)**
    
    백엔드 코드(파이썬)와 데이터베이스(SQL)는 **사용하는 언어가 다릅니다.** 파이썬은 `객체(클래스/딕셔너리)`를 사용하고, DB는 `테이블(행/열)`을 사용하죠. 이 둘 사이를 중간에서 통역해 주는 배달원이 바로 SQLAlchemy 같은 **ORM(Object-Relational Mapping)** 라이브러리입니다.
    
    - **SQLAlchemy가 없을 때 (순수 SQL 방식):** 파이썬 코드 중간에 `"SELECT * FROM users WHERE id = 1"` 같은 SQL 문자열을 직접 타이핑해야 합니다. 오타가 나기도 쉽고 번거롭습니다.
    - **SQLAlchemy가 있을 때 (ORM 방식):**`db.query(User).filter(User.id == 1).first()` 처럼 **파이썬 문법 그대로 DB를 제어**할 수 있습니다. 알아서 파이썬 코드를 올바른 SQL 문으로 변환해서 SQLite에 찔러 넣어줍니다.

---

## 0️⃣ 사전 준비 (가상환경 및 패키지 설치)

실습을 시작하기 전, 터미널에서 아래 명령어를 순서대로 실행해 주세요.

```bash
# 1. 가상환경 생성 및 활성화 (터미널)
python -m venv .venv

# (Mac / Linux 환경)
source .venv/bin/activate
# (Windows 환경)
.venv\\Scripts\\activate

# 2. 핵심 패키지 설치
pip install fastapi uvicorn[standard]
```

- 인터프리터(Interpreter)
    
    1. VS Code 화면에서 `Ctrl + Shift + P` (Mac은 `Cmd + Shift + P`)를 누릅니다.
    2. `Python: Select Interpreter`를 검색해 선택합니다.
    3. 목록에서 방금 생성한 `(.venv)`가 포함되어있고, `Recommended`라고 적힌 옵션을 선택합니다.
    
    
    

## 1️⃣ 프로젝트 구조

```
practice/
├── 02_post.py     
├── 03_get.py        
└── database.py    # DB 연결 설정
```

**참고:** 1주차에 배운 APIRouter를 써서 파일을 분리하는 것이 좋지만, 오늘은 **DB 연동의 핵심 원리**에만 집중하기 위해 편의상 [main.py](http://main.py/) 하나에 모두 작성합니다.

### APIRouter 복습

오늘은 `main.py` 하나에 모두 작성하지만, 엔드포인트가 많아지면 **APIRouter**를 사용해 파일을 기능 단위로 나눕니다.

<aside> 📌

**APIRouter란?**

FastAPI 앱을 여러 파일로 분리할 때 사용하는 라우터입니다. 각 파일에서 `APIRouter()`로 라우터를 만들고, `main.py`에서 `app.include_router()`로 합칩니다.

</aside>

파일을 분리한다면 아래처럼 구성합니다:

```
chatbot/
├── main.py              # FastAPI 앱 생성 + 라우터 등록만 담당
├── database.py          # DB 연결 설정
└── routers/
    └── messages.py      # /messages 관련 엔드포인트 모음
```

```python
# routers/messages.py
from fastapi import APIRouter

router = APIRouter(prefix="/messages", tags=["messages"])
# prefix="/messages" → 이 파일의 모든 경로 앞에 /messages 가 자동으로 붙음

@router.get("/")           # 실제 경로: GET /messages/
def get_messages(): ...

@router.post("/")          # 실제 경로: POST /messages/
def create_message(): ...
```

```python
# main.py
from fastapi import FastAPI
from routers import messages

app = FastAPI()
app.include_router(messages.router)  # 라우터 등록
```

서버 실행 방법:

```bash
uvicorn 파일명:app --reload
```

---

## 2️⃣ DB 연결 설정 ([database.py](http://database.py/))

### sqlite3 기본 문법 표

|문법|역할|설명|
|---|---|---|
|`sqlite3.connect(DB_PATH)`|DB 연결|DB 파일이 없으면 자동 생성. 연결 객체(conn) 반환|
|`init_db()`|초기화 함수|앱 시작 시 테이블이 없으면 생성 (`CREATE TABLE IF NOT EXISTS`)|
|`conn.cursor()`|커서 생성|SQL을 실행하는 "펜" 역할. SQL 문 전송 전 반드시 생성|
|`cursor.execute(sql, params)`|SQL 실행|`?` 플레이스홀더에 params 튜플 바인딩 후 실행|
|`conn.commit()`|변경사항 확정|INSERT/UPDATE/DELETE는 commit 전까지 DB에 반영되지 않음|
|`conn.close()`|연결 종료|사용 후 반드시 닫아야 메모리 누수 방지|
|`get_connection()`|연결 헬퍼 함수|매번 connect를 직접 쓰는 대신, 설정이 통일된 conn을 반환하는 함수|
|`conn.row_factory = sqlite3.Row`|결과 형식 설정|조회 결과를 딕셔너리처럼 `row["컬럼명"]`으로 접근 가능하게 설정|

```python
# database.py
import sqlite3

DB_PATH = "chatbot.db"  # .db 파일 하나가 곧 전체 데이터베이스

def get_connection():
    # sqlite3.connect(): 지정한 경로의 DB 파일에 연결 (없으면 자동 생성)
    conn = sqlite3.connect(DB_PATH)

    # row_factory 설정: DB 조회 결과를 어떤 형태로 받을지 지정
    # sqlite3.Row로 설정하면 row["content"] 처럼 컬럼 이름으로 접근할 수 있고,
    # dict(row)로 Python 딕셔너리로 변환하는 것도 가능해집니다.
    # (이 설정이 없으면 결과가 일반 튜플로 오기 때문에 컬럼 이름 접근 불가)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """DB에 테이블이 없으면 생성. 서버를 재시작해도 기존 데이터는 유지됨."""
    conn = get_connection()

    # CREATE TABLE IF NOT EXISTS: 테이블이 이미 있으면 아무것도 안 하고, 없을 때만 생성
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT    NOT NULL
        )
    """)

    # conn.commit(): 실행한 SQL을 실제로 DB 파일에 저장(확정)합니다.
    # INSERT/UPDATE/DELETE/CREATE 등 변경 작업 후에는 반드시 commit()을 호출해야 합니다.
    # commit() 전까지는 변경사항이 메모리에만 있고 아직 파일에 기록되지 않은 상태입니다.
    conn.commit()

    # conn.close(): DB 연결을 닫습니다.
    # DB 연결은 파일 핸들과 메모리를 사용하므로, 작업이 끝나면 반드시 닫아야 합니다.
    # 닫지 않으면 연결이 계속 열려 있어 리소스 낭비 및 충돌이 발생할 수 있습니다.
    conn.close()
```

<aside> 💡

`row_factory = sqlite3.Row` 설정을 하면 `row["content"]` 처럼 칼럼 이름으로 결과를 꺼낼 수 있어요.

이 설정이 없으면 DB 조회 결과가 일반 **튜플**로 반환됩니다:

```python
# row_factory 없이 — 튜플 형태
row = (1, 1, "안녕하세요")
row[2]        # "안녕하세요" (인덱스로만 접근 가능)
dict(row)     # ❌ 오류 — 컬럼 이름 정보가 없어서 dict 변환 불가
```

`sqlite3.Row`로 설정하면 결과 객체가 컬럼 이름을 알고 있어서:

```python
# row_factory = sqlite3.Row 설정 후
row["content"]   # ✅ "안녕하세요" — 컬럼 이름으로 접근 가능
row[2]           # ✅ "안녕하세요" — 인덱스로도 여전히 접근 가능
dict(row)        # ✅ {"id": 1, "user_id": 1, "content": "안녕하세요"} — 딕셔너리 변환 가능
```

</aside>

---

## 3️⃣ 메시지 저장 API (POST)

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import get_connection, init_db

app = FastAPI()
init_db()  # 서버 시작 시 테이블 자동 생성 (없으면 만들고, 있으면 그냥 넘어감)

# ─── Pydantic 스키마 정의 (API 위쪽에 모아두는 것이 좋습니다) ───

# [요청 스키마] 클라이언트가 보내는 데이터의 형태 정의
class MessageRequest(BaseModel):
    user_id: int
    content: str = Field(min_length=1, max_length=500)  # 빈 문자열 방지, 최대 500자

# [응답 스키마] 서버가 돌려주는 데이터의 형태 정의
class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    status: str = "saved"  # 기본값 "saved"

# ─────────────────────────────────────────────────────────

# response_model=MessageResponse 를 지정하면:
# 1. 반환한 딕셔너리를 자동으로 MessageResponse 형태로 변환 및 검증
# 2. Swagger UI(/docs)에 "이 API는 이런 형태로 응답합니다" 자동 문서화
@app.post("/messages", response_model=MessageResponse)
def create_message(request: MessageRequest):
    conn = get_connection()   # DB 연결 열기
    cursor = conn.cursor()    # SQL을 실행할 커서 생성 (DB와 직접 대화하는 객체)

    # ✏️ [실습] messages 테이블에 user_id와 content를 삽입하는 INSERT 쿼리를 완성하세요.
    # SQL 인젝션 방지를 위해 값 자리에는 ? 를 사용합니다.
    cursor.execute(
        "여기에 INSERT 쿼리를 작성하세요",
        (request.user_id, request.content)
    )

    conn.commit()              # 변경사항을 DB 파일에 확정 저장
    new_id = cursor.lastrowid  # 방금 INSERT된 행의 자동 생성 id 값
    conn.close()               # DB 연결 닫기 (리소스 해제)

    return {
        "id": new_id,
        "user_id": request.user_id,
        "content": request.content,
        "status": "saved",
    }

# 실행 예시:
# POST /messages  Body: {"user_id": 1, "content": "안녕하세요"}
# → {"id": 1, "user_id": 1, "content": "안녕하세요", "status": "saved"}

@app.get("/messages", response_model=list[MessageResponse])
def get_messages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# 실행 예시:
# GET /messages → [{"id": 1, "user_id": 1, "content": "안녕하세요", "status": "saved"}, ...]
```

<aside> ⚠️

**`?` 를 쓰는 이유**

`VALUES (?, ?)` 처럼 물음표를 쓰면 sqlite3가 값을 안전하게 이스케이프 처리합니다. 아래처럼 f-string으로 직접 문자열에 넣으면 악의적인 SQL 코드가 실행되는 **SQL 인젝션 공격**에 노출됩니다:

```python
# ❌ 위험한 방식
cursor.execute(f"INSERT INTO messages (content) VALUES ('{request.content}')")
# content에 '); DROP TABLE messages; -- 를 입력하면 테이블이 삭제됨

# ✅ 안전한 방식
cursor.execute("INSERT INTO messages (content) VALUES (?)", (request.content,))
```

</aside>

- 두 번째 인자로 실제 값을 튜플 형태로 전달합니다: `(request.user_id, request.content)`
    
- 정답
    
    ```python
    cursor.execute(
        "INSERT INTO messages (user_id, content) VALUES (?, ?)",
        (request.user_id, request.content)
    )
    ```
    

---

## 4️⃣ 메시지 조회 API (GET)

```python
# 쿼리 파라미터 user_id가 있으면 해당 사용자의 메시지만, 없으면 전체 조회
# 예: GET /messages?user_id=1  →  user_id가 1인 메시지만 반환
# 예: GET /messages            →  전체 메시지 반환
@app.get("/messages", response_model=list[MessageResponse])
def get_messages(user_id: Optional[int] = None):  # user_id는 선택 파라미터 (없으면 None)
    conn = get_connection()
    cursor = conn.cursor()

    if user_id is not None:
        # user_id 조건이 있을 때: WHERE 절로 필터링
        # ✏️ [실습] user_id 조건으로 필터링하는 SELECT 쿼리를 완성하세요.
        cursor.execute(
            "여기에 SELECT ~ WHERE 쿼리를 작성하세요", (user_id,)
        )
    else:
        # user_id 조건이 없을 때: 전체 조회
        cursor.execute("SELECT * FROM messages")

    rows = cursor.fetchall()  # 쿼리 결과 전체를 리스트로 가져옴 (결과 없으면 빈 리스트)
    conn.close()

    # dict(row): sqlite3.Row 객체를 Python 딕셔너리로 변환
    # row_factory = sqlite3.Row 설정 덕분에 가능하며, FastAPI가 JSON으로 직렬화하려면 dict가 필요함
    return [dict(row) for row in rows]

# 실행 예시:
# GET /messages           → [{"id": 1, ...}, {"id": 2, ...}]  (전체)
# GET /messages?user_id=1 → [{"id": 1, ...}]                  (user_id=1인 것만)
```

- 원소가 하나인 튜플은 뒤에 쉼표가 필요합니다: `(user_id,)`
    
- 정답
    
    ```python
    cursor.execute(
        "SELECT * FROM messages WHERE user_id = ?", (user_id,)
    )
    ```
    

---

## 5️⃣ Swagger UI로 테스트하기

1. `uvicorn 02_post:app --reload` 실행
2. 브라우저에서 `http://127.0.0.1:8000/docs` 접속
3. `POST /messages` 클릭 → **Try it out** → Body 입력 → **Execute**
4. `uvicorn 03_get:app --reload` 실행 → `GET /messages` 클릭 → 저장된 메시지 확인

---

## 📝 실습: 메시지 삭제 API 만들기

<aside> 📝

**실습 문제**

아래 엔드포인트를 직접 구현해보세요.

`DELETE /messages/{message_id}` → 해당 id의 메시지 삭제. 없으면 404 에러 반환.

</aside>

```python
@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # ✏️ [실습] message_id에 해당하는 메시지를 삭제하는 DELETE 쿼리를 작성하세요.
    cursor.execute("여기에 DELETE 쿼리를 작성하세요", (message_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    # ✏️ [실습] 삭제된 행이 없으면(deleted == 0) 404 에러를 반환하세요.
    # 여기에 조건문을 작성하세요

    return {"status": "deleted", "message_id": message_id}
```

- `cursor.rowcount`: SQL 실행 후 영향받은 행 수. 0이면 해당 id의 데이터가 없다는 뜻입니다.
    
- 404 에러: `raise HTTPException(상태 코드, 상태 메시지)`
    
- 정답
    
    ```python
    @app.delete("/messages/{message_id}")
    def delete_message(message_id: int):
        conn = get_connection()
        cursor = conn.cursor()
    
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        deleted = cursor.rowcount  # 삭제된 행 수
        conn.close()
    
        if deleted == 0:
            raise HTTPException(status_code=404, detail="메시지를 찾을 수 없습니다")
    
        return {"status": "deleted", "message_id": message_id}
    
    # DELETE /messages/1  → {"status": "deleted", "message_id": 1}
    # DELETE /messages/99 → 404 {"detail": "메시지를 찾을 수 없습니다"}
    ```
    

---

## 🎯 정리

<aside> 📌

**오늘 배운 것**

- SQLite
    
- Pydantic 모델(임시) vs DB 테이블(영구 저장)의 차이
    
- `sqlite3`로 FastAPI와 DB를 연결하는 기본 패턴
    
- `?` 파라미터로 안전하게 SQL 쿼리 작성하기
    
- POST(저장), GET(조회), DELETE(삭제) API + DB 연동
    
- (참고) Depends
    
    오늘 코드에서는 매번 `conn = get_connection()`과 `conn.close()`를 직접 작성했습니다. FastAPI의 **의존성 주입(Depends)**을 사용하면 API 호출 시 자동으로 연결을 열고, 응답이 끝나면 자동으로 닫아주는 구조를 만들 수 있습니다.
    

</aside>

<aside> 🔭

**다음 내용**

- **2주 3일차 (VOD)**: HTML/CSS — 지금 만든 API를 화면에서 호출하려면 프론트엔드가 필요합니다 </aside>