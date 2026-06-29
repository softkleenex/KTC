---

## FastAPI & Pydantic

---

## FastAPI 기본 구조

FastAPI는 Python으로 API 서버를 빠르게 만들 수 있는 프레임워크다. 함수 위에 데코레이터를 붙여 HTTP Method와 URL path를 연결한다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
```

여기서 `@app.get("/")`는 `GET /` 요청이 들어왔을 때 아래 함수를 실행하겠다는 뜻이다. 함수가 반환한 dict는 JSON 응답으로 변환된다.

---

## Path Parameter와 Query Parameter

URL 경로 자체에 포함되는 값은 Path Parameter다.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

`/items/1`로 요청하면 `item_id`에는 `1`이 들어온다. 타입을 `int`로 지정하면 FastAPI가 자동으로 타입 변환과 검증을 수행한다.

물음표 뒤에 붙는 값은 Query Parameter다.

```python
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

`/items?skip=10&limit=5`처럼 요청하면 함수 인자로 값이 전달된다.

---

## Pydantic BaseModel

POST 요청처럼 JSON body를 받을 때는 Pydantic의 `BaseModel`을 사용한다.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items")
def create_item(item: Item):
    return item
```

Pydantic은 요청 body가 정해진 타입과 필드를 만족하는지 검증한다. 잘못된 타입이 들어오면 FastAPI는 자동으로 `422 Unprocessable Entity` 응답을 반환한다.

---

## Swagger UI

FastAPI의 장점 중 하나는 API 문서가 자동으로 생성된다는 점이다.

```text
http://localhost:8000/docs
```

Swagger UI에서는 API 목록, 요청 body 형식, 응답 형식을 확인하고 직접 요청도 보내볼 수 있다. 실습할 때는 브라우저, curl, Postman 없이도 `/docs`에서 빠르게 API를 검증할 수 있어 편하다.

---

## 오늘의 정리

- FastAPI는 데코레이터로 URL과 함수를 연결한다.
- Path Parameter는 URL 경로 안의 값이다.
- Query Parameter는 `?key=value` 형태의 값이다.
- Pydantic `BaseModel`은 요청 body의 구조와 타입을 검증한다.
- Swagger UI는 FastAPI가 자동으로 만들어주는 API 테스트/문서 화면이다.
