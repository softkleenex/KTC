---

## 01. 검색 기능 구현 방식

풀스택 통합 실습에서는 게시글 목록을 가져온 뒤 검색어 기준으로 필터링하는 기능을 구현했다.

```text
전체 게시글 조회
  → 검색어 입력
  → title/content 기준 필터링
  → 화면 갱신
```

검색 데이터를 가져오는 방식은 크게 두 가지로 비교했다.

| 방식 | 호출 흐름 | 특징 |
| --- | --- | --- |
| Direct Fetch | 브라우저 → FastAPI | 단순하지만 백엔드 주소가 노출되고 CORS 설정 필요 |
| Route Handler | 브라우저 → Next.js `/api/search` → FastAPI | 백엔드 주소 노출을 줄이고 CORS 부담 감소 |

---

## 02. Direct Fetch와 NEXT_PUBLIC_

Client Component에서 FastAPI를 직접 호출하려면 브라우저가 API 주소를 알아야 한다. Next.js에서 브라우저에 노출할 환경변수는 `NEXT_PUBLIC_` 접두사를 붙인다.

```env
NEXT_PUBLIC_FASTAPI_URL=http://localhost:8000
```

```tsx
useEffect(() => {
  fetch(`${process.env.NEXT_PUBLIC_FASTAPI_URL}/posts`)
    .then((res) => res.json())
    .then((data) => setResults(data));
}, []);
```

`NEXT_PUBLIC_`은 편리하지만 말 그대로 공개되는 값이다. API 서버 주소처럼 공개되어도 되는 값에는 사용할 수 있지만, 비밀번호나 토큰에는 사용하면 안 된다.

---

## 03. Route Handler 방식

Route Handler 방식은 브라우저가 FastAPI를 직접 호출하지 않고 Next.js 서버의 API 경로를 먼저 호출한다.

```text
브라우저
  → /api/search
  → Next.js Route Handler
  → FASTAPI_URL/posts
  → FastAPI
```

이때 FastAPI 주소는 서버 전용 환경변수로 관리한다.

```env
FASTAPI_URL=http://localhost:8000
```

```tsx
// app/api/search/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  const fastapiUrl = process.env.FASTAPI_URL;

  if (!fastapiUrl) {
    return NextResponse.json(
      { detail: "FASTAPI_URL 환경 변수가 설정되지 않았습니다" },
      { status: 500 }
    );
  }

  const res = await fetch(`${fastapiUrl}/posts`);
  const data = await res.json();
  return NextResponse.json(data);
}
```

이 구조에서는 브라우저가 보는 주소가 `/api/search`로 고정된다. 실제 백엔드 주소는 Next.js 서버 안쪽에 숨겨진다.

---

## 04. Vercel과 Railway 배포

4주차 배포 실습에서는 프론트엔드는 Vercel, 백엔드는 Railway에 올렸다.

```text
사용자 브라우저
  → Vercel의 Next.js 앱
  → Railway의 FastAPI 서버
  → SQLite DB
```

| 서비스 | 담당 |
| --- | --- |
| Vercel | Next.js 프론트엔드 배포 |
| Railway | FastAPI 백엔드 실행 |
| GitHub | 배포 소스 저장소 |
| 환경변수 | 배포 환경별 API 주소 관리 |

로컬에서는 `localhost:3000`, `localhost:8000`으로 통신했지만 배포 후에는 Vercel URL과 Railway URL이 서로 통신한다. 그래서 배포 환경에서는 환경변수 값을 로컬 주소가 아니라 실제 공개 URL로 바꿔야 한다.

---

## 05. E2E 검증

배포 후에는 단순히 사이트가 열리는지만 보면 안 된다. 사용자가 실제로 할 행동을 처음부터 끝까지 따라가야 한다.

```text
1. 게시글 작성
2. 목록 조회
3. 상세 조회
4. 검색
5. 수정
6. 삭제
7. Swagger UI에서 실제 API 응답 확인
```

E2E 검증은 “버튼이 보이는가”보다 “데이터가 끝까지 정상적으로 흐르는가”를 확인하는 과정이다. 특히 배포 환경에서는 프론트와 백엔드가 서로 다른 서버에 있으므로 환경변수, CORS, API URL, DB 저장 여부를 함께 확인해야 한다.

---

## 06. Vercel/Railway와 Docker/AWS의 차이

Vercel과 Railway는 빠르게 배포하기 좋다. 하지만 인프라 제어권은 제한적이다. Docker/AWS 방식은 직접 설정해야 할 것이 많지만, 실행 환경과 네트워크, DB, 모니터링을 더 세밀하게 제어할 수 있다.

| 구분 | Vercel + Railway | Docker + AWS |
| --- | --- | --- |
| 난이도 | 낮음 | 높음 |
| 배포 속도 | 빠름 | 느림 |
| 제어권 | 제한적 | 높음 |
| 적합한 상황 | 사이드 프로젝트, MVP | 운영 서비스, 고트래픽 시스템 |
| DB | 간단한 파일 DB도 가능 | RDS 같은 관리형 DB 권장 |

---

## 오늘의 정리

4주차의 핵심은 로컬에서 만들던 풀스택 앱을 실제 URL이 있는 배포 환경으로 옮겨보는 것이었다.

- Direct Fetch는 단순하지만 브라우저에 백엔드 주소가 드러난다.
- Route Handler는 Next.js 서버가 백엔드를 대신 호출하는 프록시 역할을 한다.
- Vercel은 Next.js 배포에 편하고, Railway는 FastAPI 서버 실행에 적합했다.
- 배포 후에는 E2E 시나리오로 실제 데이터 흐름을 검증해야 한다.
- 다음 단계인 Docker/AWS는 편리한 플랫폼 뒤에서 일어나는 일을 직접 다뤄보는 과정이다.

> [!note]- 📚 강의 자료 보기
> ![[19. 풀스택 통합 실습 복습]]
> ![[20. Vercel & Railway 소개 및 배포]]
> ![[21. E2E 검증 & Docker:AWS 개요]]
