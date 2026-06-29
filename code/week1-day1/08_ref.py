# 가상의 데이터 세팅
user_profile = {"name": "김카카오", "balance": 50000}
product_item = {"name": "파이썬 마스터 북", "price": 20000}


# ❌ 1. IF 중첩 방식 (기존 방식)
def process_order_nested(user, item, quantity):
    if user:
        if item:
            if quantity > 0:
                if user["balance"] >= item["price"] * quantity:
                    return "주문 완료"
    # 💡 맹점: 만약 조건 중 하나라도 실패하면? (아무것도 반환하지 않아 None이 됨)


# ✅ 2. Early Return 방식 (추천 방식)
def process_order_early(user, item, quantity):
    if not user:
        return "로그인이 필요합니다"
    
    if not item:
        return "상품 정보가 없습니다"
        
    if quantity <= 0:
        return "수량은 1 이상이어야 합니다"
        
    if user["balance"] < item["price"] * quantity:
        return "잔액이 부족합니다"

    return "주문 완료"


# --- 출력 결과 ---

print("=== Case 1: 정상 주문 (수량 2개 = 40,000원) ===")
print("중첩 IF 결과:", process_order_nested(user_profile, product_item, 2))
print("Early Return 결과:", process_order_early(user_profile, product_item, 2))
print("-" * 50)

print("=== Case 2: 실패 상황 (잔액 부족! 수량 3개 = 60,000원) ===")
print("중첩 IF 결과:", process_order_nested(user_profile, product_item, 3))
print("Early Return 결과:", process_order_early(user_profile, product_item, 3))
print("-" * 50)

print("=== Case 3: 실패 상황 (수량을 0개로 잘못 입력) ===")
print("중첩 IF 결과:", process_order_nested(user_profile, product_item, 0))
print("Early Return 결과:", process_order_early(user_profile, product_item, 0))