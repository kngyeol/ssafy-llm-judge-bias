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
    return fib(n - 1) + fib(n - 2)
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

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: A는 `lru_cache`로 안전하고 표준적인 메모이제이션을 구현했으며, B는 mutable default argument(`memo={}`)를 사용해 함수 재호출 시 이전 캐시가 남아있는 심각한 버그가 있음. B는 불필요한 테스트 출력도 포함. A가 코드 품질과 정확성에서 명백히 우수.
