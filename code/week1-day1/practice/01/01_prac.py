# 아래를 Early Return 패턴으로 바꿔보세요
def send_message(user, message):
    if user:
        if message:
            if len(message) > 200:
                return {"status": "ok", "msg": message}
            else:
                return {"status": "error", "reason": "메시지 너무 김"}
        else:
            return {"status": "error", "reason": "메시지 없음"}
    else:
        return {"status": "error", "reason": "사용자 없음"}

