


## 01_ SQL 시작하기

---

### SQL 이란?

데이터베이스는 많은데,,, 세상에 존재하는 모든 데이터베이스에 대해서 알 필요는 없다

데이터 베이스의 검색, 분석에 사용되는 기본 사용 방법은 모두 동일하다.

---

### 테이블에서 데이터 검색하기

- 관계형 데이터 베이스
	- 하나 이상의 테이블로 이루어지며 서로 연결된 데이터를 가짐
	- 관례형 데이터베이스는 테이블이 모여있는 집합이라고도 할 수 있음

 - 테이블
	-  테이블은 컬럼(Column)과 레코드(Record) = 행(row) 로 구성된 표이다
	 - 모든 테이블은 고유의 이름으로 구분한다

테이블에서 데이터 검색하는법

---


### 테이블에서 데이터를 가져오는 기본명령어들

- SELECT
	- 데이터 검색, 엑셀의 filter과 유사함, select 검색할대상	
		- 중복 데이터는 가져오기 싫다면? DISTINCT:뚜렷한, 분명함 명령어를 쓴다. 뒤에 나오는 컬럼의 중복을 제거하고 보여준다. 마치 엘셀에서의 중복된 항목 제거와 유사하다.
		- DISTINCT 제목, 저자. 이런식으로 2개 이상의 컬럼을 적어 여러 중복에 대해서 제외 가능(제목과 저자 모두 중복일때만 제외됨)
- FROM
	- ~로부터. from 테이블 명
- WHERE
	- 조건을 부여할떄 쓰인다. where 조건

```
-- SELECT 와 FROM 으로 book 테이블에서 모든 책의 tittle과 author 컬럼을 검색한다

-- SELECT 검색할 컬럼, 
SELECT title, author
--from 테이블
FROM book


-- 모든 데이터를 SELECT로 가져오는 방법
SELECT *
FROM book;



--두개의 컬럼에 대한 DISTINCT.순서를 잘 기억하자.
SELECT DISTINCT title, author
FROM book;
```

---


### 조건을 추가하여 검색하기


검색하고자 하는 데이터의 조건을 설정할수 있는 명령인 WHERE을 사용하자.


- WHERE
	- WHERE + 데이터(레코드) 로 사용된다. 


```
-- SELECT/WHERE문의 기본 문법. 제목이 돈키호테인 책 데이터를 book테이블에서 검색하자.

-- 모든 컬럼을 SELECT로 검색하자
SELECT *
-- 대상테이블
FROM book
-- 조건을 입력한다
WHERE title = ‘돈키호테‘;
```


---

### 여러 개의 조건을 추가하기

조건 부여에 사용되는 연산자들

- 값 비교 연산자
  - <, >, >= <= 등 기본적으로 파이썬과 같다. 단, 같음의 조건이 == 가 아니라 = 인 점에 유의할것

```
-- 비교연산자를 사용해서 검색 예시, score 테이블에서 국어(korean) 성적이 90 이상인 값 검색

-- 명령 검색할 컬럼
SELECT *
-- 테이블
FROM score
--조건
WHERE korean >= 90

```

- 복합 조건 연산자
	- 여러 조건이 합쳐짐

| 연산자      | 연산 예시                | 의미                 |
| -------- | -------------------- | ------------------ |
| AND, &&  | A AND B <br> A && B  | A 그리고 B를 모두 만족하는 값 |
| OR, \|\| | A OR B <br> A \|\| b | A또는 B인 값           |
| NOT, !   | NOT A <br>!A         | A가 아닌 값            |
```
-- 복합 조건 연산자를 사용해서 검색 예시, score 테이블에서 국어(korean) 성적이 90 이상이거나 수학(math) 성적이 80초과인 값 검색
-- 명령 검색할 컬럼
SELECT *
-- 테이블
FROM score
-- 조건
WHERE korean >= 90 OR math > 80;
```

기타 연산자



| 연산자     | 연산 예시               | 의미                                          |
| ------- | ------------------- | ------------------------------------------- |
| BETWEEN | A BETWEEN 10 AND 20 | A가 10과 20 사이에 포함된 값(10 이상 20 이하임, 초과 미만 아님) |
| IN      | A IN B              | B에 A가 포함된 값                                 |
| NOT IN  | A NOT IN B          | B에 A가 포함되지않은 값                              |
```
-- 기타 연산자를 사용하여 검색 예씨, score 테이블에서 수학(math) 성적이 80과 90 사이의 값 검색
--
명령 검색할 컬럼
SELECT *
-- 테이블
FROM score
-- 조건
WHERE math BETWEEN 80 AND 90
```

between 은 나이대 검색에 자주 쓰임(20대 > between 20 AND 29)

---

## 02_데이터를 제어하는 DML

### 테이블에서 유사한 값 찾기


- LIKE 
	- 특정 문자가 포함된 문자열을 찾고 싶을떄 사용
```
-- book 테이블에서 제목이 어린왕자인 책 검색 예씨
-- 명령 검색할 컬럼
select *
-- 테이블
FROM book

-- 조건 예시 WHERE title LIKE DATA 유의할것!
WHERE title LIKE ‘어린왕자‘;
```

