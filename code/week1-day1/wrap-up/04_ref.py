# for — 리스트를 순서대로 순회
messages = ["안녕", "날씨?", "감사"]
for i, msg in enumerate(messages):
    print(f"{i+1}번: {msg}")

# 출력 결과
# 1번: 안녕
# 2번: 날씨?
# 3번: 감사

# while — 조건이 True인 동안 반복 (카운터 빠뜨리면 무한 루프!)
retry = 0
while retry < 3:
    print(f"재시도 {retry + 1}회")
    retry += 1
    
# 출력 결과
# 재시도 1회
#재시도 2회
#재시도 3회