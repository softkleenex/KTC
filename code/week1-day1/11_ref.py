class ChatSession:
    def __init__(self, user_name):
        self.user_name = user_name     # 상태: 이 객체만의 데이터
        self.messages = []

    def add_message(self, role, content):   # 책임: 이 객체가 할 수 있는 일
        self.messages.append({"role": role, "content": content})

    def get_summary(self):
        return f"{self.user_name}의 대화 ({len(self.messages)}개)"

# 각 유저는 완전히 독립된 세션을 가진다
session_a = ChatSession("철수")
session_b = ChatSession("영희")

session_a.add_message("user", "안녕!")
print(session_a.get_summary())   # 철수의 대화 (1개)
print(session_b.get_summary())   # 영희의 대화 (0개) — 서로 영향 없음