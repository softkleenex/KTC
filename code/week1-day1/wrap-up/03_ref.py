# 비교: ==, !=, >, <, >=, <=
# 논리: and, or, not, in

user_type = "vip"
message_count = 150

# 먼저 VIP인지 일반인지 확인
if user_type == "vip":
    
    # 메시지 개수에 따라 추가 분류
    if message_count < 200:
        print("VIP 프리미엄 응답")
    else:
        print("VIP이지만 한도 초과")

else:
    print("일반 응답")