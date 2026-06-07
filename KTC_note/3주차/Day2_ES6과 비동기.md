
---
## 01 ES6 문법
---
### ES6 문법

2015에 업데이트된 ES6(ECMAScript 2015)에서는 let, const를 비롯, 중요한 큰 변화들이 많이 도입되었다.

ES6 이후 도입된 문법

![[스크린샷 2026-06-04 21.13.10.png]]

---

### let과 const

이전에는 var로 변수 선언을 하였지만, ES6부터는 let, const 를 쓴다

**let**: 값이 변경 가능한 변수를 선언하는 키워드. 선언와 초기화를 동시에 할 필요없음.
**const**: 값의 변경이 불가능한 변수(상수)를 선언하는 키워드. 선언과 초기화를 동시에 해야함.

이제부터는 무조건 변경 여부를 체크해 let, const 만쓰자!
var의 문제점: 똑같은 이름으로 변수를 선언하는 중복 선언이 발생하는 오류 발생
+ 스코프, Hoisting 이라는 두 차이점도 존재한다.

---
### 변수와 스코프

- **스코프**: 변수를 참조할 수 있는 유효 범위
	- 전역 스코프: 가장 바깥의 코드 영역
	  파일내의 어디서든 유효하다.
	- 지역 스코프: 함수 및 코드 블럭 내부
	  자신이 속한 특정 구역 내에서만 유효하다.

- 지역 스코프 종류
	- 함수 레벨 스코프: 함수 내부만 지역 스코프로 인정
	- 블록 레벨 스코프: 함수 내부 및 코드 블록 내부 둘 다 지역 스코프로 인정

var 키워드는 함수 레벨 스코프를 지원하므로, if 문 내부에서 변수 b를선언하면, if는 함수가 아니므로 변수 b는 전역변수가 된다.

let, const는 블록 레벨 스코프를 지원하므로, if 문 내부에서 변수 b를 선언하면, if는 블록이므로 변수 b는 지역변수가 된다.


>**스코프 체인**: 모든 스코프가 계층적 구조로 연결된것
모든 지역 스코프의 최상위 스코프는 전역 스코프이다
변수 및 함수를 참조할 떄 해당 스코프에서 시작해 상위 스코프 방향으로 순차적으로 이동하면서 변수 및 함수를 검색한다.

렉시컬 스코프: 함수를 정의한 위치에서 **상위 스코프**를 결정하는 방식(자바 스크립트에서 사용)

동적 스코프: 함수를 호출한 위치에서 상위 스코프를 결정하는방식(극히 일부의 언어에서 사용)


---
### 화살표 함수

일반 함수보다 간략하게 함수를 선언할 수 있다
```
() => {...}
(a, b) => a + b; //중괄호 없이 작성하면 return 키워드를 생략하고 값을 반활할 수 있다.

```


---
### 옵셔널 체이닝

기본 동작: 객체에서 존재하지않는 프로퍼티에 접근하거나, null또는 undefined인 값의 프로퍼티에 접근하면 에러 발생

'?.' 연산자 사용시(옵셔널 체이닝): 존재 하지않는 프로퍼티/인덱스에 대해 에러 없이 undefined 반환함.

예시: javascript가 오류가 난다면 화면이 하얗게 변하고 멈추는 백화현상 발생. ?.(옵셔널 체이닝) 사용시에는 사용자에게 끊김없는 화면 제공

---

### 구조 분해 할당

ES6이전 객체의 프로퍼티 값을 새로운 변수에 할당하려면, 각 변수 선언때마다 프로퍼티를 하나씩 참조해야했다.

구조 분해 할당 사용시
- `const {name, age} = person;` 과 같이 간단하게 객체의 프로퍼티 값을 변수에 할당할 수 있다. 
- `const{name: nameOfJohn, age} = person;` 처럼 각 변수의 이름을 다른 이름으로 변경할 수도 있다.
- `const{name, age, grade = 1, contact: {email}} = person;` 처럼 기본값 설정, 객체 안의 객체 구조 분해 할당 또한 가능하다.
- Rest Syntax: `const {name, age, ...rest} `처럼 '...'을 이용해 할당되지 않은 나머지 프로퍼티는 객체형태로 할당할 수 있으며, 이 객체는 보통 'rest'라는 이름으로 설정한다. 
- `function introducePerson({name, age})` 함수의 인수로 전달되는 객체를 바로 구조 분해 할당할 수도 있다.
- `const numbers = [1, 2, 3, 4, 5]; const [first, second] = numbers;` 배열 또한 구조 분해 할당 가능. 이때 변수의 이름은 원하는대로 설정할 수 있다. 배열에서도 '...'를 사용가능



