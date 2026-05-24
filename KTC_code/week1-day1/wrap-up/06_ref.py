# ① 챗봇 설계도(Class) 작성하기
class ChatBot:
    # __init__ : 챗봇이 딱 생성되는 순간(앱을 처음 켰을 때) 무조건 1번 실행되는 초기 세팅
    def __init__(self, name):
        self.name = name       # "내(self) 이름은 전달받은 이름으로 세팅해라"
        self.history = []      # "내(self) 대화창은 빈 리스트([])로 깨끗하게 시작해라"

    # 메서드 : 이 챗봇이 할 수 있는 '행동' (대화하기)
    def chat(self, msg):
        self.history.append(msg) # 내가 받은 메시지를 내(self) 대화창에 저장해라
        return f"[{self.name}] 대화 기록이 {len(self.history)}개 있습니다."


# ② 설계도를 보고 실제 챗봇(Instance) 2개 만들어내기
# 이때 __init__이 자동 실행되면서 이름과 빈 대화창이 각각 세팅됨!
bot_1 = ChatBot("카카오봇")
bot_2 = ChatBot("마카오봇")

# ③ 만들어진 챗봇과 대화해보기 (가장 중요한 부분: 둘은 대화가 안 섞임!)
print(bot_1.chat("안녕?"))      # 출력: [카카오봇] 대화 기록이 1개 있습니다.
print(bot_1.chat("오늘 날씨?")) # 출력: [카카오봇] 대화 기록이 2개 있습니다.

# 마카오봇은 카카오봇과 완전히 독립된 챗봇이므로 대화 기록이 0개부터 시작함!
print(bot_2.chat("반가워!"))    # 출력: [마카오봇] 대화 기록이 1개 있습니다.