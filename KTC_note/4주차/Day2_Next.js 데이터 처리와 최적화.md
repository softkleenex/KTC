---

## 01. Server Component에서 데이터 가져오기

Next.js App Router의 컴포넌트는 기본적으로 Server Component다. 따라서 컴포넌트 함수 자체를 `async`로 만들고 서버에서 직접 데이터를 가져올 수 있다.

```tsx
interface Post {
  id: number;
  title: string;
}

async function getPosts() {
  const response = await fetch("https://jsonplaceholder.typicode.com/posts");
  const posts: Post[] = await response.json();
  return posts;
}

export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

이 요청은 브라우저가 아니라 서버에서 실행된다. 그래서 브라우저 개발자 도구의 Network 탭에서 해당 API 요청이 직접 보이지 않을 수 있다. 이 점은 환경변수나 내부 API 주소를 숨길 수 있다는 장점이 되지만, 디버깅할 때는 서버 로그를 함께 봐야 한다.

---

## 02. SSR의 단점과 loading.tsx

Server Component는 서버에서 데이터를 가져온 뒤 HTML을 만들어 보낸다. 데이터가 빨리 오면 좋지만, 요청이 오래 걸리면 사용자는 빈 화면을 보게 될 수 있다.

```tsx
async function getPosts() {
  await new Promise((resolve) => setTimeout(resolve, 3000));
  const response = await fetch("https://jsonplaceholder.typicode.com/posts");
  return response.json();
}
```

이 문제를 보완하기 위해 Next.js는 `loading.tsx`라는 약속된 파일을 제공한다.

```tsx
// app/loading.tsx
export default function Loading() {
  return <h2>Loading...</h2>;
}
```

`loading.tsx`를 추가하면 데이터가 준비되는 동안 로딩 UI를 먼저 보여줄 수 있다. 서버에서 렌더링하는데도 중간 로딩 UI가 가능한 이유는 Streaming 때문이다.

---

## 03. Streaming

Streaming은 HTML 또는 데이터를 작은 조각으로 나누어 준비된 부분부터 점진적으로 클라이언트에 보내는 방식이다. React 컴포넌트는 화면을 여러 조각으로 나누어 구성하므로, Streaming과 잘 맞는다.

흐름을 간단히 쓰면 다음과 같다.

```text
1. 브라우저가 페이지 요청
2. 서버가 레이아웃과 로딩 UI를 먼저 전송
3. 서버에서 데이터 fetching 진행
4. 준비된 컴포넌트를 추가로 전송
5. 브라우저가 화면을 점진적으로 갱신
```

즉, `loading.tsx`는 단순히 “로딩 문구 파일”이 아니라, Next.js가 Streaming 경계를 잡을 수 있게 해주는 파일이다.

---

## 04. 여러 데이터 요청과 Promise.all

한 페이지에서 여러 데이터를 가져올 때 순차적으로 `await`하면 대기 시간이 합쳐진다.

```tsx
const posts = await getPosts(); // 3초
const users = await getUsers(); // 5초
// 총 8초 가까이 대기
```

두 요청이 서로 의존하지 않는다면 `Promise.all`로 병렬 처리할 수 있다.

```tsx
const [posts, users] = await Promise.all([getPosts(), getUsers()]);
```

이 경우 전체 대기 시간은 두 작업의 합이 아니라 더 오래 걸리는 작업의 시간에 가까워진다. 예를 들어 3초 요청과 5초 요청을 병렬로 보내면 전체는 약 5초가 된다.

---

## 05. Suspense를 이용한 병렬 렌더링

`Promise.all`은 요청을 병렬로 처리하지만, 모든 요청이 끝나야 화면이 한 번에 렌더링된다. 먼저 끝난 컴포넌트부터 보여주고 싶다면 컴포넌트를 분리하고 `Suspense`로 감싼다.

```tsx
import { Suspense } from "react";
import PostsList from "./PostsList";
import UsersList from "./UsersList";

export default function PostsPage() {
  return (
    <>
      <h2>게시글 목록</h2>
      <Suspense fallback={<h2>Loading Posts...</h2>}>
        <PostsList />
      </Suspense>
      <Suspense fallback={<h2>Loading Users...</h2>}>
        <UsersList />
      </Suspense>
    </>
  );
}
```

이 구조에서는 `PostsList`와 `UsersList`가 각각 독립적인 로딩 경계를 가진다. 먼저 준비된 컴포넌트는 먼저 화면에 나타나고, 늦게 끝나는 컴포넌트만 fallback UI를 유지한다.

---

## 06. Server Actions

GET 요청은 Server Component에서 자연스럽게 처리할 수 있다. 문제는 POST, PUT, DELETE처럼 서버나 DB 상태를 바꾸는 작업이다.

클라이언트 컴포넌트에서 `fetch`로 직접 처리할 수도 있지만, 그러면 브라우저에 비즈니스 로직이 많아지고 hydration 부담도 커진다. Next.js는 이런 변경 작업을 서버에서 처리하기 위해 Server Actions를 제공한다.

```tsx
// app/actions.ts
"use server";

export async function createPost(formData: FormData) {
  const title = formData.get("title");
  const content = formData.get("content");

  await fetch(`${process.env.FASTAPI_URL}/posts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });
}
```

Server Action은 서버에서 실행되므로 클라이언트 번들에 포함되지 않는다. API 주소, DB 접근, 인증 로직처럼 브라우저에 드러나면 안 되는 처리를 서버 쪽으로 숨길 수 있다.

---

## 오늘의 정리

- Server Component에서는 컴포넌트 함수에서 직접 `async/await`을 사용할 수 있다.
- SSR은 데이터가 늦으면 빈 화면 대기가 생길 수 있다.
- `loading.tsx`와 Streaming은 준비된 UI부터 점진적으로 보여준다.
- 독립적인 요청은 `Promise.all`로 병렬 처리한다.
- 컴포넌트를 분리하고 `Suspense`를 쓰면 준비된 컴포넌트부터 렌더링할 수 있다.
- 데이터 변경 작업은 Server Actions로 서버에 가깝게 두는 것이 Next.js다운 방향이다.

> [!note]- 📚 강의 자료 보기
> ![[[수업 자료] Next.js 데이터 처리와 최적화]]
