

---

데이터베이스 소개

데이터란? 현실 세계에서 수집된 단순한 사실과 값들을 모아 놓은 것

정보는 데이터를 특정 목적에 의해 해석하거나 가공한 형태

데이터 베이스란

한 조직 안에서 여러 사용자와 응용프로그램이 공동으로 사용하는데이터들을 통합하여 저장하고 운영하는 데이터

데이터베이스의 종류

1. RDB(Relational DB)
	데이터를 행과 열을 가지는 테이블로 표현
	테이블 간의 관계를 이용해 데이터를 효과적으로 관리하여 데이터의 무결성을 보장
	정의된 테이블(스키마)에 맞게 데이터가 삽입되므로 데이터의 안정성을 보장
	데이터의 구조가 일관적인 경우에 주로 사용

	RDBMS의 종류
		MySQL
		PostgreSQL
		MariaDB

2. NoSQL(Not only SQL)
	데이터를 저장할 수 있는 유형의 제한이없음
	새로운 유형의 데이터를 추가하기 용이
	데이터의 구조가 일관적이지 않고 자주 변경되는 경우에 적합
	대용량의 데이터를 더 빠르게 처리할 수 있음(이미지, 음성 등)

	NoSQL의 종류
		mongoDB
		redis
		cassandra

가장 큰 차이는
관계!!!!

---

관계형 데이터 베이스의 구성요소

테이블은 행, 열로 구성
속성은 데이터의 특성을 나타내는 가장 작은 논리적 단위
튜플은 속성이 모여 구성된 각각ㄱ의 행
속성이 가질 수 있는 값의 집합을 도메인이라 함

관계
	관계가 ㅇ벗으면 주문번호등을 ID,이름, 주소와 함께 관리해야한다.
	하지만 관계가 있으니 하나의 속성으로 테이블을 연결해서 데이터들을 효과적으로 관리 가능하다.


관계형 데이터 베이스 만들기

테이블 정의하기

```
CREATE TABLE customer(
	id VARCHAR(10),
	name VARCHARE(10),
	address VARCHAR(30)
);
```

CREATE TABLE 테이블명(속성1 데이터타입1, 속성2 데이터타입 2,...);

정의한 테이블 확인하기

데이터베이스의 테이블 목록을 확인

```
SHOW TABLES; 

```

테이블의 구조를 확인
```
DESC customer;
```

SQL 문법의 기본 작성 규칙

- SQL 문법은 대문자로 작성  권장
- 테이블명, 속성명은 소문자로 작성 권장
- 이름은 항상 의미가 잘 드러나도록 작성
- 이름에 여러 단어를 혼합하는 경우 "_"를 이용해서 구분
- "--"을 이용해 주석을 나타낼 수 있음
- 명령어 ㄷ끝에는 세미콜론(;) 작성

데이터 삽입하기

```
INSERT INTO customer (id, name, address)
VALUES('kmax6', '김민준', '서울시 관악구 신림동');

-- 속성의 순서는 중요하지않는다

INSERT INTO customer (name, address, id)
VALUSE('이서연', '서울시 동작구 대방동', 'flykit');

-- 모든 속성을 순서대로 입력하는 경우에 속성 목록은 생략가능
INSERT INTO custome
VALUES('freeman123', '박서준', '서울시 관악구 신림동');

```

INSERT INTO 테이블면 (속성1, 속성2,...) VALUES(속성값1, 속성값2, ...);

속성값을 넣지않으면 default 값인 NULL이 삽입됨



데이터 출력하기

```
SELECT id, name, addredd FROM customer;

-- 출력하고 싶은 속성 조정 가능
SELECT address, name FROM customer;

--SELECT * FROM customer;
```

SELECT 속성1, 속성2,... FROM 테이블명


데이터베이스 정의어

SQL(Structured Query Language) 

관계형 데이터베이스를 활용하기 위해 사용하는 표준어

SQL의 종류

1. 데이터 정의어(DDL, Data Definition Language): 테이블과 같은 데이터 구조 정의(이번에 다룰 질의어)
    
2. 데이터 조작어(DML , Data Manipulation Language): 데이터 조회 및 검색
    
3.  데이터 제어어(DCL , Data Control Language): 데이터베이스에 접근하는 권한 관리


```
CREATE TABLE customer(
    id      VARCHAR(10) NOT NULL, --꼭 들어가야하는 데이터로 정의
    name    VARCHAR(10) NOT NULL,
    address VARCHAR(30) NULL
);

```

CREATE TABLE 테이블명(속성1 데이터타입1 제약조선, 속성 2 데이터타입 2 제약조건2, ...);


### 데이터베이스 주요 자료형 (Data Types)

| 자료형            | 의미                                          |
| :------------- | :------------------------------------------ |
| **VARCHAR(n)** | nBytes 크기의 **가변 길이** 문자열 데이터                |
| **INT**        | 정수형 숫자 데이터 (4Bytes)                         |
| **FLOAT**      | 4Bytes 크기의 부동 소수점 데이터                       |
| **DATETIME**   | 날짜와 시간 형태의 기간 데이터 <br>(YYYY-MM-DD HH:MM:SS) |


테이블 수정하기

```
-- 컬럼 추가
ALTER TABLE custimer ADD COLUMN birthday DATE NULL;
-- 컬럼 수정
ALTER TABLE customer MODIFY COLUMN id varchar(15) NULL:
-- 컬럼 이름 변경
ALTER TABLE custimer CHANGE COLUMN name korean)name varchar(10) NOT NULL;
-- 컬럼 삭제
ALTER TABLE custimer DROP COLMN adderss;
-- 테이블 이름 변경
ALTER TABLE customer RENAME member;

```


