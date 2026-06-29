# utils/validators.py

def validate_message(message):
    """메시지 유효성 검사 — Early Return 패턴으로 구현"""
    # ✏️ [실습] 아래 조건을 순서대로 Early Return 패턴으로 구현하세요
    # 1. message가 None이거나 빈 문자열이면 → "메시지를 입력하세요" 반환
    # 2. len(message) > 500이면 → "메시지가 너무 깁니다" 반환
    # 3. 정상이면 → message.strip() 반환

    if not message or message.strip() == "":
        return "메시지를 압력하세요"
    elif len(message) > 500:
        return "메시지가 너무 깁니다"
    else:
        return message.strip()

    pass  # 여기에 코드를 작성하세요
