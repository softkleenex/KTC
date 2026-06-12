

---

## 🌐 16. Next.js 기초 & 데이터 처리 복습

> [!note]- 📚 16. Next.js 기초 & 데이터 처리 복습 내용 보기
> 
> ### 1️⃣ Next.js 기초와 렌더링 복습
> 
> <aside>
> 👾 **Framework vs Library**
> 
> React는 **라이브러리**입니다. 라우팅, 데이터 페칭, 폴더 구조 등 모든 것을 개발자가 직접 결정합니다.
> Next.js는 **프레임워크**입니다. "이 폴더에 이 파일을 두면 이렇게 동작한다"는 규칙이 이미 정해져 있습니다. 제어권이 프레임워크에 있고, 개발자는 그 규칙 안에서 코드를 채웁니다.
> 비유하자면 React는 식재료만 주는 것이고, Next.js는 레시피와 주방 도구까지 세팅해주는 것입니다.
> </aside>
> 
> ---
> 
> ### App Router & File-based Routing
> 
> Next.js에서는 **폴더와 파일의 위치가 곧 URL 경로**가 됩니다.
> 
> - [Next.js App Router 공식 문서](https://nextjs-ko.org/docs/app/building-your-application/routing)
> 
> | 파일 경로 | URL |
> | --- | --- |
> | `app/page.tsx` | `/` |
> | `app/posts/page.tsx` | `/posts` |
> | `app/posts/[postId]/page.tsx` | `/posts/1`, `/posts/2` |
> 
> - `page.tsx` — 해당 경로에서 보여줄 화면
> - `layout.tsx` — 공통 레이아웃으로, 하위 페이지들이 children prop으로 전달되어 내부에 렌더링됩니다.
> - `loading.tsx` — 페이지 로딩 중에 보여줄 UI
> 
> ---
> 
> ### 2️⃣ 데이터 처리와 최적화 복습
> 
> ### 서버 컴포넌트에서 직접 데이터 가져오기
> 
> Next.js의 Server Component는 서버에서 실행됩니다. 덕분에 컴포넌트 자체를 `async` 함수로 만들어 직접 데이터를 가져올 수 있습니다.
> 
> ```tsx
> // app/posts/page.tsx — Server Component
> export default async function PostsPage() {
>   const res = await fetch("http://localhost:8000/posts");
>   const posts = await res.json();
> 
>   return (
>     <ul>
>       {posts.map((post) => (
>         <li key={post.id}>{post.title}</li>
>       ))}
>     </ul>
>   );
> }
> ```
> 
> 이 컴포넌트는 브라우저가 아니라 서버에서 실행됩니다. 서버 컴포넌트는 모든 계산과 화면 조립을 서버에서 끝냅니다. 브라우저는 무거운 소스코드 대신 '다 만들어진 화면(HTML)'만 받기 때문에, 다운로드할 용량이 줄어들어 첫 화면이 뜨는 속도가 압도적으로 빨라집니다.
> 
> ---
> 
> ### Streaming과 loading.tsx
> 
> **SSR(Server Side Rendering)의 한계:** 서버에서 데이터를 모두 가져올 때까지 브라우저는 빈 화면을 보게 됩니다.
> 
> **Streaming으로 해결:** `loading.tsx`를 추가하면 Next.js는 HTML을 조각조각 나눠 전송합니다. 레이아웃과 로딩 UI를 먼저 보내고, 데이터 준비가 끝나면 나머지를 추가로 전송합니다.
> 
> > 💡 **스트리밍**은 SSR의 단점을 해결하기 위해 페이지의 HTML을 더 작은 청크로 나누고 서버에서 클라이언트로 점진적으로 전송하는 방식입니다.
> 
> - [Next.js Loading UI와 스트리밍 가이드](https://nextjs-ko.org/docs/app/building-your-application/routing/loading-ui-and-streaming)
> 
> ```
> loading.tsx가 있을 때:
> 1. 브라우저가 요청
> 2. 서버: 레이아웃 + 로딩 UI 즉시 전송 ← 사용자가 빈 화면 대신 스켈레톤을 봅니다
> 3. 서버: 데이터 페칭 진행 중...
> 4. 서버: 완성된 컴포넌트 추가 전송
> 5. 브라우저: 화면 업데이트
> ```
> 
> ---
> 
> ### Promise.all 로 여러 개의 Data Fetching
> 
> 데이터를 순차적으로 가져오면 대기 시간이 합산됩니다.
> 
> ```tsx
> // ❌ 순차 실행: 100ms + 200ms = 300ms 대기
> const user = await fetchUser();    // 100ms
> const posts = await fetchPosts();  // 200ms
> 
> // ✅ 병렬 실행: max(100ms, 200ms) = 200ms 대기
> const [user, posts] = await Promise.all([
>   fetchUser(),
>   fetchPosts(),
> ]);
> ```
> 
> 두 요청이 서로 의존하지 않는다면, `Promise.all`로 동시에 보내는 것이 훨씬 효율적입니다.
> 
> ---
> 
> ### 3️⃣ Server Component vs Client Component, 그리고 Server Actions
> 
> ### Server Component vs Client Component
> 
> Next.js의 모든 컴포넌트는 기본적으로 **Server Component**입니다. 서버에서 실행되며, 완성된 HTML 등이 클라이언트에 전달됩니다. 반면 **Client Component**는 파일 최상단에 `"use client"` 지시어를 선언하며, 서버에서 초기 렌더링 후 브라우저에서 실행됩니다.
> 
> | 구분 | Server Component | Client Component |
> | --- | --- | --- |
> | **선언 방법** | 기본값 (별도 선언 불필요) | 파일 상단에 `"use client"` |
> | **실행 위치** | 서버 | 서버 (사전 렌더링) + 브라우저 (Hydration) |
> | **async/await** | ✅ 컴포넌트 함수 자체에 사용 가능 | ❌ 컴포넌트 함수 자체에는 사용 불가<br>(내부 함수나 이벤트 핸들러에서는 사용 가능) |
> | **useState / useEffect** | ❌ 사용 불가 | ✅ 사용 가능 |
> | **onClick 등 이벤트 핸들러** | ❌ 사용 불가 | ✅ 사용 가능 |
> | **DB / 환경변수 직접 접근** | ✅ 가능 (서버에서 실행) | ❌ 불가 (브라우저 노출 위험, `NEXT_PUBLIC_` 환경변수는 예외) |
> | **클라이언트 번들 크기** | 영향 없음 | 번들에 포함됨 |
> 
> ```tsx
> // Server Component — 기본값, 컴포넌트 함수 자체에 async 사용 가능
> // app/posts/page.tsx
> export default async function PostsPage() {
>   // 서버에서 직접 DB/API 호출 — 클라이언트에 URL 노출 없음
>   const res = await fetch(`${process.env.FASTAPI_URL}/posts`);
>   const posts = await res.json();
>   return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
> }
> ```
> 
> ```tsx
> // Client Component — "use client" 선언 필수
> // app/search/page.tsx
> "use client";
> import { useState } from "react";
> 
> export default function SearchPage() {
>   const [query, setQuery] = useState(""); // Server Component에서는 사용 불가
>   return (
>     <input
>       value={query}
>       onChange={(e) => setQuery(e.target.value)}
>       placeholder="검색어 입력..."
>     />
>   );
> }
> ```
> 
> <aside>
> 📌 인터랙션(클릭, 입력 등 사용자 행동)이 필요하면 **Client Component**, 데이터 페칭·DB 접근만 필요하면 **Server Component**를 선택하시는 걸 권장드립니다. 하나의 페이지 안에서 두 종류를 자유롭게 섞어 쓸 수 있습니다.
> </aside>
> 
> ---
> 
> ### Server Actions
> 
> **Server Actions**는 `"use server"` 지시어를 선언한 **서버 전용 함수**입니다. Client Component나 `<form>`에서 직접 호출할 수 있으며, 별도의 API Route를 만들지 않아도 됩니다. 함수 본문은 항상 서버에서 실행되므로 `FASTAPI_URL` 같은 환경변수를 안전하게 사용할 수 있습니다.
> 
> - 사용자의 입력(Form 제출)이나 상호작용으로 인해 서버의 데이터가 변경(CUD)되어야 할 때 사용
> 
> ```tsx
> // app/actions.ts
> "use server";
> import { revalidateTag } from "next/cache";
> import { redirect } from "next/navigation";
> 
> export async function createPost(formData: FormData) {
>   const title = formData.get("title") as string;
>   const content = formData.get("content") as string;
> 
>   // 서버에서 직접 FastAPI 호출 — FASTAPI_URL이 클라이언트에 노출되지 않음
>   await fetch(`${process.env.FASTAPI_URL}/posts`, {
>     method: "POST",
>     headers: { "Content-Type": "application/json" },
>     body: JSON.stringify({ title, content }),
>   });
> 
>   revalidateTag("posts-list"); // 게시글 목록 캐시 즉시 무효화
>   redirect("/posts");          // 완료 후 목록 페이지로 이동
> }
> ```
> 
> ```tsx
> // app/posts/new/page.tsx — <form action={서버액션}> 패턴
> import { createPost } from "@/app/actions";
> 
> export default function NewPostPage() {
>   return (
>     // HTML <form>의 action에 서버 함수를 직접 연결
>     // 제출 시 formData가 createPost로 자동 전달됨
>     <form action={createPost}>
>       <input name="title" placeholder="제목" />
>       <textarea name="content" placeholder="내용" />
>       <button type="submit">작성</button>
>     </form>
>   );
> }
> ```
> 
> <aside>
> 💡 **SSR의 한계를 최소화하는 전략**
> 
> **SSR의 기본 한계:** 서버가 HTML을 완성해 보내므로 초기 로딩은 빠르지만, 사용자 인터랙션(클릭, 입력 등)과 실시간 상태 변화를 서버 컴포넌트 단독으로는 처리하기는 어렵습니다.
> 
> **Server Component + Client Component 분리**로 해결합니다. 데이터 표시처럼 정적인 부분은 Server Component가 담당해 JavaScript 번들을 줄이고, 검색창·버튼처럼 인터랙션이 필요한 부분만 Client Component로 교체합니다. 필요한 곳에만 선택적으로 브라우저 코드를 씁니다.
> 
> **Server Actions**는 API Route Handler를 만들지 않고도 클라이언트에서 서버 로직을 실행할 수 있게 합니다. 폼 제출이나 데이터 변경 후 `revalidateTag()`로 캐시를 즉시 갱신하면, 사용자는 페이지 새로고침 없이 최신 데이터를 바로 볼 수 있습니다.
> 
> **결과:** 초기 로딩 속도라는 SSR의 장점을 유지하면서, 인터랙션 반응성이라는 CSR의 장점까지 확보합니다.
> </aside>

---

## 🗄️ 17. SQLAlchemy 소개 및 CRUD 실습

> [!note]- 📚 17. SQLAlchemy 소개 및 CRUD 실습 내용 보기
> 
> > 📌 **SQLAlchemy란?**
> > Python 클래스와 데이터베이스 테이블을 연결해 주는 ORM(Object-Relational Mapping) 라이브러리입니다. SQL 구문을 직접 작성하지 않고도 Python 코드를 통해 데이터베이스의 데이터를 관리할 수 있도록 지원합니다.
> 
> ### 1️⃣ ORM의 필요성
> 
> 이전에는 `sqlite3` 모듈을 활용해 SQL을 직접 작성하여 데이터를 추가했습니다.
> 
> ```python
> # sqlite3 방식: SQL 문자열을 직접 작성하여 실행
> cursor.execute(
>     "INSERT INTO messages (user_id, content) VALUES (?, ?)",
>     (1, "안녕")
> )
> ```
> 
> 이 방식은 프로젝트의 규모가 커지고 테이블이 늘어날수록 복잡한 SQL 문자열을 소스코드 내에서 관리하기가 까다로워집니다. 사소한 오타도 실제 프로그램이 실행되기 전에는 에러를 발견하기 어렵고, 자동완성의 도움도 받을 수 없습니다.
> 
> ORM은 객체와 데이터베이스 간의 번역기 역할을 수행합니다.
> 우리에게 익숙한 Python 코드를 작성하면, ORM이 이를 적절한 SQL 구문으로 변환하여 실행해 줍니다.
> 
> | **작업 구분** | **sqlite3 방식 (직접 SQL 작성)** | **SQLAlchemy 방식 (Python 코드)** |
> | --- | --- | --- |
> | **등록** | `cursor.execute("INSERT INTO ...")` | `db.add(post)` |
> | **조회** | `cursor.execute("SELECT * FROM ...")` | `db.execute(select(Post)).scalars().all()` |
> | **삭제** | `cursor.execute("DELETE FROM ...")` | `db.delete(post)` |
> | **안정성** | 실행해 보기 전에는 오류 확인이 어려움 | 코드 개발 도구(IDE)의 자동완성 및 타입 지원 |
> 
> ---
> 
> ### 2️⃣ SQLAlchemy 핵심 개념 4가지
> 
> ```bash
> pip install SQLAlchemy
> ```
> 
> ```bash
> # 1. backend 폴더로 이동
> cd fullstack-practice/backend
> 
> # 2. uv 가상환경 생성 (최초 1회)
> uv venv
> 
> # 3. 의존성 패키지 일괄 설치
> uv pip install -r requirements.txt
> 
> # 4. 개발 서버 실행
> uv run fastapi dev main.py
> 
> # 💡 혹시 에러가 발생한다면? 현재 폴더에 잘못 생성되었거나 경로가 틀어진 .venv 폴더를 완전히 지우고 새로 시작합니다.
> rm -rf .venv
> ```
> 
> ```bash
> # 프론트엔드 실행
> cd fullstack-practice/frontend
> npm install
> npm run dev
> ```
> 
> #### ① 데이터베이스 연결 설정 (main.py 상단 영역)
> 
> <aside>
> 🧼 **주요 개념 정리**
> - **engine**: 실제 데이터베이스 파일(ex. blog.db)과의 연결 경로를 열고 관리합니다.
> - **SessionLocal**: 데이터베이스에 데이터를 조회하고 추가/수정/삭제 작업을 수행할 수 있는 창구(세션)를 만들어 냅니다.
> - **Base**: 파이썬 클래스가 데이터베이스의 테이블과 연결될 수 있도록 기본 규칙을 제공하는 뼈대 클래스입니다.
> - **Model (Post)**: Base를 상속받아 데이터베이스 테이블에 저장될 구체적인 항목(id, 제목, 내용 등)을 선언한 클래스입니다.
> </aside>
> 
> ```python
> from sqlalchemy import create_engine
> from sqlalchemy.orm import sessionmaker, DeclarativeBase
> 
> # 1. DATABASE_URL: 연결할 데이터베이스의 경로를 지정합니다.
> DATABASE_URL = "sqlite:///./blog.db"
> 
> # 2. engine: 데이터베이스와의 실제 물리적인 연결을 관리하는 객체입니다.
> engine = create_engine(
>     DATABASE_URL, 
>     connect_args={"check_same_thread": False}
> )
> 
> # 3. SessionLocal: 데이터베이스 조작 작업(등록, 조회 등)을 수행할 세션(Session) 객체를 생성하는 클래스입니다.
> SessionLocal = sessionmaker(
>     bind=engine,
>     autoflush=False,
> )
> 
> # 4. Base: 데이터베이스 테이블 정보를 선언할 때 규칙 공유를 위해 반드시 상속받아야 하는 기준 클래스입니다.
> class Base(DeclarativeBase):
>     pass
> ```
> 
> ---
> 
> #### ② Model — Python 클래스와 DB 테이블 매핑
> 
> ```python
> from datetime import datetime, timezone
> from sqlalchemy import Integer, String, Text, DateTime
> from sqlalchemy.orm import Mapped, mapped_column
> 
> # 5. Base를 상속받아 데이터베이스에 생성할 'posts' 테이블 구조를 설계하는 클래스입니다.
> class Post(Base):
>     __tablename__ = "posts"   # 데이터베이스에 만들어질 실제 테이블 이름
> 
>     # id: 각 데이터(행)를 식별하는 고유 번호입니다. 고유값 식별을 위해 기본키(primary_key)로 지정합니다.
>     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
>     
>     # title: 게시글의 제목입니다. 최대 200자 제한을 두며, 빈 값(nullable=False)을 허용하지 않습니다.
>     title: Mapped[str] = mapped_column(String(200), nullable=False)
>     
>     # content: 게시글의 본문 내용입니다. 길이 제한이 없는 텍스트형이며, 빈 값을 허용하지 않습니다.
>     content: Mapped[str] = mapped_column(Text, nullable=False)
>     
>     # created_at: 글이 작성된 시간입니다. 기본값으로 함수를 연결해 데이터가 저장될 때의 현재 UTC 시간이 기록됩니다.
>     created_at: Mapped[datetime] = mapped_column(
>         DateTime, default=lambda: datetime.now(timezone.utc)
>     )
> 
> # [참고] 서버가 실행될 때, 위에서 설계한 'posts' 테이블이 실제 파일에 존재하지 않는다면 자동으로 생성해 줍니다.
> Base.metadata.create_all(bind=engine)
> ```
> 
> ---
> 
> ### 3️⃣ 데이터 조회 API 학습 및 실습
> 
> ```python
> def get_db():
>     db = SessionLocal()  # Session 활성화
>     try:
>         yield db         # 엔드포인트에 Session 주입
>     finally:
>         db.close()       # 요청 처리가 종료되면 확실하게 세션 반환 및 종료
> ```
> 💡 `get_db()`는 이 요청에서만 쓸 DB 세션을 빌려주고, 요청이 끝나면 반납하는 역할입니다. 없으면 매 라우트마다 세션 열고 닫는 코드를 반복해야 하고, 실수로 `close()`를 빼먹기 쉽습니다.
> 
> #### ① 전체 조회 (Select All) 문법
> 파이썬 코드로 전체 데이터를 조회할 때는 두 가지 단계를 거칩니다.
> 1. `select(Post)`: SQL의 `SELECT * FROM posts;` 문장을 만들어내는 작업입니다.
> 2. `db.scalars(...).all()`: 데이터베이스에 쿼리를 실행하고, 그 결과를 파이썬 객체 리스트(목록)로 가공하여 가져옵니다.
> 
> ```python
> # 1. 쿼리문 객체 만들기 (posts 테이블에서 id가 1인 데이터를 찾는 문장 준비)
> stmt = select(Post).where(Post.id == 1)
> 
> # 2. 실행 및 결과 추출 (db.scalar()를 통해 단 한 건의 결과 객체를 직접 가져옵니다)
> post = db.scalar(stmt)
> ```
> 
> ```python
> @app.get("/posts", response_model=list[PostResponse])
> def get_posts(db: Session = Depends(get_db)):
>     # 데이터베이스에서 모든 게시글을 조회하여 리스트로 반환합니다
>     return db.scalars(select(Post)).all()
> ```
> 
> #### ② 단건 조회 (Select One) 문법
> 특정 조건에 맞는 데이터 한 건만 조회할 때는 다음과 같이 작성합니다.
> 1. `.where(Post.id == post_id)`: SQL의 `WHERE posts.id = ?` 조건문을 작성하는 방식입니다.
> 2. `db.scalar(...)`: 조건에 부합하는 **단 하나의 결과 객체**를 가져옵니다. 만약 찾는 데이터가 없다면 `None`을 반환합니다.
> 
> ```python
> # post_id로 조회하여 데이터가 있으면 Post 객체를, 없으면 None을 반환하는 함수
> def _get_post_or_none(db: Session, post_id: int) -> Post | None:
>     return db.scalar(select(Post).where(Post.id == post_id))
> ```
> 
> ---
> 
> #### 📝 실습 1: GET /posts/{post_id} (단건 조회) 구현
> 
> ```python
> @app.get("/posts/{post_id}", response_model=PostResponse)
> def get_post(post_id: int, db: Session = Depends(get_db)):
>     # ✏️ Q1. Post 테이블에서 id가 post_id와 일치하는 데이터를 찾는 쿼리문(stmt)을 작성하고 실행하세요.
>     # 힌트: select(Post).where(조건)와 db.scalar(stmt)를 조합합니다.
>     stmt = select(Post).where(____________________)
>     post = db.scalar(________)
> 
>     # ✏️ Q2. 만약 일치하는 게시글(post)이 없다면, 사용자에게 404 에러를 반환하세요.
>     # 힌트: raise HTTPException(status_code=404, detail="...")을 사용합니다.
>     if not post:
>         raise ___________________________________________
> 
>     return post
> ```
> 
> > [!success]- **정답 확인하기**
> > ```python
> > @app.get("/posts/{post_id}", response_model=PostResponse)
> > def get_post(post_id: int, db: Session = Depends(get_db)):
> >     stmt = select(Post).where(Post.id == post_id)
> >     post = db.scalar(stmt)
> > 
> >     if not post:
> >         raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
> >     return post
> > ```
> 
> ---
> 
> ### 4️⃣ 트랜잭션과 데이터 생성 API 학습 및 실습
> 
> 데이터베이스의 값을 변경할 때는 안정성을 위해 **트랜잭션(Transaction)** 단위로 작업을 관리해야 합니다.
> 
> <aside>
> 🚧 **트랜잭션(Transaction)이란?**
> - 더 이상 쪼갤 수 없는 하나의 논리적인 작업 단위
> - 여러 개의 데이터베이스 조작 로직을 최소 하나의 논리 작업 덩어리로 구성해 관리하는 메커니즘
> 
> 수행 단계 중 어떠한 작업 오류라도 도출되면, **전체 처리를 실행 전 지점으로 완전히 백업 및 되돌리는 롤백(Rollback)** 연동을 발동시켜 데이터에 오류 상태가 누적되는 현상을 차단합니다.
> 
> *실생활 예시: 자금 송금 거래*
> 1단계. A 계좌에서 10만원 인출
> 2단계. B 계좌로 10만원 입금
> ➔ 2단계 통신 실패 시, 롤백을 수행해 1단계 인출 건까지 전면 원상복구 조치합니다.
> </aside>
> 
> 파이썬에서 새로운 데이터를 데이터베이스에 영구적으로 안전하게 저장하는 과정입니다.
> 1. `db.add(post)`: 새로운 게시글 객체를 데이터베이스 작업 세션에 올립니다. (임시 저장 상태)
> 2. `db.commit()`: 임시 저장된 데이터를 데이터베이스 파일에 실제 영구 기록하고 작업을 완료합니다.
> 3. `db.refresh(post)`: 데이터베이스에 기록되면서 자동으로 생성된 고유 ID(id)와 작성 시간(created_at)을 파이썬 객체에 다시 동기화해 줍니다.
> 4. `db.rollback()`: 만약 위 작업 도중 에러가 발생하면 임시 저장되었던 내역을 전부 없었던 일로 되돌려 안정성을 유지합니다.
> 
> ```python
> try:
>     post = Post(title="제목", content="내용")
>     db.add(post)      # 1단계. 세션에 임시 추가 (대기 상태)
>     db.commit()       # 2단계. DB에 영구 저장 (최종 승인)
>     db.refresh(post)  # 3단계. DB에서 자동 생성된 값(id 등)을 파이썬 객체에 동기화
> except Exception as e:
>     db.rollback()     # ❌ 예외 발생 시 모든 임시 변경 사항을 전면 취소하고 원래대로 복구
> ```
> 
> ```python
> @app.post("/posts", response_model=PostResponse, status_code=201)
> def create_post(data: PostCreate, db: Session = Depends(get_db)):
>     try:
>         # 입력받은 제목과 내용으로 파이썬 객체 생성
>         post = Post(title=data.title, content=data.content)
>         db.add(post)      # 1단계. 작업 세션 추가
>         db.commit()       # 2단계. DB 영구 저장
>         db.refresh(post)  # 3단계. 자동 생성된 id 등 정보 동기화
>         return post
>     except Exception as e:
>         db.rollback()     # 에러 발생 시 진행중이던 모든 작업 취소
>         raise HTTPException(status_code=500, detail=f"게시글 생성 실패: {str(e)}")
> ```
> 
> ---
> 
> #### 📝 실습 2: POST /posts (게시글 등록) 완성하기
> 
> ```python
> @app.post("/posts", response_model=PostResponse, status_code=201)
> def create_post(data: PostCreate, db: Session = Depends(get_db)):
>     try:
>         post = Post(title=data.title, content=data.content)
>         
>         # ✏️ Q1. 데이터를 세션에 임시 추가하고, 실제 DB에 반영한 뒤 최신 정보를 객체에 동기화하세요.
>         db._______________(post)
>         db._______________()
>         db._______________(post)
>         return post
>     except Exception as e:
>         # ✏️ Q2. 에러가 발생했을 때 DB를 원래 상태로 안전하게 되돌리는 코드를 작성하세요.
>         db._______________()
>         raise HTTPException(status_code=500, detail=f"게시글 생성 실패: {str(e)}")
> ```
> 
> > [!success]- **정답 확인하기**
> > ```python
> > @app.post("/posts", response_model=PostResponse, status_code=201)
> > def create_post(data: PostCreate, db: Session = Depends(get_db)):
> >     try:
> >         post = Post(title=data.title, content=data.content)
> >         db.add(post)      # 트랜잭션에 추가 (아직 DB에 기록되지 않음)
> >         db.commit()       # DB에 영구 반영
> >         db.refresh(post)  # id, created_at 등 DB 자동 생성 값 재조회
> >         return post
> >     except Exception as e:
> >         db.rollback()     # 실패 시 변경사항 전체 취소
> >         raise HTTPException(status_code=500, detail=f"게시글 생성 실패: {str(e)}")
> > ```
> 
> ---
> 
> ### 5️⃣ 데이터 수정 및 삭제 API 학습 및 실습
> 
> #### ① 데이터 수정(Update) 문법 배우기
> ORM 방식의 데이터 수정은 직접 쿼리문을 작성하는 대신 ‘DB에서 꺼내온 객체의 속성값을 직접 대입하여 수정하고 commit’하는 방식으로 처리합니다.
> 이때 SQLAlchemy는 객체의 상태를 추적하고 있다가, 값이 바뀐 것을 감지하고 `db.commit()` 호출 시 자동으로 전용 SQL `UPDATE` 문을 실행해 줍니다.
> 
> ```python
> # 1. 수정 대상을 DB에서 먼저 조회
> post = db.scalar(select(Post).where(Post.id == 1))
> 
> # 2. 파이썬 객체의 속성값을 직접 대입하여 수정
> post.title = "새로운 제목"
> 
> # 3. commit을 하면 SQLAlchemy가 변경 데이터를 감지해 자동으로 DB 값을 갱신합니다.
> db.commit()
> ```
> 
> ---
> 
> #### 📝 실습 3: PUT /posts/{post_id} (게시글 수정) 완성하기
> 
> ```python
> @app.put("/posts/{post_id}", response_model=PostResponse)
> def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
>     post = _get_post_or_none(db, post_id)
>     if not post:
>         raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
>     try:
>         if data.title is not None:
>             post.title = data.title
>         if data.content is not None:
>             post.content = data.content
>             
>         # ✏️ Q1. 변경된 사항을 데이터베이스에 반영하고 최신 정보로 동기화하세요.
>         db._______________()
>         db._______________(post)
>         return post
>     except Exception as e:
>         db.rollback()
>         raise HTTPException(status_code=500, detail=f"게시글 수정 실패: {str(e)}")
> ```
> 
> > [!success]- **정답 확인하기**
> > ```python
> > @app.put("/posts/{post_id}", response_model=PostResponse)
> > def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
> >     post = _get_post_or_none(db, post_id)
> >     if not post:
> >         raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
> >     try:
> >         if data.title is not None:
> >             post.title = data.title
> >         if data.content is not None:
> >             post.content = data.content
> >         db.commit()
> >         db.refresh(post)
> >         return post
> >     except Exception as e:
> >         db.rollback()
> >         raise HTTPException(status_code=500, detail=f"게시글 수정 실패: {str(e)}")
> > ```
> 
> ---
> 
> #### ② 데이터 삭제(Delete) 문법 배우기
> 데이터 삭제는 조회한 객체를 삭제 대상으로 등록하고, 최종적으로 commit 하여 실제 DB에서 지워버립니다.
> 
> ```python
> # 1. 삭제 대상을 DB에서 먼저 조회
> post = db.scalar(select(Post).where(Post.id == 1))
> 
> # 2. 객체를 삭제 대상으로 표시하고 실제 DB에 반영
> db.delete(post)
> db.commit()
> ```
> 
> ---
> 
> #### 📝 실습 4: DELETE /posts/{post_id} (게시글 삭제) 완성하기
> 
> ```python
> @app.delete("/posts/{post_id}", status_code=204)
> def delete_post(post_id: int, db: Session = Depends(get_db)):
>     post = _get_post_or_none(db, post_id)
>     if not post:
>         raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
>     try:
>         # ✏️ Q1. 대상을 삭제 목록에 올리고 데이터베이스에 최종 기록하세요.
>         db._______________(post)
>         db._______________()
>     except Exception as e:
>         db.rollback()
>         raise HTTPException(status_code=500, detail=f"게시글 삭제 실패: {str(e)}")
> ```
> 
> > [!success]- **정답 확인하기**
> > ```python
> > @app.delete("/posts/{post_id}", status_code=204)
> > def delete_post(post_id: int, db: Session = Depends(get_db)):
> >     post = _get_post_or_none(db, post_id)
> >     if not post:
> >         raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
> >     try:
> >         db.delete(post)  # 삭제 대상으로 표시
> >         db.commit()      # DB에서 영구 삭제
> >     except Exception as e:
> >         db.rollback()
> >         raise HTTPException(status_code=500, detail=f"게시글 삭제 실패: {str(e)}")
> > ```

---

## 🔄 18. End-to-End 흐름 확인

> [!note]- 📚 18. End-to-End 흐름 확인 내용 보기
> 
> ### 1️⃣ 프로젝트 구조
> 
> ```
> fullstack-practice/
> ├── frontend/                    # Next.js 앱
> │   ├── app/
> │   │   ├── layout.tsx           # 공통 레이아웃 (네비게이션 등)
> │   │   ├── page.tsx             # / → /posts 리다이렉트
> │   │   ├── actions.ts           # Server Action (서버에서 API 호출)
> │   │   └── posts/
> │   │       ├── page.tsx             # 게시글 목록
> │   │       ├── new/page.tsx         # 새 글 작성 폼
> │   │       └── [postId]/
> │   │           ├── page.tsx         # 게시글 상세
> │   │           └── edit/page.tsx    # 수정 폼
> │   └── .env.local           # FASTAPI_URL=http://localhost:8000
> │
> └── backend/                     # FastAPI 앱
>     ├── main.py              # API 엔드포인트 + SQLAlchemy 모델
>     └── blog.db              # SQLite DB 파일 (자동 생성)
> ```
> 
> ---
> 
> ### 2️⃣ 전체 요청 흐름
> 
> 새 게시글을 작성할 때 일어나는 일을 단계별로 살펴봅니다.
> 
> ```
> [1] 브라우저
>      └─ 사용자가 /posts/new 폼에 제목과 내용을 입력하고 추가 버튼 클릭
> 
> [2] Next.js Server Action (actions.ts)
>      └─ createPost(formData) 함수가 서버에서 실행
>      └─ fetch("http://localhost:8000/posts", { method: "POST", body: JSON.stringify({title, content}) })
> 
> [3] FastAPI (main.py)
>      └─ POST /posts 엔드포인트 실행
>      └─ Pydantic으로 요청 데이터 유효성 검증
> 
> [4] SQLAlchemy
>      └─ Post 객체 생성 → db.add() → db.commit() → db.refresh()
> 
> [5] SQLite DB (blog.db)
>      └─ INSERT INTO posts (title, content, created_at) VALUES (...)
> 
> [6] 응답 반환
>      └─ PostResponse JSON 반환
>      └─ revalidateTag("posts-list") → /posts 리다이렉트
> 
> [7] 브라우저
>      └─ 목록 페이지에서 새 게시글 확인 ✅
> ```
> 
> #### 💡 Server Action을 쓰면 CORS 에러가 발생하지 않는 이유
> 브라우저는 보안상 **다른 출처(도메인/포트)로의 요청**을 기본으로 차단합니다. 이를 CORS(Cross-Origin Resource Sharing) 정책이라고 합니다.
> 현재 구조에서는 브라우저가 아니라 **Next.js 서버가 직접 FastAPI 서버(8000번)로 데이터를 요청**합니다. 즉, 브라우저가 개입하지 않는 '서버 간 통신'이기 때문에 CORS 설정을 백엔드에 하지 않아도 에러 없이 잘 작동합니다.
> 
> ---
> 
> ### 3️⃣ 프로젝트 실행하기
> 
> **백엔드 실행**
> ```bash
> cd fullstack-practice/backend
> 
> # 1. 필요한 라이브러리 설치
> uv pip install -r requirements.txt
> 
> # 2. 백엔드 서버 개발 모드로 구동하기
> uv run fastapi dev main.py
> 
> # → http://localhost:8000 에서 실행됩니다.
> # → http://localhost:8000/docs 에서 API 명세서(Swagger UI)를 볼 수 있습니다.
> ```
> 
> **프론트엔드 실행 (새 터미널)**
> ```bash
> cd fullstack-practice/frontend
> npm install
> npm run dev
> # → http://localhost:3000 에서 실행
> ```
> 
> **환경 변수 확인**
> `frontend/.env.local` 파일을 만들고 아래 내용을 기입합니다.
> ```
> FASTAPI_URL=http://localhost:8000
> ```
> 
> **직접 확인하기**
> 1. 백엔드와 프론트엔드를 모두 실행합니다.
> 2. `http://localhost:3000`에서 새 게시글을 작성하고 확인합니다.
> 3. 게시글을 수정하고 삭제해봅니다.
> 4. Swagger UI에서 DB가 실제로 변경되는 것을 확인합니다.
> 
> ---
> 
> ### ✅ 4주차 지금까지 배운 내용 정리
> 
> **Next.js(프론트) ➔ Server Action ➔ FastAPI(백엔드) ➔ SQLAlchemy ➔ SQLite(DB)**
> 
> | 계층 | 역할 | 기술 |
> | --- | --- | --- |
> | **프론트엔드** | 사용자 화면, 폼 입력 | Next.js |
> | **Server Action** | 서버에서 API 호출, 캐시 관리 | Next.js (actions.ts) |
> | **백엔드 API** | 요청 처리, 비즈니스 로직 | FastAPI |
> | **ORM** | Python ↔ DB 변환 | SQLAlchemy |
> | **데이터베이스** | 데이터 영구 저장 | SQLite |