컬럼 추가: `ALTER TABLE 테이블명 ADD COLUMN 컬럼명 데이터타입 제약조건` 
컬럼 수정: `ALTER TABLE 테이블명 MODIFY COLUMN 컬럼명 데이터타입 제약조건` 
컬럼 이름 변경: `ALTER TABLE 테이블명 CHANGE COLUMN 기존컬럼명 새로운컬럼명 데이터타입 제약조건` 
컬럼 삭제: `ALTER TABLE 테이블명 DROP COLUMN 컬럼명` 
테이블 이름 변경: `ALTER TABLE 기존테이블명 RENAME 새로운테이블명`

테이블 삭제하기

``
```
DROP TABLE member;
```

DROP TABLE 테이블 명


---

데이터베이스 구정하기

제약조건

1. NOT NULL
	   NULL 값 비허용
	   데이터를 입력하지않는다면 에러가 발생한다
	   아무것도 명시하지않는 경우에 기본값은 널 값 허용
2.  UNIQUE
		중복되는 값을 비허용함
		똑같은 값이 있으면 에러가 발생함
		NULL 값은 비교가 불가능하여 중복되어도 에러가 발생하지않음
3. DEFAULT
		기본값을 설정
		아무런 값을 지정하지않으면 DEFAULT 값으로 설정됨
		
4. CHECK
		값의 범위를 제한하여 특정 값만 허용
		제한한 값이 아닌 경우 에러 발생함
	
 CONSTRAINT
	제약 조건 이름 정의: CONSTRAINT 제약조건 이름 제약조건(UNIQUE, CHECK,...) (적용할 속성);
	생성된 제약 조건 확인 SELECT * FROM information_schema.table_constraints;
	NOT NULL, DEFAULT는 사용 불가능!!!!


제약 조건 추가 : ALTER TABLE 테이블 명 ADD CONSTRAINT 제약 조건 이름 제약조건 (속성);
DEFAULT 제약 조건 수정: ALTER TABLE 테이블 명 ALTER 속성 SET DEFAULT 기본값;


제약 조건 삭제 : ALTER TABLE 테이블명 DROP CONSTRAINT 제약조건 이름;
DEFAULT 제약 조건 삭제 :ALTER TABLE 테이블명 ALTER 속성 DROP DEFAULT



데이터 베이스에서의 키

조건에 만족하는 튜플을 찾거나, 정럴할떄 기준이 되는 속성을 의미한다

기본키 (PK, Primary Key)
	서로 다른 튜플을 유일하게 실별할 수 있는 기준이 되는속성
	중복되는 값을 가질수없음
	널 값을 가질 수 없음
	테이블 당 1개만 설명


외래 키(FK, Foreign Key)
	다른 테이블의 기본키를 참조하는 속성으로 테이블의 관계를 정의
	참조하는 테이블의 키본키에 없는 값은 지정할 수 없음

후보 키
	기본 키가 될 수 있는 키로 유일성과 최소성을 만족(후보 키는 기본키의 상위)
대체 키
	후보 키중에 기본키가 아닌 키(대체 키는 후보키의 하위)
슈퍼 키
	튜플을 식별할수 있는 유일성은 만족하지만 최소성은 만족하지않는 키

SQL에서의 PK,FK 설정방법

PK, FK도 제약조건의 일부이다.

기본키

```
id VARCHAR(10) PRIMARY KEY

FOREIGN KET (customer_id) REFERENCES customer(id)
```

기본 키 설정 PRIMARY KEY

외래키 FOREIGN KEY(참조할 속성) REFERENCES 참조되는 테이블(참조되는 속성)


무결성 제약 조건
	개체 무결성
		기본키는 널 값과 중복된 값을 가질 수 없음
	참조 무결성
		외래키는 널이거나 참조되는 릴레이션의 기본키 값과 동일


		도메인 무결성
			특성 속성값은 그 속성이 정의된 도메인에 속한 값이여야한다
		NULL 무결성
				특성 속성값은 널 값을 가질 수 없음
		 고유 무결성
				각 튜플이 가지는 속성값들은 서로 달라야 함
		키 무결성
				테이블에 최소 한개 이상의 키 존재

데이터 모델링

데이터 모델링
	현실세계의 데이터를 단순화, 추상화 하여 표현한 모델
	- 개체(Entity)
		데이터로 표현하고자 하는 현실 세계의 개념이나 정보의 단위(요구사항의 명사)
	- 속성(Attribute)
		개체에 대한 정보
	- 관계(Relationship)
		개체 간의 연관성(요구사항에서의 동사)



데이터 모델링 과정
	현실세계를 추상적 개념으로 표현화 하는 과정
	
	개념적 설계
		DBMS가 처리할 수 있는 데이터 구조(스키마) 를 설계
	논리적 설계
		DBMS에 테이블을 저장할 구조를 설계
	물리적 설계


ER다이어그램(Peter Chen 방식)

ERD, Entity Relationship Diagram(개체 - 관계 다이어그램)
	현실세계의 데이터를 개체와 관계 형태의 다이어그램으로 나타내는것

![[Pasted image 20260524215619.png]]

![[Pasted image 20260524220213.png]]

하나의 데이터가 다른 테이블의 몇개의 데이터와 관계를 가지는지 나타낸다

N : M 관계는 테이블로 표기하며 각 개체의 기본키를 외래 키로 가진다



ER다이어그램(IE)
	Information Engineering
![[Pasted image 20260524221309.png]]

키를 나타내며 데이터 타입과 제약 조건 표기, 관계를 세부적으로 나타냄


![[Pasted image 20260524221414.png]]
---

## 데이터 베이스 개요

---
## 데이터 베이스 구성하기

---


## 카카오 크루 특강
