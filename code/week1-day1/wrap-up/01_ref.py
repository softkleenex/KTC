# 아래에서 활용할 예시 데이터
chat_history = ["안녕", "날씨?", "감사"]
user = {"name": "카카오", "age": 23}
user_name = "카카오"

# str — 텍스트 깔끔하게 다듬기
print("  hello  ".strip())              # "hello" (양옆 공백 제거)
print("hello world".split())            # ["hello", "world"] (단어 쪼개기)
print(f"안녕, {user_name}님!")           # f-string: 변수를 문장 안에 쏙 넣기

# list — 목록(데이터) 추가하고 찾기
chat_history.append("또 올게요")         # 리스트 맨 뒤에 데이터 추가
print(chat_history[0])                   # "안녕" (첫 번째 데이터 꺼내기)
print(chat_history[-1])                  # "또 올게요" (가장 마지막 데이터 꺼내기)

# dict — 이름표(Key)로 정보 꺼내기
print(user["name"])                      # "카카오"
print(user.get("email", "없음"))         # 키가 없어도 에러 없이 "없음" 반환3