LIKE 조건의 다양한 형태
```
SELECT *
FROM book
-- % = 와일드 카드. 제목이 왕자로 끝나는 책 검색
WHERE title LIKE ‘%왕자’;

-- 제목이 어린으로 시작하는 책 검색
WHERE title LIKE ‘어린%‘;

-- 제목에 린왕이 포함되는 책 검색
WHERE title LIKE ‘%린왕%’;
```


---

### 데이터 정렬하기

- ORDER BY
	- 데이터를 검색할 때 정렬하여 결과를 출력하는 명령여
		- 엑셀의 텍스트 오름차순/내림차순 정렬과 비슷하다
		- 정말 많이 쓴다!!!
```
-- ORDER BY 문의 기본 문법
-- score 테이블에서 수학 값이 높은 데이터부터 검색하여 출력
-- 명령
SELECT *
-- 테이블
FROM score
-- 정렬 조건 오름차순
ORDER BY math DESC;

— 생략
--정렬 조건 내림차순
ORDER BY math ASC;

```

---

### 테이블에 데이터 삽입하기

- INSERT
	- 관계형 데이터베이스의 테이블에 값을 저장하는 명령

```
-- INSERT 문의 기본 문법
—- 햄릿 책 데이터를 book 테입ㅡㄹ에 추가

-- 명령 테이블 컬럼
INTSER INTO book(id, title, author, publisher)
-- 추가할 데이터
VALUES(‘3’, ‘햄릿‘, ’윌리엄 셰익스피어‘, ’엘리스 출판’);


--만약 컬럼을 넣지 않는다면?, 순서대로 값을 삽입한다
INTSER INTO book
-- 추가할 데이터
VALUES(‘3’, ‘햄릿‘, ’윌리엄 셰익스피어‘, ’엘리스 출판’);

```


---

### 테이블의 데이터 수정하기

- UPDATE
	- 관계형 데이터베이스의 테이블에서 이미 저장된 값을 수정하는 명령


```
-- UPDATE 문의 기본 문법
-- 책 제목이 돈키호테인 데이터의 제목을 돈키호테 1로 변경
— 명령 테이블
UPDATE book
-- 변경할 값(미래)
SET title = ‘돈키호테 1’
-- 조건(현재)
WHERE title = ‘돈키호테‘;
```

---
### 테이블의 데이터 삭제하기


- DELETE
	- 관계형 데이터베이스의 테이블에서 이미 저장된 값을 삭제하는 명령


```
--DELETE 문의 기본 문법
-- 제목이 돈키호테 1인 책 데이터를 book 테이블에서 삭제
-- 명령
DELETE
--테이블
FROM book
-- 조건
WHERE title - ‘돈키호테 1‘;



-- WHERE 조건이 없을 시에 모든 데이터 삭제
 
```

---

## 03_SQL과 함수

함수의 종류는 크게 3가지

1. 데이터 값을 계산하거나 조작 : 행함수
2. 행의 크룹을 계산하거나 요약 : 그룹함수
3. 열의 데이터 타입을 변환
 우리가 배울껀 1, 2 번 함수

---

### COUNT

- COUNT
	- 검색한 결과의 데이터의 개수를 가져오는 내장 함수. NULL인 데이터는 제외(데이터가 없음, 빈공간)

```
-- COUNT 기본 문법
-- BOOK 테이블 안에 있는 id컬럼의 개수를 검색

-- 명령, 검색할 컬럼
SELECT COUNT(id) FROM book;

-- 검색할 데이터에 *을 입력하면 모든 데이터 검색
SELECT COUNT(*) FROM book;
```







---

### LIMIT
- LIMIT
	- 테이블에서 출력하고자 하는 데이터의 개수를 제한하는 명령어

```
--LIMIT 기본 문법

-- book 테이블에서 데이터를 5개만 가져오기
—-명령 —- 제한할 숫자
SELECT * FROM book LIMIT 5;

--2번째 데이터부터 5개를 가져오기
-- 2번째 데이터부터 5개를 가져오기
SELECT * FROM book LIMIT 1, 5;

--첫번째 컬럼의 시작은 0 즉, LIMIT 1, 5는 “2번째 철럼부터 5개를 가져오라는 의미 
```

---

### SUM & AVG

- SUM
	- Summation 총합
	- 지정한 컬럼들의 값을 모두 더하여 총점을 구해주는 내장함수

- AVG
	- AVERAGE 평균
	- 지정한 컬럼들의 평균값을 구해주는 내장함수

```
-- SUM 기본 문법
-- SUM을 이용해 원하는 데이터의 합을 구할 수 있다.
-- 명령 검색할 컬럼
SELECT SUM(math) FROM grade;


-- AVG 기본문법
-- AVG를 이용해서 원하는 데이터의 평균을 구할 수 있다.
-- 명령 평균을 구할 컬럼
SELECT AVG(korean), AVG(english), AVG(math) FROM grade;
```




