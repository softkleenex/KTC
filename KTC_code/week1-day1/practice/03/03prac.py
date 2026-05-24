# 부모 클래스: 기본형 챗봇
class BasicBot:
    def say(self, msg):
        return f"🤖 [기본 응답]: {msg}"


# 자식 클래스: 부모의 특정 기능을 내 방식대로 '덮어쓴' 챗봇
class OverrideBot(BasicBot):
    # 부모와 '완전히 똑같은 이름'의 함수를 만들면 덮어쓰기(오버라이딩)가 됩니다.
    def say(self, msg):
        return f"✨ [덮어쓴 응답]: {msg}"

# 1. 기본형 봇에게 말을 걸었을 때
basic = BasicBot()
print("1. 기본형 봇의 결과:")
print(basic.say("안녕하세요"))

print("-" * 60)

# 2. 덮어쓰기형 봇에게 똑같이 말을 걸었을 때
override = OverrideBot()
print("2. 덮어쓰기형 봇의 결과:")
print(override.say("안녕하세요, 저는 님을 도우러 온 사람입니다."))  # 똑같은 say를 호출했지만 출력 결과가 다름

# BasicBot을 상속받는 EnglishBot 클래스를 만드세요. 부모의 say 메서드를 오버라이딩하여, 입력받은 메시지 앞에 "Answer: "를 붙여서 반환하도록 수정해 보세요.
class EnglishBot(BasicBot):
    def say(self, msg):
        return f"Answer: {msg}"

e_bot = EnglishBot()
print(e_bot.say("Hello"))
