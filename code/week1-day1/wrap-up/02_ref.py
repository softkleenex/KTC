user_input = input("나이를 입력하세요: ")  # input() -> 항상 문자열(str) 자료형으로 반환
age = int(user_input)                 # str → int 변환
print(f"내년엔 {age + 1}살이에요")

# str(), float()도 같은 방식