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

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: A는 Python의 표준 라이브러리를 활용하여 메모이제이션을 정확하고 파이써닉하게 구현했으며, "코드만" 요구사항을 완벽히 지켰습니다. B는 가변 기본 인자(`memo={}`)를 사용하여 메모이제이션을 구현하는 일반적인 실수를 저질렀고, 불필요한 `print` 문을 포함하여 요구사항을 위반했습니다.
