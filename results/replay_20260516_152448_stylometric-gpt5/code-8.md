# 피보나치 메모이제이션  (code)  [replay/stylometric-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: A
REASON: 둘 다 메모이제이션으로 O(n)이며 n=50을 빠르게 계산하지만, B는 불필요한 print 출력이 있어 요구사항(함수와 시간복잡도 한 줄)에 덜 부합한다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