예시: 속성 하나하나 입력할때 발생 가능한 개발자의 휴면 에러의 구조적 차단 가능.


---

### Spread 문법

**Spread**: 이터너블* 에 해당하는 여러 값의 집합을 펼쳐러 개별 값의 목록으로 만드는 문법. 
- 여러 배열을 결합할때 간편하게 사용 가능
- 함수의 인수로 여러 값을 전달할떄 사용
- 객체 또한 spread문법 사용가능, 단, 객체 리터럴 내부에서만 사용가능

```
...[1, 2, 3] -> 1, 2, 3
..."Elice" -> 'E', 'l', 'i', 'c', 'e'
...document.querySelectorAll("li") -> <li></li>, <li></li>, <li></li>
//여러 배열 결합
console.log([arr1, arr2]) // [ [ 1, 2, 3, 4, 5 ], [ 6, 7, 8, 9, 10 ] ]
console.log([...arr1, ...arr2]); // [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
// 함수의 인수로 여러 값 전달
const arr = [1, 2, 3, 4, 5];
console.log(...arr); // 1 2 3 4 5
function sum(a, b) { return a + b; }
const arrToSum = [45, 23];
sum(...arrToSum); // 68


//- 객체 또한 spread문법 사용가능, 단, 객체 리터럴 내부에서만 사용가능
const nameAndAge = { name: 'John', age: 30 }

const person = {
  ...nameAndAge,
  city: 'New York'
};

console.log(person);
// {
//   name: 'John',
//   age: 30,
//   city: 'New York'
// }

```


예시: 사용자가 쇼핑몰에서 스크롤을 맨 아래로 내리면 20개의 상품을 부르는 무한스크롤 구현

---
### 템플릿 리터럴

문자열 내부에 변수나 표현식을 포함해야 할 떄, ``` `` ``` 백틱 기호와 `${}`를 이용하여 편리하게 문자열을 작성할 수 있다.
더하기 없이 작업가능하므로, 직관적이다.
`
```
const name = "Hellobit";
const age = 20;

// 기존
console.log("My name is " + name + " and I am " + age + " years old.");

// 템플릿 리터럴 사용
console.log(`My name is ${name} and I am ${age} years old.`);
```

---

### 프로퍼티/메서드 축약

객체 리터럴에서 프로퍼티의 이름과 변수 이름이 동일할 때, 해당 프로퍼티 이름을 생략할 수 있다.

```
const name = "Hellobit";
const age = 20;

const hellobit1 = {
  name: name,
  age: age
}

// 프로퍼티 축약 사용
const hellobit2 = {
  name,
  age
}

console.log(hellobit1); // { name: 'Hellobit', age: 20 }
console.log(hellobit2); // { name: 'Hellobit', age: 20 }
```


---

## 02_배열 메서드

---
### 배열 메서드

**고차 함수(Higher-Order Functions)**: 함수를 인자로 받고나, 함수를 반환하는 함수.
```
// 고차 함수: 함수를 인자로 받음
function repeat(n, action) {
  for (let i = 0; i < n; i++) {
    action(i);
  }
}

// 사용 예제
repeat(3, console.log); // 0 1 2
repeat(3, (index) => console.log(`Hello ${index}`)); // Hello 0, Hello 1, Hello 2


// 고차 함수: 함수를 반환함
function createMultiplier(multiplier) {
  return function(value) {
    return value * multiplier;
  };
}

// 사용 예제
const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15


```

**콜백 함수**: 함수를 인자로 받는 고차 함수에서, 인자로 넘겨주는 함수
- forEach, map, filter, reduce 등이 있다. 배열에 내장된 배열 메서드에 콜백함수를 전달하면 각 원소에 대해 콜백 함수를 호출하게 된다.

```
// 고차 함수: 함수를 인자로 받음
function repeat(n, action) {
  for (let i = 0; i < n; i++) {
    action(i);
  }
}

