---

## 🔎 19. 풀스택 통합 실습 복습

> [!note]- 📚 19. 풀스택 통합 실습 복습 내용 보기
>
> ### 1️⃣ 실습 목표
>
> 클라이언트 컴포넌트에서 검색어를 입력하면, 전체 게시글 목록을 가져온 뒤 검색어 기준으로 실시간 필터링되는 화면을 구현합니다.
>
> ```
> 전체 데이터 조회 → 검색어 입력 → title/content 기준 필터링 → 화면 갱신
> ```
>
> 이번 실습에서는 같은 검색 기능을 두 가지 방식으로 구현합니다.
>
> | 방식 | 호출 흐름 | 특징 |
> | --- | --- | --- |
> | **Direct Fetch** | 브라우저 → FastAPI | 구조가 단순하지만 백엔드 주소가 브라우저에 노출되고 CORS 설정이 필요합니다. |
> | **Route Handler** | 브라우저 → Next.js `/api/search` → FastAPI | 백엔드 주소가 노출되지 않고, 서버 간 통신이므로 CORS 문제를 줄일 수 있습니다. |
>
> ---
>
> ### 2️⃣ Direct Fetch 방식
>
> Direct Fetch는 Client Component가 브라우저에서 직접 FastAPI 서버를 호출하는 방식입니다.
>
> ```
> 브라우저
>   ↓
> NEXT_PUBLIC_FASTAPI_URL/posts
>   ↓
> FastAPI
> ```
>
> ```tsx
> useEffect(() => {
>   setLoading(true);
>   setError(null);
>
>   fetch(`${process.env.NEXT_PUBLIC_FASTAPI_URL}/posts`)
>     .then((res) => {
>       if (!res.ok) throw new Error("데이터를 불러오는 데 실패했습니다");
>       return res.json();
>     })
>     .then((data) => setResults(data))
>     .catch((err) => setError(err.message))
>     .finally(() => setLoading(false));
> }, []);
> ```
>
> #### `NEXT_PUBLIC_` 접두사의 의미
>
> Next.js의 환경변수는 기본적으로 서버에서만 읽을 수 있습니다. 하지만 Client Component는 브라우저에서 실행되므로, 브라우저가 직접 API 주소를 호출하려면 해당 값이 클라이언트 코드에 노출되어야 합니다.
>
> | 환경변수 | 사용 위치 | 노출 여부 |
> | --- | --- | --- |
> | `FASTAPI_URL` | 서버 전용 | 브라우저에 노출되지 않음 |
> | `NEXT_PUBLIC_FASTAPI_URL` | 클라이언트에서도 사용 가능 | 브라우저에 노출됨 |
>
> <aside>
> ⚠️ `NEXT_PUBLIC_`이 붙은 값은 브라우저 번들에 포함됩니다. API 서버 주소처럼 공개되어도 괜찮은 값에만 사용하고, 비밀키나 토큰에는 절대 사용하지 않습니다.
> </aside>
>
> ---
>
> ### 3️⃣ Route Handler 방식
>
> Route Handler 방식은 브라우저가 FastAPI를 직접 호출하지 않고, Next.js 서버의 API 경로를 먼저 호출하는 구조입니다.
>
> ```
> 브라우저
>   ↓
> /api/search
>   ↓
> Next.js Route Handler
>   ↓
> FASTAPI_URL/posts
>   ↓
> FastAPI
> ```
>
> 이 방식에서는 FastAPI 주소를 `FASTAPI_URL`이라는 서버 전용 환경변수로 관리할 수 있습니다.
>
> ```tsx
> useEffect(() => {
>   setLoading(true);
>   setError(null);
>
>   fetch(`${BASE_PATH}/api/search`)
>     .then((res) => {
>       if (!res.ok) throw new Error("데이터를 불러오는 데 실패했습니다");
>       return res.json();
>     })
>     .then((data) => setResults(data))
>     .catch((err) => setError(err.message))
>     .finally(() => setLoading(false));
> }, []);
> ```
>
> #### `app/api/search/route.ts`
>
> ```tsx
> import { NextResponse } from "next/server";
>
> export async function GET() {
>   const fastapiUrl = process.env.FASTAPI_URL;
>
>   if (!fastapiUrl) {
>     return NextResponse.json(
>       { detail: "FASTAPI_URL 환경 변수가 설정되지 않았습니다" },
>       { status: 500 }
>     );
>   }
>
>   const res = await fetch(`${fastapiUrl}/posts`);
>
>   if (!res.ok) {
>     return NextResponse.json(
>       { detail: "게시글 목록을 불러오는 데 실패했습니다" },
>       { status: res.status }
>     );
>   }
>
>   const data = await res.json();
>   return NextResponse.json(data);
> }
> ```
>
> ---
>
> ### 4️⃣ 검색 필터링 로직
>
> 검색어는 서버에 다시 요청하지 않고, 이미 가져온 `results` 배열을 클라이언트에서 필터링합니다.
>
> ```tsx
> const filtered: Post[] = results.filter(
>   (post) =>
>     post.title.includes(query) || post.content.includes(query)
> );
> ```
>
> | 상태 | 화면 표시 |
> | --- | --- |
> | `loading === true` | `불러오는 중...` |
> | `error !== null` | 에러 메시지 |
> | 결과 없음 + 검색어 있음 | `검색 결과가 없습니다.` |
> | 결과 없음 + 검색어 없음 | `게시글이 없습니다.` |
> | 결과 있음 | 게시글 목록 렌더링 |
>
> ---
>
> ### 5️⃣ Fetch 기반 구현 비교
>
> | 구분 | Direct Fetch | Route Handler |
> | --- | --- | --- |
> | **호출 주소** | `NEXT_PUBLIC_FASTAPI_URL/posts` | `/api/search` |
> | **통신 흐름** | 브라우저 → FastAPI | 브라우저 → Next.js 서버 → FastAPI |
> | **환경변수** | `NEXT_PUBLIC_FASTAPI_URL` | `FASTAPI_URL` |
> | **브라우저 주소 노출** | 노출됨 | 노출되지 않음 |
> | **CORS 필요 여부** | 필요 | 일반적으로 불필요 |
> | **구현 난이도** | 낮음 | 중간 |
>
> <aside>
> 📌 실무에서는 백엔드 주소나 인증 흐름을 숨기고 싶을 때 Route Handler 방식이 더 적합합니다. 단순 실습이나 내부 도구에서는 Direct Fetch가 더 빠르게 구현될 수 있습니다.
> </aside>
>
> ---
>
> ### 6️⃣ axios 리팩토링
>
> Fetch로 작성한 검색 요청과 삭제 요청을 axios로 교체합니다.
>
> ```bash
> cd fullstack-practice/frontend
> npm install axios
> ```
>
> #### Fetch와 axios 차이
>
> | 비교 항목 | Fetch | Axios |
> | --- | --- | --- |
> | JSON 변환 | `await res.json()` 필요 | `response.data`로 바로 접근 |
> | HTTP 에러 처리 | `if (!res.ok)` 직접 체크 필요 | 2xx가 아니면 자동으로 `catch` 이동 |
> | 에러 상세 메시지 | 응답 바디를 직접 파싱해야 함 | `err.response?.data?.detail`로 접근 |
> | 메서드 표현 | `fetch(url, { method: "DELETE" })` | `axios.delete(url)` |
>
> ---
>
> ### 7️⃣ `search/page.tsx` axios 리팩토링
>
> ```tsx
> "use client";
>
> import { useState, useEffect } from "react";
> import Link from "next/link";
> import axios from "axios";
>
> type Post = {
>   id: number;
>   title: string;
>   content: string;
>   created_at: string;
> };
>
> export default function SearchPage() {
>   const [query, setQuery] = useState<string>("");
>   const [results, setResults] = useState<Post[]>([]);
>   const [loading, setLoading] = useState<boolean>(false);
>   const [error, setError] = useState<string | null>(null);
>
>   const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
>
>   useEffect(() => {
>     async function fetchPosts() {
>       setLoading(true);
>       setError(null);
>
>       try {
>         const res = await axios.get<Post[]>(`${BASE_PATH}/api/search`);
>         setResults(res.data);
>       } catch (err) {
>         if (axios.isAxiosError(err)) {
>           setError(err.response?.data?.detail ?? "게시글을 불러오는 데 실패했습니다");
>         } else {
>           setError("알 수 없는 오류가 발생했습니다");
>         }
>       } finally {
>         setLoading(false);
>       }
>     }
>
>     fetchPosts();
>   }, []);
>
>   const filtered = results.filter(
>     (post) => post.title.includes(query) || post.content.includes(query)
>   );
>
>   return (
>     <main>
>       <div className="flex items-center gap-3 mb-6">
>         <Link href={`${BASE_PATH}/posts`} className="text-gray-400 hover:text-gray-600 text-sm">
>           ← 목록으로
>         </Link>
>         <h1 className="text-2xl font-bold text-gray-900">검색</h1>
>       </div>
>
>       <input
>         type="text"
>         value={query}
>         onChange={(e) => setQuery(e.target.value)}
>         placeholder="제목 또는 내용으로 검색하세요"
>         className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
>       />
>
>       {loading && <p className="text-center text-gray-400 py-10">불러오는 중...</p>}
>       {error && <p className="text-center text-red-500 py-10">{error}</p>}
>
>       {!loading && !error && filtered.length === 0 && (
>         <p className="text-center text-gray-400 py-10">
>           {query ? "검색 결과가 없습니다." : "게시글이 없습니다."}
>         </p>
>       )}
>
>       {!loading && !error && filtered.length > 0 && (
>         <ul className="space-y-3">
>           {filtered.map((post) => (
>             <li key={post.id}>
>               <Link
>                 href={`${BASE_PATH}/posts/${post.id}`}
>                 className="block bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-400 hover:shadow-sm transition-all"
>               >
>                 <p className="font-medium text-gray-900">{post.title}</p>
>                 <p className="text-sm text-gray-500 mt-1 line-clamp-2">{post.content}</p>
>                 <p className="text-xs text-gray-400 mt-2">
>                   {new Date(post.created_at).toLocaleDateString("ko-KR")}
>                 </p>
>               </Link>
>             </li>
>           ))}
>         </ul>
>       )}
>     </main>
>   );
> }
> ```
>
> ---
>
> ### 8️⃣ `DeleteButton.tsx` axios 리팩토링
>
> ```tsx
> "use client";
>
> import axios from "axios";
>
> export default function DeleteButton({ postId }: { postId: number }) {
>   const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
>
>   async function handleDelete() {
>     if (!confirm("정말 삭제할까요?")) return;
>
>     try {
>       await axios.delete(`${BASE_PATH}/api/posts/${postId}`);
>       window.location.href = `${BASE_PATH}/posts`;
>     } catch (err) {
>       if (axios.isAxiosError(err)) {
>         alert(err.response?.data?.detail ?? "게시글 삭제에 실패했습니다");
>       } else {
>         alert("알 수 없는 오류가 발생했습니다");
>       }
>     }
>   }
>
>   return (
>     <button
>       onClick={handleDelete}
>       className="bg-red-500 text-white text-sm px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
>     >
>       삭제하기
>     </button>
>   );
> }
> ```
>
> <aside>
> ✅ axios 리팩토링의 핵심은 `res.ok`와 `res.json()`을 직접 처리하던 코드를 줄이고, 성공은 `res.data`, 실패는 `catch`에서 일관되게 다루는 것입니다.
> </aside>

