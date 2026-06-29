# *args — 개수가 정해지지 않은 위치 인자 (튜플로 받음)
def sum_all(*args):
    print(args)                 
    return sum(args)

print(sum_all(1, 2, 3))         # 6
print(sum_all(10, 20, 30, 40))  # 100