// 사용 예제
// 아래 예제에서 전달되는 'console.log'와 화살표 함수가 콜백 함수에 해당합니다.
repeat(3, console.log); // 0 1 2
repeat(3, (index) => console.log(`Hello ${index}`)); // Hello 0, Hello 1, Hello 2
```

콜백함수들의 동작


**forEach**
- `forEach`배열의 각 요소에 대해 콜백 함수를 한 번씩 순서대로 실행한다.
- 콜백 함수에는 각 차례의 배열 요소와 해당 요소의 인덱스 값이 인수로 전달된다.
- 반환 값은 없다.

```
const numbers = [1, 2, 3, 4, 5];

numbers.forEach((num, index) => {
  console.log(`Index ${index}: ${num}`);
});

// 출력:
// Index 0: 1
// Index 1: 2
// Index 2: 3
// Index 3: 4
// Index 4: 5
```

**map**

- `map`은 배열의 각 요소에 대해 콜백 함수를 실행한 반환 값을 모아 새로운 배열을 반환한다.
- 콜백 함수에는 각 차례의 배열 요소와 해당 요소의 인덱스 값이 인수로 전달된다.
- 원래 배열의 값은 변경되지 않는다.

```
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(num => num * 2);

console.log(doubled); // [2, 4, 6, 8, 10]
```

**filter**

- `filter`는 배열의 각 요소에 대해 특정 조건을 만족하는 요소를 모아 새로운 배열을 반환한다.
- 콜백 함수에는 각 차례의 배열 요소와 해당 요소의 인덱스 값이 인수로 전달된다.
- 콜백 함수는 조건의 결과를 boolean 값으로 반환해야 한다.
- 원래 배열의 값은 변경되지 않는다.


```
const numbers = [1, 2, 3, 4, 5];

const evenNumbers = numbers.filter(num => num % 2 === 0);

console.log(evenNumbers); // [2, 4]
```


**reduce**

- `reduce`는 배열의 각 요소에 대해 콜백 함수를 호출하여 누적된 결과를 반환한다.
- 두 번째 인수로 초깃값을 지정할 수 있다.
- 콜백 함수에는 이전 단계까지의 누적 값과 현재 요소 값이 인수로 전달된다.
- 콜백 함수는 누적 값과 현재 요소 값으로 계산한 결과를 반환해야 한다.

```
const numbers = [1, 2, 3, 4, 5];

// 끝에 있는 0은 '초깃값'을 의미합니다.
const sum = numbers.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

console.log(sum); // 15
```

---
## 03_내장 객체

---
### 내장 객체 1


**내장 객체**
- ﻿﻿자바스크립트는 여러 용도에 활용하는 객체를 내장하고 있다.
- ﻿﻿숫자 다루기, 문자 다루기, 날짜 다루기, JSON 객체 다루기 등에 유용한 객체를 제공한다.
- ﻿﻿핵심 내장 객체들의 기능을 이해하면, 실제 프로젝트에서 유용하게 활용할 수 있다.



**window**
- DOM document를 포함하는 브라우저 창을 나타내는 객체.
- 현재 창의 정보를 얻거나, 창을 조작할 수 있다.
- (브라우저 환경에서는 window 객체가 전역 객체이다.)

```
const targetURL = "https://www.naver.com";
const windowSize = "height=S(window.innerHeight), width=$(window.innerWidth}';
window.open(targetURL, "Target", windowSize);
```


**document**
- 브라우저에 로드된 웹 페이지에 대한 객체.
- 문서의 title, URL 등의 정보를 얻을 수 있고, 요소 생성, 검색 등의 기능을 제공한다.
```
function printDocumentInfo() { console. 1og("문서 URL : ", document.URL);
console.Log("문서 타이틀 : ", document. title);
console.log("모든 노드 :", document.querySeLectorALL("*"));
}
```

**Number**
- 자바스크립트의 number 자료형을 감싸는 객체로, 유의미한 상수값, 숫자를 변환하는 메서드 등을 제공한다.
```
function changeToUsd(krw) {
const rate = 1046;
return (krw / rate). toFixed(2);
}
const krw = 1000000;
console.log(changeToUsd(krw)) ; // '956.02'
```

**Math**
- 기본적인 수학 연산 메서드, 상수를 다루는 객체입니다.
```
function getMaxDiff(nums) {
  return Math.max(...nums) - Math.min(...nums);//여러 숫자를 인자로 받아 최대, 최소 리턴
}
getMaxDiff([-1, -4, -7, 11]); // 18
```

- **Math.random**. **Math.floor**
	- **Math.random**은 0에서 1 사이의 float number(실수)를 랜덤으로 구합니다.
	- **Math.floor**는 소숫점 이하 숫자를 버립니다.
```
function getRandomNumberInRange(min, max) {
	  return Math.floor(Math.random() * (max - min + 1)) + min;
	}
	console.log(getRandomNumberInRange(50, 100));
