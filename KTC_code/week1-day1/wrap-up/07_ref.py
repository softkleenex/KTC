def parse_age(value):
    try:
        return int(value)
    except ValueError:
        print(f"'{value}'는 숫자가 아닙니다.")
        return None

print(parse_age("23"))      # 23
print(parse_age("hello"))   # 오류 메시지 출력 후 None 반환 (프로그램 계속 실행)