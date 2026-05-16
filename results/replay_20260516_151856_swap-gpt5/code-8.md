# 피보나치 메모이제이션  (code)  [replay/swap-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: B
REASON: B는 lru_cache로 깔끔하게 메모이제이션하고 음수 입력 검증까지 포함; A는 동작은 맞지만 기본 인자로 mutable dict를 사용한 점이 감점 요인.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
