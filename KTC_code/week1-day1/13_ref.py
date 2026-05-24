class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0           # _ : "직접 접근 금지" 약속

    # 1. 검증된 통로 (입금)
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("입금액은 0보다 커야 합니다")
        self._balance += amount

    # 2. 검증된 통로 (출금)
    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("잔액 부족")
        self._balance -= amount

    # 3. 안전하게 읽기만 허용 (@property)
    @property
    def balance(self):
        return self._balance

account = BankAccount("카카오")
account.deposit(10000)

# ✅ 안전한 방식 (검증 로직 통과)
account.withdraw(3000)

print(f"현재 잔액: {account.balance}원")

# ❌ 위험한 방식 (직접 수정 시도)
# account.balance = 1000000    # 에러 발생! (@property라 수정 불가)
# account._balance = 1000000   # 가능은 하지만, 추천하지 않는 코드