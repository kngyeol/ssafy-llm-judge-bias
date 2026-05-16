# 피보나치 메모이제이션  (code)  [replay/self-claude]

**문제**
> Python으로 메모이제이션을 사용한 피보나치 함수 fib(n)을 작성하라. n=50도 빠르게 계산되어야 한다. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
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

## 🅱️ (shown as B, originally B (Claude-Opus))
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

## ⚖️ 심판 (CLAUDE_OPUS_4_5_20251101)
WINNER: A

REASON: 두 답변 모두 O(n) 메모이제이션 피보나치를 정확히 구현했으나, A는 표준 라이브러리(`lru_cache`)를 활용한 더 Pythonic한 방식이고 음수 입력 검증까지 포함한 반면, B는 mutable default argument(`memo={}`) 안티패턴을 사용하여 함수 호출 간 상태가 공유되는 잠재적 버그 위험이 있음.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
