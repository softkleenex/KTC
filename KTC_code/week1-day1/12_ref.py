from dataclasses import dataclass, field
from typing import List

# 기존 방식 — 반복적인 코드가 많음
class UserOld:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        # !r을 사용하면 문자열에 자동으로 따옴표(')가 붙어 출력됩니다.
        return f"UserOld(name={self.name!r}, age={self.age})"

u1 = UserOld("카카오", 23, "k@k.com")
u2 = UserOld("카카오", 23, "k@k.com")

print(u1)        # 출력: UserOld(name='카카오', age=23) -> __repr__ 덕분에 이렇게 나옴
print(u1 == u2)  # 출력: False -> __eq__를 안 만들었기 때문에 메모리 주소로 비교함

print("-" * 50)

# @dataclass 방식 — __init__, __repr__, __eq__ 자동 생성
@dataclass
class User:
    name: str
    age: int
    email: str
    tags: List[str] = field(default_factory=list)  # 리스트 기본값은 반드시 field() 사용
    
    # 일반 클래스에서는 tags = [] 로 쓰면 모든 인스턴스가 리스트를 공유하는 치명적 버그가 생깁니다.
    # @dataclass는 이를 방지하기 위해 tags = [] 라고 쓰면 아예 ValueError를 발생시킵니다.
    # 따라서 "인스턴스마다 새 리스트를 만들어라"라는 의미로 field(default_factory=list)를 써야 합니다.

user1 = User(name="카카오", age=23, email="kakao@kakao.com")
user2 = User(name="카카오", age=23, email="kakao@kakao.com")

print(user1)           # 출력: User(name='카카오', age=23, email='kakao@kakao.com', tags=[])
print(user1 == user2)  # 출력: True -> 값이 같으면 같은 객체로 판단 (__eq__ 자동 구현)