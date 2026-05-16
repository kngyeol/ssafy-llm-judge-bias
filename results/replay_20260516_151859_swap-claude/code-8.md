# 피보나치 메모이제이션  (code)  [replay/swap-claude]

**문제**
> Python으로 메모이제이션을 사용한 피보나치 함수 fib(n)을 작성하라. n=50도 빠르게 계산되어야 한다. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally B (Claude-Opus))
```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

print(fib(50))  # 12586269025
```

**시간복잡도: O(n)**

## 🅱️ (shown as B, originally A (GPT-5.2))
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

시간복잡도: O(n)

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: B

REASON: A는 mutable default argument (`memo={}`) 사용으로 함수 재호출 시 캐시가 누적되는 치명적 버그가 있고, B는 표준 라이브러리 `lru_cache`로 안전하게 구현했으며 입력 검증과 타입 힌트까지 제공해 코드 품질이 우수함. 둘 다 O(n)이지만 A는 실무에서 사용 불가능한 결함 코드.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
