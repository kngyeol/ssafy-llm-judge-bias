# 피보나치 메모이제이션  (code)  [replay/stylometric-claude]

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

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: 두 답변 모두 메모이제이션을 정확히 구현했으나, A는 `@lru_cache` 데코레이터를 사용해 더 간결하고 Pythonic하며, 입력 검증도 포함했다. B는 `memo={}` 기본 인자의 mutable default argument 안티패턴을 범했고(함수 재호출 시 메모리 공유 문제), 불필요한 `print(fib(50))` 출력문이 포함되어 "코드만" 요구사항을 벗어났다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