```

---
### 내장객체2


**Date**
- 특정 시점의 날짜를 표시하기 위한 객체입니다.
- 날짜와 관련된 작업을 하기 위한 여러 메서드를 포함하고 있습니다.
```
function isWeekend(today) {
  let day = today.getDay();
  return day === 0 || day === 6;
}
console.log(isWeekend(new Date("2024/9/14")));
```

- **setDate** 등의 메서드로 시간을 설정한다.
- **toDateString** 메서드는 특정 포맷의 날짜로 문자열을 반환한다.
```
function addDays(date, days) {
  date.setDate(date.getDate() + days);
  return date.toDateString();
}

addDays(new Date("2024/9/22"), 100); // 'Tue Dec 31 2024'
```

- **getTime**은 1970.01.01 시점부터 흐른 시간을 밀리초단위로 반환한다.
```
function timeDiff(date1, date2) {
  return date2.getTime() - date1.getTime();
}

let dayTime = 60 * 24 * 60 * 1000;
function fromNow(date) {
  let diff = timeDiff(date, new Date());
  return `${Math.floor(diff / dayTime)} days ago...`;
}

fromNow(new Date("2024/03/23")); // 예시: '61 days ago...'
```



**String**
- 문자열을 조작하기 위한 여러 메서드를 포함한다
```
"hello".toUpperCase();               // 'HELLO'
"Daniel,Kim,SW".split(',');          // [ 'Daniel', 'Kim', 'SW' ]
"Daniel,Kim,SW".replace(',', ' ');   // 'Daniel Kim,SW'
"Daniel,Kim,SW".includes("Kim");     // true
"  Daniel,Kim,SW  ".trim();          // 'Daniel,Kim,SW'
"Daniel,Kim,SW".indexOf("Kim");      // 7
```


**JSON**
- 자바스크립트 객체를 직렬화 / 역직렬화 하는데 사용되는 객체입니다.
- 데이터 통신 과정에서 자주 사용됩니다.
```
// 객체 직렬화 (자바스크립트 객체를 문자열로 변환)
JSON.stringify({ name: "Daniel", age : 12}) // '{"name":"Daniel","age":12}'

// 역직렬화 (문자열을 다시 자바스크립트 객체로 변환)
JSON.parse('{"name":"Daniel","age":12}') // { name: 'Daniel', age: 12 }
```





---

### 04_비동기 처리의 원리

---
### 타이머 함수

타이머 함수 : 코드의 실행시간을 제어하는 함수. 함수 호출을 예약할 수 있다. 시간기반 동작을 가능하게 해준다
- setTimeout
- setInterval
**setTimeout:** 특정 시간 후에 콜백 함수가 호출되도록 예약할 수 있다. 두번째 인수로 시간을 전달하며, 단위는 밀리초(ms)이다.
```
console.log('3초 후에 메시지가 출력됩니다.');

