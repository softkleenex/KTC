import asyncio

async def task_a():
	print("A: start")
	await asyncio.sleep(1)  # 여기서 제어권 양보
	print("A: end")

async def task_b():
	print("B: start")
	await asyncio.sleep(2)
	print("B: end")

async def main():
	await asyncio.gather(task_a(), task_b())

asyncio.run(main())

# A: start  [0.0초] task_a 시작. 첫 번째 프린트 출력 후 sleep(1)을 만나 제어권을 넘김
# B: start  [0.0초] task_a가 넘겨준 제어권을 받아 task_b 시작. sleep(2)를 만나 제어권 넘김
# -------- (약 1초 동안 두 태스크 모두 대기 상태 / 이벤트 루프 작동 중) --------
# A: end    [1.0초] 1초가 지나 일어난 task_a가 남은 코드 실행 후 완전히 종료
# -------- (다시 약 1초 동안 task_b의 남은 시간 대기) --------
# B: end    [2.0초] 총 2초가 지나 일어난 task_b가 마지막 코드 실행 후 완전히 종료