import { useState, useEffect } from "react";
import TimeLoopUI from "./TimeLoopUI";

export default function TimeLoopMission() {
  const [timeLeft, setTimeLeft] = useState(15);
  const [loopCount, setLoopCount] = useState(0);
  const [cluesFound, setCluesFound] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  const isSolved = cluesFound >= 3;

  // ================================================================
  // useEffect 1 — 타이머
  // ================================================================
  useEffect(
    () => {
      // [문제 1] isSolved 또는 isPaused 가 true 이면 early return 하세요.
      if (isSolved || isPaused) {
        return;
      }

      const interval = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            setLoopCount((c) => c + 1);
            return 15;
          }
          return prev - 1;
        });
      }, 1000);

      // [문제 2] interval 을 정리하는 cleanup 함수를 반환하세요.
      return () => {
        clearInterval(interval);
      };
    },
    // [문제 3] 의존성 배열을 채우세요.
    // 미션이 완수(isSolved)되거나 일시정지(isPaused) 상태가 바뀔 때마다 useEffect가 다시 실행되어야 합니다.
    [isSolved, isPaused]
  );

  // ================================================================
  // useEffect 2 — 탭 타이틀 업데이트
  // ================================================================
  useEffect(
    () => {
      document.title =
        loopCount > 0 ? `[루프 ${loopCount}회] 타임루프 작전` : "타임루프 작전";

      // [문제 4] 탭 타이틀을 "실습" 으로 되돌리는 cleanup 함수를 반환하세요.
      return () => {
        document.title = "실습";
      };
    },
    // [문제 5] 의존성 배열을 채우세요.
    // 탭 타이틀은 loopCount 값이 변경될 때마다 업데이트되어야 합니다.
    [loopCount]
  );

  function handleCollectClue() {
    if (!isSolved && cluesFound < 3) setCluesFound((c) => c + 1);
  }

  function handleTogglePause() {
    if (!isSolved) setIsPaused((p) => !p);
  }

  return (
    <TimeLoopUI
      timeLeft={timeLeft}
      loopCount={loopCount}
      cluesFound={cluesFound}
      isSolved={isSolved}
      isPaused={isPaused}
      onCollectClue={handleCollectClue}
      onTogglePause={handleTogglePause}
    />
  );
}



