# 피보나치 메모이제이션  (code)  [replay/stylometric-gemini]

**문제**
> Python으로 메모이제이션을 사용한 피보나치 함수 fib(n)을 작성하라. n=50도 빠르게 계산되어야 한다. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n은 0 이상이어야 합니다")
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

시간복잡도: O(n)

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

print(fib(50))  # 12586269025
```

**시간복잡도: O(n)**

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: A는 파이썬 내장 `lru_cache`를 사용하여 간결하고 파이썬스러운 메모이제이션을 구현했으며, 음수 입력에 대한 예외 처리까지 제공하여 더 견고합니다. B는 요청하지 않은 함수 실행 코드와 결과값을 포함했습니다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
