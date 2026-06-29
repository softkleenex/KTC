---

## 01. 프로젝트 구조

Day4에서는 Next.js 프론트엔드와 FastAPI 백엔드를 연결해 End-to-End 흐름을 확인했다. 여기서 End-to-End는 사용자의 입력이 화면에서 시작해 API, ORM, DB까지 도달하고 다시 화면으로 돌아오는 전체 과정을 뜻한다.

```text
fullstack-practice/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── actions.ts
│   │   └── posts/
│   │       ├── page.tsx
│   │       ├── new/page.tsx
│   │       └── [postId]/
│   │           ├── page.tsx
│   │           └── edit/page.tsx
│   └── .env.local
│
└── backend/
    ├── main.py
    └── blog.db
```

역할을 나누면 다음과 같다.

| 위치 | 역할 |
| --- | --- |
| Next.js `page.tsx` | 목록, 상세, 작성, 수정 화면 |
| Next.js `actions.ts` | 서버에서 FastAPI 호출 |
| FastAPI `main.py` | API 엔드포인트 처리 |
| SQLAlchemy | Python 객체와 DB 테이블 연결 |
| SQLite `blog.db` | 실제 데이터 저장 |

---

## 02. 게시글 생성 요청 흐름

새 글 작성 버튼을 눌렀을 때 흐름은 다음과 같다.

```text
1. 브라우저
   사용자가 /posts/new 폼에 제목과 내용을 입력

2. Next.js Server Action
   createPost(formData)가 서버에서 실행

3. FastAPI
   POST /posts 엔드포인트 실행

4. Pydantic
   요청 데이터 타입과 필드 검증

5. SQLAlchemy
   Post 객체 생성 후 db.add(), db.commit(), db.refresh()

6. SQLite
   posts 테이블에 데이터 저장

7. Next.js
   revalidateTag() 후 /posts로 redirect
```

이 흐름을 따라가면 풀스택 프로젝트에서 각 계층이 왜 필요한지 보인다. 프론트엔드는 입력과 화면 전환을 담당하고, 백엔드는 요청 검증과 저장을 담당하며, ORM은 애플리케이션 코드와 DB 사이의 번역을 담당한다.

---

## 03. Server Action을 쓰면 CORS 문제가 줄어드는 이유

브라우저가 `localhost:3000`에서 `localhost:8000`으로 직접 요청을 보내면 출처가 달라 CORS 설정이 필요하다.

하지만 Server Action을 사용하면 브라우저가 FastAPI를 직접 호출하지 않는다.

```text
브라우저
  → Next.js 서버의 Server Action
  → FastAPI 서버
```

즉, FastAPI를 호출하는 주체가 브라우저가 아니라 Next.js 서버가 된다. 브라우저 보안 정책인 CORS는 “브라우저의 교차 출처 요청”에 적용되므로, 서버 간 통신에서는 같은 방식으로 문제가 발생하지 않는다.

---

## 04. 실행 순서

백엔드와 프론트엔드를 각각 실행한다.

```bash
cd fullstack-practice/backend
uv pip install -r requirements.txt
uv run fastapi dev main.py
```

```bash
cd fullstack-practice/frontend
npm install
npm run dev
```

프론트엔드에서는 FastAPI 주소를 환경변수로 관리한다.

```env
FASTAPI_URL=http://localhost:8000
```

확인할 것은 단순히 화면이 뜨는지가 아니다.

1. 게시글 작성
2. 목록에 새 글 표시
3. 상세 페이지 조회
4. 수정 후 반영 확인
5. 삭제 후 목록에서 제거
6. Swagger UI에서 실제 API 응답 확인

---

## 05. 오늘의 정리

End-to-End 흐름을 확인한다는 것은 “각 서버가 켜졌다”에서 끝나지 않는다. 사용자의 행동이 DB 저장까지 이어지고, 다시 화면에 반영되는지 확인해야 한다.

```text
Next.js 화면
  → Server Action
  → FastAPI
  → SQLAlchemy
  → SQLite
  → 다시 Next.js 화면
```

이 흐름을 한 번 끝까지 따라가 보니 풀스택이라는 말이 단순히 프론트와 백을 둘 다 만든다는 뜻이 아니라, 데이터가 오가는 길 전체를 책임진다는 뜻에 가깝게 느껴졌다.

> [!note]- 📚 강의 자료 보기
> ![[18. End-to-End 흐름 확인]]
