

https://www.notion.so/elice-track/06-DB-SQL-36c2bb984257806d997ec5d6838affdb?source=copy_link

<aside> 📊

**DB & SQL을 배워야 하는 이유**

파이썬으로 변수에 값을 저장하고, 함수도 만들고, 리스트로 데이터도 다뤄봤습니다. 그런데 한 가지 문제가 있습니다. **프로그램을 끄면 다 사라집니다.**

회원가입을 처리하는 코드를 짰어도, 서버를 재시작하면 가입 정보가 없어집니다. 진짜 서비스가 되려면 데이터가 영구적으로 살아있어야 합니다. 이때 필요한 게 **데이터베이스(DB)** 입니다.

그럼 SQL은 뭘까요? DB는 창고, **SQL은 창고 직원에게 말을 거는 방법**입니다. "이 데이터 꺼내줘", "저 데이터 수정해줘"를 DB가 알아듣는 언어로 요청하는 것이 SQL입니다.

</aside>

## 🔙 1주 5일차 복습 — DB & SQL 기초

<aside> 📌

**핵심 개념**

- **관계형 DB**: 데이터를 표(테이블) 형태로 저장. 테이블은 **Foreign Key**로 서로 연결됨
- **Primary Key (PK)**: 각 행을 유일하게 구분하는 값 (예: `id`)
- **Foreign Key (FK)**: 다른 테이블의 PK를 참조해 관계 표현
- **ERD**: 테이블 간 관계를 그림으로 나타낸 설계도 </aside>

![[Pasted image 20260526191722.png]]

관계형, 비관계형 DB

### users 테이블

|id|name|
|---|---|
|1|김민준|
|2|이서아|

### messages 테이블

|id|user_id|content|
|---|---|---|
|1|1|안녕하세요|
|2|1|날씨 알려줘|
|3|2|오늘 메뉴 추천해줘|

`messages.user_id = 1` 이 `users.id = 1` (김민준)을 가리키는 구조입니다.

- PK: `users.id`, `messages.id`
- FK: `messages.user_id` ➡️ `users.id`를 가리킴


ERD예시로는 Supabase가 있다.



## 🔙 2주 1일차 복습 — SQL 조회와 조작

<aside> 📌

**핵심 구문**

- **SELECT**: `SELECT * FROM messages WHERE user_id = 1 ORDER BY id DESC`
- **INSERT**: `INSERT INTO messages (user_id, content) VALUES (1, '안녕')`
- **UPDATE**: `UPDATE messages SET content = '수정된 내용' WHERE id = 1`
- **DELETE**: `DELETE FROM messages WHERE id = 1` </aside>

---

## 📚 SQL 핵심 문법 복습

### 1️⃣ SELECT — 데이터 조회하기

```sql
-- 전체 컬럼 조회
SELECT * FROM messages;

-- 특정 컬럼만 조회 (보낸 사람과 내용만)
SELECT user_id, content FROM messages;

-- 조건 추가 (WHERE): 특정 사용자의 메시지만
SELECT * FROM messages WHERE user_id = 1;

-- AND (둘 다 만족): 사용자 1이 보낸 메시지 중 '날씨' 포함된 것
SELECT * FROM messages WHERE user_id = 1 AND content LIKE '%날씨%';

-- OR (하나라도 만족): 사용자 1 또는 2의 메시지
SELECT * FROM messages WHERE user_id = 1 OR user_id = 2;

-- NOT (조건 반전): 사용자 1이 아닌 메시지
SELECT * FROM messages WHERE NOT user_id = 1;

-- BETWEEN (범위): id가 10~20 사이인 메시지 (특정 구간 페이지네이션)
SELECT * FROM messages WHERE id BETWEEN 10 AND 20;

-- IN (목록 중 하나): 특정 사용자들의 메시지 한 번에 조회
SELECT * FROM messages WHERE user_id IN (1, 2, 3);

-- NOT IN (목록 제외): 특정 사용자들의 메시지 제외
SELECT * FROM messages WHERE user_id NOT IN (1, 2, 3);

-- DISTINCT (중복 제거): 메시지를 보낸 적 있는 사용자가 누구누구인지
SELECT DISTINCT user_id FROM messages;
```

### 2️⃣ LIKE — 패턴으로 검색하기

<aside> 📌

`%` = **아무 글자나 여러 개** (0개 이상). 정규표현식의 `.*`와 비슷하게 생각하세요.

</aside>

|패턴|의미|예시|
|---|---|---|
|`LIKE '%안녕'`|'안녕'으로 끝나는 메시지|잘 부탁해, 안녕 ✅|
|`LIKE '안녕%'`|'안녕'으로 시작하는 메시지|안녕하세요? ✅|
|`LIKE '%추천%'`|'추천'을 포함하는 메시지|오늘 메뉴 추천해줘 ✅|

