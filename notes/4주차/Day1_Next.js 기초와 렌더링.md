---

## 01. Next.js 기초

Next.js는 React 기반 프레임워크다. React가 UI를 만들기 위한 라이브러리라면, Next.js는 라우팅, 렌더링, 데이터 처리, 최적화 같은 웹 애플리케이션의 큰 흐름까지 정해주는 도구에 가깝다.

React만 사용할 때는 라우터를 따로 설치하고, 데이터 fetching 방식과 폴더 구조를 직접 정해야 한다. Next.js에서는 `app/` 디렉토리 아래의 파일 구조가 곧 URL 구조가 되고, 약속된 파일 이름을 사용하면 프레임워크가 알아서 해당 역할을 수행한다.

---

## 02. 프레임워크와 라이브러리

프레임워크와 라이브러리는 모두 이미 만들어진 코드의 모음이다. 차이는 코드 흐름의 주도권이다.

| 구분 | 라이브러리 | 프레임워크 |
| --- | --- | --- |
| 흐름 제어 | 개발자가 주도 | 프레임워크가 주도 |
| 예시 | React | Next.js |
| 개발 방식 | 필요한 기능을 가져다 씀 | 정해진 규칙에 맞춰 작성 |
| 장점 | 자유도가 높음 | 구조가 일관되고 생산성이 높음 |

Next.js를 쓰면 “이 경로에는 이 파일을 둔다”, “공통 레이아웃은 이 파일에 둔다” 같은 규칙이 이미 정해져 있다. 처음에는 제약처럼 보이지만, 프로젝트가 커질수록 이런 규칙이 팀 전체의 약속이 되어 유지보수를 편하게 만든다.

---

## 03. App Router와 파일 기반 라우팅

Next.js App Router에서는 `app/` 폴더 아래의 디렉토리 구조가 URL path에 대응된다.

| 파일 경로 | URL |
| --- | --- |
| `app/page.tsx` | `/` |
| `app/about/page.tsx` | `/about` |
| `app/about/contact/page.tsx` | `/about/contact` |
| `app/products/list/page.tsx` | `/products/list` |

중요한 점은 디렉토리만 있다고 페이지가 생기지는 않는다는 것이다. 해당 경로가 실제 페이지가 되려면 `page.tsx` 파일이 필요하다.

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return <h1>About Page</h1>;
}
```

즉, Next.js 라우팅은 “폴더명으로 경로를 만들고, `page.tsx`로 화면을 만든다”고 이해하면 된다.

---

## 04. layout.tsx와 공통 UI

`layout.tsx`는 하위 페이지들이 공유하는 UI를 정의하는 약속된 파일이다. 최상위 `app/layout.tsx`는 Root Layout이며, 반드시 `html`과 `body` 태그를 포함해야 한다.

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <h1>Elice with Next.js</h1>
        {children}
      </body>
    </html>
  );
}
```

여기서 `children`에는 현재 URL에 대응되는 `page.tsx`의 결과가 들어온다. 공통 네비게이션, 전체 폰트, 공통 스타일, 헤더/푸터 같은 요소를 `layout.tsx`에 두면 모든 하위 페이지에서 반복 없이 사용할 수 있다.

하위 폴더에도 `layout.tsx`를 둘 수 있다. 예를 들어 `app/about/layout.tsx`를 만들면 `/about` 아래 경로에만 적용되는 중첩 레이아웃을 구성할 수 있다.

---

## 05. Link 컴포넌트

Next.js에서 페이지 이동은 일반 `<a>` 태그보다 `next/link`의 `Link` 컴포넌트를 사용하는 것이 좋다.

```tsx
import Link from "next/link";

export default function Navigation() {
  return (
    <nav>
      <Link href="/">홈</Link>
      <Link href="/about">소개</Link>
      <Link href="/products/list">제품 목록</Link>
    </nav>
  );
}
```

`<a href="/about">`는 브라우저가 새 HTML 문서를 다시 요청하는 방식이라 전체 페이지가 새로고침된다. 반면 `Link`는 클릭을 가로채 클라이언트 사이드 라우팅으로 필요한 부분만 교체한다.

| 구분 | `<a>` 태그 | `Link` 컴포넌트 |
| --- | --- | --- |
| 이동 방식 | 전체 페이지 새로고침 | 클라이언트 사이드 이동 |
| 상태 유지 | 어려움 | 상대적으로 유리 |
| 성능 | 매번 새 요청 | prefetch 활용 가능 |
| UX | 깜빡임 발생 가능 | 부드러운 전환 |

---

## 06. not-found.tsx

정의하지 않은 경로로 접근하면 Next.js 기본 404 페이지가 나타난다. 직접 404 화면을 만들고 싶다면 `not-found.tsx`를 사용한다.

```tsx
// app/not-found.tsx
import Link from "next/link";

export default function NotFound() {
  return (
    <>
      <h2>404 Not Found</h2>
      <Link href="/">홈으로 돌아가기</Link>
    </>
  );
}
```

---

## 오늘의 정리

Next.js의 핵심은 React 위에 “애플리케이션 구조의 규칙”을 얹는 것이다.

- `app/` 아래 폴더 구조가 URL이 된다.
- `page.tsx`는 해당 경로의 화면이다.
- `layout.tsx`는 하위 페이지가 공유하는 UI다.
- `Link`는 새로고침 없는 페이지 이동을 돕는다.
- 프레임워크의 규칙을 따르면 라우팅과 렌더링 구조를 직접 조립하는 부담이 줄어든다.

> [!note]- 📚 강의 자료 보기
> ![[[수업 자료] Next.js 기초와 렌더링]]