---

## 🚀 20. Vercel & Railway 소개 및 배포

> [!note]- 📚 20. Vercel & Railway 소개 및 배포 내용 보기
>
> ### 1️⃣ 오늘의 목표
>
> 로컬에서만 실행되던 풀스택 앱을 실제 공개 URL로 배포합니다.
>
> ```
> 로컬 개발
> - Frontend: http://localhost:3000
> - Backend:  http://localhost:8000
>
> 배포 후
> - Frontend: https://your-project.vercel.app
> - Backend:  https://your-app.up.railway.app
> ```
>
> 배포 대상 프로젝트는 `fullstack-practice`입니다.
>
> ```text
> fullstack-practice/
> ├── frontend/    ← Vercel에 배포
> └── backend/     ← Railway에 배포
> ```
>
> 배포 흐름은 다음과 같습니다.
>
> ```text
> 1단계: Railway에 FastAPI 백엔드 배포
> 2단계: Vercel에 Next.js 프론트엔드 배포
> 3단계: Vercel 환경변수에 Railway 백엔드 URL 등록
> 4단계: Railway CORS 설정에 Vercel URL 등록
> ```
>
> ---
>
> ### 2️⃣ Vercel이란?
>
> [Vercel](https://vercel.com/)은 Next.js 애플리케이션을 가장 쉽게 배포할 수 있는 플랫폼입니다. Next.js를 만든 회사가 운영하기 때문에 Next.js와의 호환성이 좋습니다.
>
> | 특징 | 내용 |
> | --- | --- |
> | **무료 플랜** | 개인 프로젝트를 무료로 배포할 수 있습니다. |
> | **자동 배포** | GitHub에 push하면 자동으로 다시 배포됩니다. |
> | **Preview 배포** | PR을 열면 미리보기 URL이 자동으로 생성됩니다. |
> | **배포 URL** | `https://your-project.vercel.app` 형태의 URL이 생성됩니다. |
>
> ---
>
> ### 3️⃣ Railway란?
>
> [Railway](https://railway.com/)는 FastAPI 같은 백엔드 서버를 컨테이너 기반으로 배포할 수 있는 호스팅 서비스입니다.
>
> | 구분 | 로컬 개발 | Railway 배포 |
> | --- | --- | --- |
> | **접근 가능 범위** | 내 컴퓨터에서만 접근 가능 | 전 세계에서 공개 URL로 접근 가능 |
> | **FastAPI 주소** | `http://localhost:8000` | `https://xxx.up.railway.app` |
> | **Vercel에서 호출 가능 여부** | 불가능 | 가능 |
> | **SQLite 유지** | 로컬 파일로 유지 | 서버 재시작 전까지 유지 |
>
> <aside>
> 📌 Vercel은 서버리스 환경이라 SQLite 파일처럼 서버 파일 시스템에 직접 의존하는 구조와 잘 맞지 않습니다. 이번 실습에서는 FastAPI와 SQLite를 Railway에 배포하고, Next.js만 Vercel에 배포합니다.
> </aside>
>
> ---
>
> ### 4️⃣ 사전 준비: GitHub 레포지토리 생성
>
> 배포 플랫폼은 GitHub 레포지토리와 연결해 코드를 가져옵니다. 따라서 먼저 프로젝트를 GitHub에 push해야 합니다.
>
> ```bash
> cd fullstack-practice
>
> git init
> git add .
> git commit -m "initial commit"
> git branch -M main
>
> git remote add origin https://github.com/{username}/fullstack-practice
> git push -u origin main
> ```
>
> ---
>
> ### 5️⃣ Railway로 FastAPI 백엔드 배포
>
> #### 단계 1. Railway 프로젝트 생성
>
> ```text
> 1. Railway 가입
> 2. GitHub 로그인 및 코드 접근 허용
> 3. Add Service → GitHub Repo 선택
> 4. fullstack-practice 레포지토리 선택
> ```
>
> #### 단계 2. 백엔드 서비스 설정
>
> | 설정 위치 | 입력값 |
> | --- | --- |
> | **Settings → Root Directory** | `backend` |
> | **Deploy → Start Command** | `fastapi run main.py --host 0.0.0.0 --port $PORT` |
> | **Variables** | 프론트엔드 URL 관련 환경변수 추가 |
>
> Railway는 실행 포트를 직접 정하지 않고 `$PORT` 환경변수로 전달합니다. 따라서 Start Command에서 `--port $PORT`를 사용해야 합니다.
>
> #### 단계 3. Railway 도메인 생성
>
> ```text
> Settings → Networking → Generate Domain 클릭
> ```
>
> 생성된 URL 예시는 다음과 같습니다.
>
> ```text
> https://next-js-fullstack-production.up.railway.app
> ```
>
> 이 URL은 나중에 Vercel의 `FASTAPI_URL` 환경변수 값으로 사용합니다.
>
> ---
>
> ### 6️⃣ FastAPI CORS 설정
>
> 배포 전에는 FastAPI가 로컬 프론트엔드만 허용하고 있을 수 있습니다. Vercel에 배포된 프론트엔드에서도 API를 호출할 수 있도록 CORS 설정을 수정합니다.
>
> ```python
> import os
>
> from fastapi import FastAPI
> from fastapi.middleware.cors import CORSMiddleware
>
> app = FastAPI(title="Blog API")
>
> FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
>
> origins = [
>     "http://localhost:3000",
>     FRONTEND_URL,
> ]
>
> app.add_middleware(
>     CORSMiddleware,
>     allow_origins=origins,
>     allow_credentials=True,
>     allow_methods=["*"],
>     allow_headers=["*"],
> )
> ```
>
> <aside>
> ⚠️ 실습 중 빠르게 확인해야 할 때는 `allow_origins=["*"]`로 임시 처리할 수 있지만, 실무에서는 허용할 프론트엔드 도메인을 명시하는 방식이 안전합니다.
> </aside>
>
> ---
>
> ### 7️⃣ Vercel로 Next.js 프론트엔드 배포
>
> #### 단계 1. Vercel 프로젝트 가져오기
>
> ```text
> 1. Vercel 가입
> 2. Add New Project
> 3. GitHub 레포지토리 선택
> 4. Root Directory를 frontend로 설정
> ```
>
> #### 단계 2. 환경변수 설정
>
> Vercel의 Environment Variables에 다음 값을 추가합니다.
>
> ```text
> FASTAPI_URL=https://your-app.up.railway.app
> ```
>
> `FASTAPI_URL`은 Next.js 서버에서 Route Handler가 사용하는 값입니다. 브라우저에 노출할 필요가 없으므로 `NEXT_PUBLIC_` 접두사를 붙이지 않습니다.
>
> #### 단계 3. 배포
>
> ```text
> Deploy 클릭
> → 빌드 로그 확인
> → https://your-project.vercel.app URL 생성
> ```
>
> ---
>
> ### 8️⃣ Railway CORS에 Vercel URL 등록
>
> Vercel 배포가 끝나면 생성된 프론트엔드 URL을 Railway 환경변수에 반영합니다.
>
> ```text
> Railway 대시보드
> → backend 서비스
> → Variables
> → FRONTEND_URL=https://your-project.vercel.app
> → Redeploy
> ```
>
> 강의에서 `CORS_ORIGINS`처럼 여러 도메인을 쉼표로 관리하는 방식으로 구현했다면 다음처럼 넣을 수 있습니다.
>
> ```text
> CORS_ORIGINS=https://your-project.vercel.app,http://localhost:3000
> ```
>
> 중요한 점은 FastAPI 코드에서 실제로 읽는 환경변수 이름과 Railway에 등록한 환경변수 이름이 일치해야 한다는 것입니다.
>
> ---
>
> ### 9️⃣ 배포 후 확인 체크리스트
>
> | 확인 항목 | 정상 기준 |
> | --- | --- |
> | **Vercel URL 접속** | 프론트엔드 페이지가 로드됩니다. |
> | **Railway URL `/docs` 접속** | FastAPI Swagger UI가 표시됩니다. |
> | **게시글 목록 조회** | Vercel 앱에서 Railway 데이터를 불러옵니다. |
> | **검색 기능** | 검색어 입력 시 게시글 목록이 필터링됩니다. |
>
> ---
>
> ### 🔧 공통 트러블슈팅
>
> #### 500 에러 또는 응답 없음
>
> ```text
> Railway 로그 확인
> - FastAPI 실행 실패 여부
> - requirements.txt 누락 여부
> - Start Command 오타 여부
> - blog.db 생성 여부
> ```
>
> #### CORS 에러
>
> ```text
> Railway Variables 확인
> - Vercel URL이 등록되어 있는지
> - http / https가 정확한지
> - 환경변수 변경 후 Redeploy 했는지
> ```
>
> #### Vercel에서 게시글 목록이 비어 있음
>
> ```text
> Vercel 환경변수 확인
> - FASTAPI_URL 값이 Railway URL인지
> - /posts까지 붙이지 않고 도메인까지만 넣었는지
> - 환경변수 변경 후 Redeploy 했는지
> ```
>
> ---
>
> ### ✅ 배포 실습 순서 요약
>
> ```text
> 1. fullstack-practice 폴더를 GitHub에 push
> 2. Railway에서 backend 디렉토리로 FastAPI 배포
> 3. Railway 도메인 생성
> 4. FastAPI CORS 설정 수정
> 5. Vercel에서 frontend 디렉토리로 Next.js 배포
> 6. Vercel 환경변수 FASTAPI_URL에 Railway URL 입력
> 7. Railway CORS 설정에 Vercel URL 추가
> 8. Vercel 앱에서 게시글 목록과 검색 기능 확인
> ```

---

## ✅ 21. E2E 검증 & Docker/AWS 개요

> [!note]- 📚 21. E2E 검증 & Docker/AWS 개요 내용 보기
>
> ### 1️⃣ E2E 검증이란?
>
> E2E(End-to-End) 검증은 사용자의 실제 행동 흐름을 처음부터 끝까지 따라가며, 프론트엔드·백엔드·DB가 함께 정상 동작하는지 확인하는 과정입니다.
>
> 로컬에서는 모든 것이 내 컴퓨터 안에서 실행됩니다.
>
> ```text
> Browser → localhost:3000 → localhost:8000 → local blog.db
> ```
>
> 배포 후에는 서로 다른 서버가 통신합니다.
>
> ```text
> Browser
>   ↓
> Vercel Frontend
>   ↓
> Railway FastAPI
>   ↓
> SQLite blog.db
> ```
>
> 따라서 배포 후에는 단순히 페이지가 열리는지만 보는 것이 아니라, 실제 사용 흐름 전체를 검증해야 합니다.
>
> ---
>
> ### 2️⃣ 사용자 시나리오 체크리스트
>
> #### ① 게시글 작성: POST
>
> ```text
> 1. https://your-project.vercel.app/posts/new 접속
> 2. 제목과 내용 입력
> 3. "작성하기" 클릭
> 4. 목록 페이지로 자동 이동되는지 확인
> 5. 방금 작성한 게시글이 목록에 나타나는지 확인
> ```
>
> 검증 포인트:
>
> ```text
> Client Form
> → Next.js Server Action 또는 Route Handler
> → Railway FastAPI POST /posts
> → SQLite 저장
> → 목록 화면 반영
> ```
>
> #### ② 게시글 조회: GET
>
> ```text
> 1. 목록에서 방금 작성한 게시글 클릭
> 2. 상세 페이지 화면 확인
> 3. Railway URL/docs 접속
> 4. GET /posts 실행
> 5. Swagger UI에서도 같은 게시글이 보이는지 확인
> ```
>
> #### ③ 검색: Query / Filtering
>
> ```text
> 1. https://your-project.vercel.app/search 접속
> 2. 검색어 입력
> 3. 검색 결과가 필터링되는지 확인
> 4. 새로고침 후에도 의도한 검색 상태가 유지되는지 확인
> ```
>
> 강의 시나리오에서 URL이 `/search?q=Next`로 변경되는 구조라면, 검색어를 URL 쿼리 파라미터에 반영해야 새로고침 후에도 상태가 유지됩니다.
>
> #### ④ 게시글 수정: PUT
>
> ```text
> 1. 게시글 상세 페이지 접속
> 2. "수정하기" 클릭
> 3. 제목 또는 내용 변경
> 4. 저장
> 5. 변경된 내용이 상세 화면과 목록에 반영되는지 확인
> ```
>
> #### ⑤ 게시글 삭제: DELETE
>
> ```text
> 1. 상세 페이지에서 삭제 버튼 클릭
> 2. confirm 승인
> 3. 목록 페이지로 리다이렉트되는지 확인
> 4. 삭제한 게시글이 목록에서 사라졌는지 확인
> 5. Railway /docs의 GET /posts 결과에서도 삭제되었는지 확인
> ```
>
> ---
>
> ### 3️⃣ Railway Swagger UI로 DB 상태 확인
>
> Railway 백엔드 URL 뒤에 `/docs`를 붙이면 FastAPI Swagger UI에 접속할 수 있습니다.
>
> ```text
> https://your-app.up.railway.app/docs
> ```
>
> 여기에서 `GET /posts`를 실행하면, Vercel 앱에서 작성한 게시글이 실제 Railway 서버의 DB에 저장되었는지 확인할 수 있습니다.
>
> <aside>
> 📌 브라우저 화면은 Next.js가 렌더링한 결과이고, `/docs`는 FastAPI 서버가 직접 보여주는 API 문서입니다. 두 곳에서 같은 데이터가 보이면 프론트엔드와 백엔드 통신, DB 저장 흐름이 모두 연결된 것입니다.
> </aside>
>
> ---
>
> ### 4️⃣ Vercel + Railway vs Docker + AWS
>
> 이번 주에는 빠른 배포를 위해 Vercel과 Railway를 사용했습니다. 다음 주에는 Docker와 AWS를 활용해 더 직접적인 서버 배포 방식을 학습합니다.
>
> | 구분 | Vercel + Railway | Docker + AWS |
> | --- | --- | --- |
> | **난이도** | 낮음 | 높음 |
> | **설정 시간** | 10~15분 | 1~3시간 |
> | **컨트롤** | 플랫폼 규칙 안에서 제한적 | 서버 환경을 직접 제어 |
> | **비용** | 무료 플랜 존재 | 인프라 비용 발생 |
> | **스케일링** | 플랫폼이 자동 처리 | ECS, ALB, ASG 등을 직접 구성 |
> | **DB** | SQLite 실습 가능 | RDS/PostgreSQL을 주로 사용 |
> | **모니터링** | Vercel Analytics 등 | CloudWatch, Prometheus 등 |
> | **적합한 상황** | 사이드 프로젝트, 빠른 MVP | 팀 서비스, 고트래픽 서비스, 실무형 인프라 |
>
> ---
>
> ### 5️⃣ Vercel의 한계
>
> Vercel은 프론트엔드 배포에는 매우 편리하지만, 모든 백엔드 워크로드에 적합한 것은 아닙니다.
>
> | 한계 | 설명 |
> | --- | --- |
> | **실행 시간 제한** | 서버리스 함수는 장시간 실행 작업에 부적합합니다. |
> | **실행 환경 제약** | ML 모델 서빙, 대용량 연산, 특수 시스템 패키지 사용이 어렵습니다. |
> | **파일 시스템 제약** | SQLite처럼 파일 저장에 의존하는 DB와 맞지 않습니다. |
> | **인프라 접근 제한** | 서버 튜닝, 네트워크 설정, 런타임 구성을 세밀하게 제어하기 어렵습니다. |
>
> Docker + AWS가 필요한 대표적인 상황은 다음과 같습니다.
>
> ```text
> - 매일 1만 명 이상 사용하는 B2B SaaS
> - 기업 보안 정책과 감사 로그가 필요한 서비스
> - ML 모델 서빙 또는 대용량 연산
> - WebSocket 기반 실시간 기능
> - PostgreSQL 등 별도 DB와 수백 GB 이상 데이터 운영
> ```
>
> ---
>
> ### 6️⃣ SQLite의 한계
>
> SQLite는 파일 기반 DB이기 때문에 학습용이나 작은 서비스에는 간단하고 편리합니다. 하지만 트래픽이 많거나 서버를 여러 대로 늘리는 환경에는 한계가 있습니다.
>
> | 한계 | 설명 |
> | --- | --- |
> | **파일 기반 저장** | 여러 서버가 하나의 DB 파일을 안정적으로 공유하기 어렵습니다. |
> | **쓰기 충돌 가능성** | 동시에 많은 쓰기 요청이 들어오면 병목이 생길 수 있습니다. |
> | **수평 확장 어려움** | 서버 인스턴스를 늘려도 DB 파일을 함께 공유하기 어렵습니다. |
>
> 프로덕션 환경에서는 보통 PostgreSQL, MySQL 같은 네트워크 기반 DB를 사용합니다.
>
> ---
>
> ### 7️⃣ 1~4주차 학습 흐름 정리
>
> ```text
> 1주차~3주차
> - Python
> - FastAPI
> - SQLite
> - SQLAlchemy
> - React 기초
>
> 4주차
> - Next.js App Router
> - Server Component / Client Component
> - Server Actions
> - Route Handler
> - FastAPI 연동
> - Vercel + Railway 배포
> ```
>
> 다음 주에는 같은 앱을 Docker로 컨테이너화하고, AWS EC2에 직접 배포하는 흐름을 학습합니다.
>
> | 항목 | Vercel/Railway | Docker/AWS |
> | --- | --- | --- |
> | **인프라 관리** | 플랫폼이 관리 | 직접 관리 |
> | **컨테이너** | 직접 다루지 않음 | Docker 이미지로 패키징 |
> | **배포 방식** | Git push 기반 자동 배포 | 이미지 빌드 후 서버에서 실행 |
> | **학습 목표** | 클라우드 플랫폼 활용 이해 | DevOps 기본 실무 능력 확보 |
>
> ---
>
> ### ✅ Day5 핵심 요약
>
> ```text
> 1. 검색 기능은 Client Component에서 상태와 필터링으로 구현할 수 있습니다.
> 2. Direct Fetch는 단순하지만 백엔드 주소 노출과 CORS 설정이 필요합니다.
> 3. Route Handler는 Next.js 서버가 FastAPI 호출을 대리하는 프록시 역할을 합니다.
> 4. axios는 JSON 변환과 HTTP 에러 처리를 더 간결하게 만듭니다.
> 5. Vercel에는 Next.js 프론트엔드, Railway에는 FastAPI 백엔드를 배포합니다.
> 6. 배포 후에는 POST, GET, 검색, PUT, DELETE 흐름을 E2E로 검증해야 합니다.
> 7. Vercel/Railway는 빠른 MVP에 좋고, Docker/AWS는 더 많은 제어가 필요한 실무 환경에 적합합니다.
> ```