```sql
-- '안녕'으로 끝나는 메시지 검색
SELECT * FROM messages WHERE content LIKE '%안녕';

-- '안녕'으로 시작하는 메시지
SELECT * FROM messages WHERE content LIKE '안녕%';

-- '추천'이 포함된 모든 메시지
SELECT * FROM messages WHERE content LIKE '%추천%';
```

### 3️⃣ ORDER BY — 정렬하기

```sql
-- 최신 메시지 순 (id 내림차순)
SELECT * FROM messages ORDER BY id DESC;

-- 오래된 메시지 순 (id 오름차순, ASC는 기본값)
SELECT * FROM messages ORDER BY id ASC;

-- 사용자 1의 메시지를 최신 순으로
SELECT * FROM messages WHERE user_id = 1 ORDER BY id DESC;
```

```sql
-- 예시 (ORDER BY id DESC)
id | user_id | content
---|---------|-------------------
3  | 2       | 오늘 메뉴 추천해줘
2  | 1       | 날씨 알려줘
1  | 1       | 안녕하세요
```

### 4️⃣ DML — 데이터 추가 · 수정 · 삭제

|**기능**|**기본 문법**|
|---|---|
|**삽입**|`INSERT INTO [테이블] (컬럼1, 컬럼2...) VALUES (값1, 값2...);`|
|**수정**|`UPDATE [테이블] SET 컬럼1 = 값1 WHERE [조건];`|
|**삭제**|`DELETE FROM [테이블] WHERE [조건];`|

<aside> 📌

**⚠️ WHERE 없이 UPDATE/DELETE 하면 전체 행이 바뀝니다.** 반드시 WHERE 먼저 확인!

</aside>

```sql
-- INSERT: 사용자가 메시지를 보냈을 때
INSERT INTO messages (user_id, content) VALUES (1, '오늘 날씨 어때?');

-- UPDATE: 메시지 내용 수정
UPDATE messages SET content = '내일 날씨 어때?' WHERE id = 3;
-- ❌ 위험: UPDATE messages SET content = '내일 날씨 어때?';
--          → 모든 메시지 내용이 '내일 날씨 어때?'로 바뀜

-- DELETE: 특정 메시지 삭제
DELETE FROM messages WHERE id = 3;
-- ❌ 위험: DELETE FROM messages;
--          → 전체 메시지 삭제
```

### 5️⃣ 집계 함수 — 데이터 통계 내기

<aside> 💡

**COUNT(*) vs COUNT(컬럼)**: `COUNT(*)`는 NULL 포함 전체 행 수, `COUNT(컬럼)`은 NULL이 있는 행을 제외하고 셉니다.

</aside>

|함수|의미|예시|
|---|---|---|
|`COUNT(*)`|전체 행 수 (NULL 포함)|`SELECT COUNT(*) FROM books;`|
|`COUNT(컬럼)`|NULL 제외 행 수|`SELECT COUNT(author) FROM books;`|
|`SUM(컬럼)`|합계|`SELECT SUM(price) FROM books;`|
|`AVG(컬럼)`|평균|`SELECT AVG(price) FROM books;`|
|`MAX(컬럼)`|최댓값|`SELECT MAX(price) FROM books;`|
|`MIN(컬럼)`|최솟값|`SELECT MIN(price) FROM books;`|

```sql
-- 전체 메시지 수
SELECT COUNT(*) FROM messages;

-- 이메일이 등록된 사용자 수 (NULL 제외)
SELECT COUNT(email) FROM users;

-- 사용자 1이 보낸 메시지 수
SELECT COUNT(*) FROM messages WHERE user_id = 1;

-- 가장 최근(최대) 메시지 id 확인
SELECT MAX(id) FROM messages;

-- 가장 오래된(최소) 메시지 id 확인
SELECT MIN(id) FROM messages;

-- 가장 최근 메시지 1개만 (LIMIT)
SELECT * FROM messages ORDER BY id DESC LIMIT 1;

-- 2번째 행부터 5개 (LIMIT offset, 개수) / (LIMIT 개수 OFFSET 오프셋)
SELECT * FROM messages LIMIT 1, 5;
SELECT * FROM messages LIMIT 5 OFFSET 1;
```

### 6️⃣ GROUP BY & HAVING — 그룹으로 묶어 집계하기

<aside> 📌

`WHERE`는 **집계 전**에 행을 필터링하고, `HAVING`은 **집계 후**에 그룹을 필터링합니다.

순서: `WHERE` → `GROUP BY` → `HAVING`

</aside>

