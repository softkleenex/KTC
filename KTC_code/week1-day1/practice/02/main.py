# main.py
# utils 폴더의 validators.py 파일에서 validate_message 함수를 가져옵니다.
from utils.validators import validate_message

# [출력 결과 확인]
# 1. 빈 문자열 입력 시
print(validate_message(""))            
# 👉 출력: 메시지를 입력하세요

# 2. 공백만 3칸 입력 시 (strip()에 의해 빈 문자열이 됨)
print(validate_message("   "))         
# 👉 출력: 메시지를 입력하세요

# 3. 정상 메시지 입력 시 (앞뒤 공백은 깎여서 나옴)
print(validate_message("  안녕하세요  "))   
# 👉 출력: 안녕하세요

# 4. 500자가 넘는 긴 메시지 입력 시
print(validate_message("a" * 600))     
# 👉 출력: 메시지가 너무 깁니다