# **kwargs — 이름 있는 추가 옵션 (딕셔너리로 받음)
def call_ai(prompt, **kwargs):
    options = {"model": "gpt-4", "temperature": 0.7}  # 기본값
    options.update(kwargs)                            # 추가 옵션으로 덮어씀
    print(f"프롬프트: {prompt}")
    print(f"옵션: {options}")

call_ai("안녕!")
# 프롬프트: 안녕!
# 옵션: {'model': 'gpt-4', 'temperature': 0.7}

call_ai("사진 분석", model="gpt-4o", temperature=0.2)
# 프롬프트: 사진 분석
# 옵션: {'model': 'gpt-4o', 'temperature': 0.2}