```sql
-- 사용자별 메시지 수

-- 3️⃣ 집계할 기준 컬럼(user_id)과 개수를 센 결과(message_count)를 화면에 보여줘라.
SELECT user_id, COUNT(*) AS message_count

-- 1️⃣ 우선 messages 테이블에서 데이터를 가져와서
FROM messages

-- 2️⃣ 똑같은 user_id를 가진 행들끼리 하나의 그룹(묶음)으로 쪼개라.
GROUP BY user_id;

-- 출력 예시
-- user_id | message_count
-- --------|---------------
-- 1       | 2
-- 2       | 1

-- 메시지를 2개 이상 보낸 사용자만 (HAVING)

-- 4️⃣ 그룹화된 결과 중, 최종 필터링을 통과한 그룹의 user_id와 개수만 화면에 보여줘라.
SELECT user_id, COUNT(*) AS message_count

-- 1️⃣ 우선 messages 테이블에서 데이터를 가져와서
FROM messages

-- 2️⃣ 똑같은 user_id를 가진 행들끼리 그룹으로 묶은 뒤
GROUP BY user_id

-- 3️⃣ 🔥 [그룹 전용 조건] 묶고 보니 데이터 개수(메시지 수)가 2개 이상인 그룹만 남겨라.
HAVING COUNT(*) >= 2;
```

### 7️⃣ JOIN — 여러 테이블 연결하기

데이터베이스는 효율적인 관리를 위해 **서로 연관된 정보들을 한곳에 모으지 않고, 성격에 따라 여러 테이블로 쪼개어 각각 따로 관리**합니다. 이처럼 분리되어 저장된 데이터들을 **다시 하나로 묶어서 한눈에 확인해야 할 때** `JOIN`이 필요합니다.

- **사용 예시**
    - **챗봇 서비스를 운영할 때**
        - 상담 대화방을 개설한 **[유저의 닉네임]**과 그 유저가 챗봇과 나눈 **[최근 대화 내용]**을 한 화면에 같이 보여줘야 하는 상황
    - **쇼핑몰 운영할 때**
        - 특정 제품 주문을 한 [**고객의 이름]**과 그 고객이 산 [**상품의 이름]**을 같이 보여줘야 하는 상황

**users 테이블**

|id|username|
|---|---|
|1|김민준|
|2|이서아|
|3|박서준|

**messages 테이블**

|id|user_id|content|
|---|---|---|
|1|1|안녕하세요|
|2|1|날씨 알려줘|
|3|2|오늘 메뉴 추천해줘|
|4|4|반갑습니다|

> 박서준(id=3)은 메시지를 보낸 적 없고, user_id=4인 메시지는 탈퇴한 회원이 보낸 기록입니다.🤲🏻 JOIN 종류와 예시

#### **🤲🏻 JOIN 종류**

![[Pasted image 20260526191854.png]]

|JOIN 종류|설명|결과|사용 예시|
|---|---|---|---|
|INNER JOIN|양쪽 모두 매칭되는 행만|교집합|양쪽 테이블에 **모두 데이터가 존재하는 온전한 건**만 엮어서 보여주고 싶을 때|
|LEFT JOIN|왼쪽 테이블 전체 기준|왼쪽 전체 + 오른쪽 매칭값 (없으면 NULL)|데이터가 없더라도 **왼쪽 메인 테이블의 정보는 무조건 누락 없이 다 보여줘야 할 때**|
|RIGHT JOIN|오른쪽 테이블 전체 기준|오른쪽 전체 + 왼쪽 매칭값 (없으면 NULL)|데이터가 없더라도 **오른쪽 서브 테이블의 정보를 무조건 다 유지해야 할 때**|

**INNER JOIN** — 양쪽에 모두 있는 행만 연결

```sql
SELECT users.username, messages.content
FROM messages
INNER JOIN users ON users.id = messages.user_id;
```

|username|content|
|---|---|
|김민준|안녕하세요|
|김민준|날씨 알려줘|
|이서아|오늘 메뉴 추천해줘|

> 박서준(메시지 없음), user_id=4(탈퇴 회원) 모두 제외됩니다.

**LEFT JOIN** — 왼쪽(users) 전체 + 오른쪽(messages) 매칭 없으면 NULL

```sql
SELECT users.username, messages.content
FROM users
LEFT JOIN messages ON users.id = messages.user_id;
```

|username|content|
|---|---|
|김민준|안녕하세요|
|김민준|날씨 알려줘|
|이서아|오늘 메뉴 추천해줘|
|박서준|NULL|

> 메시지를 보내지 않은 박서준도 포함됩니다. content는 NULL.

**RIGHT JOIN** — 오른쪽(messages) 전체 + 왼쪽(users) 매칭 없으면 NULL

> 탈퇴한 회원(user_id=4)의 메시지도 포함됩니다. username은 NULL.

---

## 🔗 오늘 배울 내용 미리보기

<aside> 🔗

지금까지 FastAPI(API)와 SQL(DB)을 **따로** 배웠습니다.

오늘은 이 둘을 **하나의 흐름으로 연결**합니다.

**클라이언트 요청 → FastAPI가 받아서 → DB에 저장하거나 꺼내서 → 클라이언트에 응답**

</aside>