함수를 언제는 앞, 뒤, 중간,,, 어떻게 외우지?
	컬럼을 기준으로 데이터를 불러오느냐? 
	컬럼은 SELECT의 오른쪽에 위치한다.
	WHERE 옆에서 조건이 되느냐? 이런 차이가 있다.
	조건은 WHERE의 오른쪽에 위치 한다.
	
---

### MAX & MIN

- MAX
	- 테이블에 존재하는 데이터에서 최대값을 가져오는 내장함수(숫자형이 아니라 문자형도 가능하다)

- MIN
	- 테이블에 존재하는 데이터에서 최소값을 가져오는 내장함수(숫자형이 아니라 문자형도 가능하다)

```
-- MAX 기본문법
-- 원하는 데이터의 최댓값을 구할 수 있다.
-- 명령 검색할 컬럼
SELECT MAX(korean) FROM grade;

-- MIN 기본문법
-- 원하는 데이터의 최솟값을 구할 수 있다.
-- 명령 검색할 컬럼
SELECT MIN(english) FROM grade;
```


---



## 04_다수의 테이블 제어하기

---
### 데이터 그룹 짓기

- GROUP BY
	- 테이블에서 컬럼값이 같은 데이터끼리 그룹화한 결과 확인 가능
	- 앞서 배운 SUM, AVG, COUNT, MAX, MIN 을 활용하면 더 잘 활용 가능함.

```
-- GROUP BY 절의 기본 문법
-- 명령 검색할 컬럼
SELECT user_id, COUNT(*)
-- 테이블
FROM rental
--그룹의 기준 컬럼, 쿼리 맨 끝에 위치하는것은 LIMIT, ORDER BY에 GROUP BY 라는것을 기억해보자.
GROUT BY user_id;

-- user_id가 같은 열에서 컬럼의 내용을 다 더한 값을 출력
SELECT user_id, SUM(컬럼명) FROM rental GROUP BY user_id;

-- user_id가 같은 열의 컬럼의 평균을 출력
SELECT user_id, AVG(컬럼명) FROM rental GROUP BY user_id;

-- user_id가 같은 열 중에서 해당 컬럼명이 가장 큰 값을 출력
SELECT user_id, MAX(컬럼명) FROM rental GROUP BY user_id;

-- user_id가 같은 열 중에서 해당 컬럼명이 가장 작은 값을 출력
SELECT user_id, MIN(컬럼명) FROM rental GROUP BY user_id;

```



---

### 데이터 그룹에 조건 적용하기

- HAVING
	- GROUP BY에 조건을 부여하고 싶다면사용한다

	```
	-- GROUP BY / HAVING 절의 기본 문법
	-- rental 테이블에서 user_id가 같은 1개 초과의 데이터가 몇개 있는지 검색
	-- 명령 검색할 컬럼
	SELECT user_id, COUNT(*)
	-- 테이블
	FROM rental
	-- 그룹의 기준 컬럼
	GROUP BY user_id
	-- 조건
	HAVING COUNT(user_id) > 1;
	```

---
### 두개의 테이블에서 조회하기

- INNER JOIN
	- 두 테이블의 정보를 한번에 조회할 수 있다.
```
-- INNER JOIN문의 기본 문법
-- 명령 검색할 컬럼
SELECT *
-- 테이블
FROM rental
-- 연결할 테이블
INNER JOIN user;
```

JOIN : 여러 개의 테이블을 서로 연결(inner, left, right세종류)

---
### 조건을 적용해 두개의 테이블 조회하기

INNER JOIN / ON

```
-- INNER JOIN / ON의 기본 문법
-- 명령 검색할 컬럼
SELECT * 
-- 테이블
FROM rental
-- 연결할 테이블
INNER JOIN user
-- 연결한 조건 컬럼
ON user.id = rental.user_id;
```

---

### LEFT JOIN

LEFT JOIN
```
-- LEFT JOIN문의 기본 문법
-- user 테이블을 모두 출력하되 모든 user 테이블의 user_id와 rental 테이블의 id가 겹치도록 합친다.

-- 명령 검색할 컬럼
SELECT * 
-- 테이블
FROM user
-- 연결할 테이블
LEFT JOIN rental
--조건
ON user.id = rental.uesr_id;
```

INNER JOIN VS LEFR JOIN
두 데이터 중 겹치는 부분만 출력 VS 왼쪽 데이터와 겹치는 부분을 출력

---

### RIGHT JOIN

RIGHT JOIN


```
-- RIGHT JOIN 문의 기본 문법
-- rental 테이블을 모두 출력하되 모든 rental 테이블의 user_id와 user테이블의 id가 겹치도록 합친다.
-- 명령 검색할 컬럼
SELECT *
-- 테이블
FROM user
-- 연결할 테이블
RIGHT JOIN
-- 조건
ON user.id = rental.user_id;
```


LEFT JOIN VS RIGHT JOIN
왼쪽 데이터와 겹치는부분을 출력 vs 오른쪽 데이터와 겹치는 부분을 출력

---


