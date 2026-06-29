---

## 01. Next.js 기초 복습

Next.js는 React를 기반으로 하지만, React처럼 필요한 기능을 하나씩 골라 붙이는 라이브러리라기보다 애플리케이션 전체 구조를 정해주는 프레임워크다.

가장 먼저 잡아야 하는 기준은 다음 세 가지다.

| 파일 | 역할 |
| --- | --- |
| `page.tsx` | 해당 URL에서 렌더링할 화면 |
| `layout.tsx` | 하위 페이지들이 공유하는 UI |
| `loading.tsx` | 데이터 준비 중 보여줄 로딩 UI |

`app/posts/page.tsx`는 `/posts` 경로가 되고, `app/posts/[postId]/page.tsx`는 `/posts/1`, `/posts/2` 같은 동적 경로가 된다. URL 설계가 폴더 구조로 드러나는 점이 App Router의 핵심이다.

---

## 02. Server Component와 Client Component

Next.js의 컴포넌트는 기본적으로 Server Component다. 서버에서 실행되기 때문에 DB나 서버 전용 환경변수에 접근하기 쉽고, 브라우저로 보내는 JavaScript 양도 줄일 수 있다.

반대로 클릭, 입력, 상태 변경처럼 브라우저 이벤트가 필요한 경우에는 파일 상단에 `"use client"`를 선언해 Client Component로 만든다.

| 구분 | Server Component | Client Component |
| --- | --- | --- |
| 기본 여부 | 기본값 | `"use client"` 필요 |
| 실행 위치 | 서버 | 브라우저 |
| `useState` | 사용 불가 | 사용 가능 |
| 이벤트 핸들러 | 사용 불가 | 사용 가능 |
| 서버 환경변수 | 접근 가능 | 직접 노출 위험 |

실습을 하면서 느낀 기준은 단순하다. 데이터를 가져와 보여주기만 하면 Server Component, 사용자가 직접 조작해야 하면 Client Component다.

---

## 03. SQLAlchemy를 쓰는 이유

이전에는 SQL 문자열을 직접 작성해서 DB를 다뤘다.

```python
cursor.execute(
    "INSERT INTO messages (user_id, content) VALUES (?, ?)",
    (1, "안녕")
)
```

작은 예제에서는 괜찮지만, 테이블이 늘어나면 SQL 문자열을 계속 직접 관리해야 한다. 오타도 실행 전까지 찾기 어렵다.

SQLAlchemy는 Python 객체와 DB 테이블을 연결해주는 ORM이다. SQL을 아예 몰라도 된다는 뜻은 아니고, SQL 작업을 Python 코드로 더 구조화해서 다룰 수 있게 해준다.

| 작업 | 직접 SQL | SQLAlchemy |
| --- | --- | --- |
| 등록 | `INSERT INTO ...` | `db.add(post)` |
| 조회 | `SELECT * FROM ...` | `select(Post)` |
| 삭제 | `DELETE FROM ...` | `db.delete(post)` |
| 장점 | SQL 흐름이 직접 보임 | 타입/자동완성/객체 중심 관리 |

---

## 04. FastAPI + SQLAlchemy CRUD 흐름

게시글을 생성하는 흐름을 기준으로 보면 계층이 분명해진다.

```text
브라우저 폼 입력
  → Next.js Server Action
  → FastAPI POST /posts
  → Pydantic 요청 검증
  → SQLAlchemy Post 객체 생성
  → db.add()
  → db.commit()
  → db.refresh()
  → JSON 응답
```

여기서 Pydantic은 API 입출력 데이터의 모양을 검증하고, SQLAlchemy 모델은 DB 테이블과 연결된다. 둘 다 “데이터 구조”를 다루지만 위치가 다르다.

| 구분 | 역할 |
| --- | --- |
| Pydantic Schema | API 요청/응답 검증 |
| SQLAlchemy Model | DB 테이블 매핑 |
| Session | DB 작업 단위 |
| `commit()` | 변경사항 확정 |
| `refresh()` | DB가 생성한 id 등을 객체에 반영 |

---

## 05. 오늘의 정리

4주차 Day3은 Next.js 화면 구조와 백엔드 DB 처리 흐름이 만나는 지점이었다.

- Next.js는 파일 기반 라우팅과 Server Component를 통해 화면과 데이터 fetching을 서버 중심으로 구성한다.
- SQLAlchemy는 Python 객체와 DB 테이블 사이를 연결하는 ORM이다.
- Pydantic은 API 데이터 검증, SQLAlchemy는 DB 테이블 매핑에 가깝다.
- CRUD는 단순히 버튼을 누르는 화면이 아니라, 프론트엔드 요청부터 DB commit까지 이어지는 흐름이다.

> [!note]- 📚 강의 자료 보기
> ![[16. Next.js 기초 & 데이터 처리 복습]]
> ![[17. SQLAlchemy 소개 및 CRUD 실습]]
