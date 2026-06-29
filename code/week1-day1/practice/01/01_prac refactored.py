# 아래를 Early Return 패턴으로 바꿔보세요
def send_message(user, message):
    if not user:
        return {"status": "error", "reason": "사용자 없음"}
    else:
        if not message:
            return {"status": "error", "reason": "메시지 너무 김"}
        else:
            if len(message) > 200:
                return {"status": "ok", "msg": message}

    return {"status": "ok", "msg": message}
