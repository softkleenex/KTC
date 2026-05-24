scores = [85, 42, 91, 67, 78]

passed = [s for s in scores if s >= 80]    # 80점 이상만 → [85, 91]
labels = [f"{s}점" for s in scores]         # 문자열로 변환 → ["85점", ...]

print(passed)
print(labels)