setTimeout(() => {
  console.log('3초가 지났습니다!');
}, 3000);
```
- 세번째 이후 인수로는 콜백함수에 전달될 인수를 전달 가능. 인자 전달을 위해 함수를 감쌀 필요가 없음
```
setTimeout((name) => console.log(`Hello, ${name}!`), 2000, "Elice") // 2초 후에 'Hello, Elice!' 출력
```


**setInterval:** 숫자 형태의 timeout id를 반환한다.(브라우저 환경 기준) clearTimeout함수에 이 id를 인수로 넘겨 호출하면 해당 timeout을 제거할 수 있다.
특정 시간마다 콜백 함수가 호출되도록 예약할 수 있다. 두번쨰 인수로 사긴을 전달하며, 단위는 ms이다.
```
const timeoutId = setTimeout(() => console.log(`Hello!`), 2000);

console.log(timeoutId); // 1
clearTimeout(timeoutId);
```

```
let count = 0;

const intervalId = setInterval(() => {
  count++;
  console.log(`Interval 실행: ${count}초 경과`);
}, 1000); // 1초마다 실행
```




---
### 실행 컨텍스트

우리의 코드는 jsengine 을 통해 파싱, 실행된다. Chrome 브라우저의 경우에는 V8엔진을 사용한다.
(이를 파싱하고, 컴파일하고, 실행한다. 고 한다). 이 떄 실행 컨텍스트가 생성된다


자바스크립트 실행 컨텍스트 (Execution Context) 생성 과정
1. 생성 단계 (Creation Phase) - 핵심 역할: 변수 선언문 먼저 저장 - 자바스크립트 엔진이 코드를 훑어보며 변수나 함수 선언들을 메모리에 미리 등록해 둔다.
2. 실행 단계 (Execution Phase) - 핵심 역할: 나머지 코드 실행 및 변수 값 할당 - 코드가 위에서부터 한 줄씩 순차적으로 실행된다.

실행컨텍스트
- 각 스코프가 실행되기 **직전**에 생성된다. (전역 실행 컨택스트는 가장 먼저 생성됨)
콜스택(실행컨텍스트 스택)
- 모든 실행컨텍스트를 쌓아가며 관리함.
![[Pasted image 20260606175524.png]]

- 이렇게 쌓이다가 return 문을 만나거나, 함수의 끝에 도달시 함수 컨텍스트는 제거됨. 전역 코드까지 모두 실행된다면 스택은 비어있는상태가 된다.


즉, js는한가지 스택만 가질수 있다.  싱글스레드 기반 언어이다.

---
### 동기와 비동기

**싱글스레드의 문제점:** 싱글르레드에서는 한번에 하나의 작업만 수행하여 작업순서가 보장된다는 장점이있지만, 앞선 작업이 종료되기 전까찌 이후 작업을 시작하지 못한다는 문제가 있다. 즉, 블로킹이 발생한다.
- **블로킹(Blocking)**: 앞선 작업이 종료되기 전까지 이후 작업을 시작하지 못한다는 문제

**동기 처리 방식** : 작업이 순차적으로 실행되며, 현재 작업이 환요될 떄까지 다음 작업이 대기하는방식

**비동기 처리 방식:** 작업 시작 이후 완료 여부와 상관없이 다음 작업을 즉시 실행하며, 작업 완료시에 콜백 함수나 프로미스 등을 통해 결과를 처리하는방식
비동기 처리방식 종류
- 타이머 함수
- Ajaxx
- 이벤트 핸들러


---

### 비동기 동작원리

브라우저는 이벤트 루프와 태스트 큐를 이용해 비동기를 처리한다.

**태스크 큐 (Task Queue):** 이벤트 핸들러 및 비동기 함수의 콜백 함수가 잠시 저장되는 큐 영역 
**이벤트 루프 (Event Loop):** 콜 스택이 비어 있고, 태스크 큐에 함수가 존재하면 이를 콜 스택으로 이동시
킴


![[Pasted image 20260606181314.png]]


1 > 3 > 2 여야할것 같은데, 실제로는 1 > 2 > 3로 동작함


![[Pasted image 20260606181754.png]]
전역 실행 컨텍스트가 Call Stack을 점유하고 있기 떄문에, Task Queue의 setTimeout(대기시간 0 초)가 Call Stack으로 이동되지 않기 때문.
콜스택이 비어야, 이벤트 루프가 태스큐 큐에 있는 작업을 콜스택으로 이동시킨다.

---
### 05_Promise
