# 피보나치 메모이제이션  (code)

**문제**
> Python으로 메모이제이션을 사용한 피보나치 함수 fib(n)을 작성하라. n=50도 빠르게 계산되어야 한다. 코드만, 시간복잡도 한 줄.

## 🅰️  GPT-5.2
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

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (GPT_5)
WINNER: A
REASON: A는 lru_cache로 메모이제이션을 깔끔히 적용하고 불필요한 출력 없이 요구사항을 충족하며, B는 mutable 기본 인자 사용과 불필요한 print 포함으로 감점.
