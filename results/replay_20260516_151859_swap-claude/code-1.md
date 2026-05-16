# Two Sum  (code)  [replay/swap-claude]

**문제**
> Python으로 'Two Sum' 문제를 풀어라. 입력: 정수 배열 nums와 target. 출력: nums[i] + nums[j] == target 인 (i, j) 인덱스. 한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로.

## 🅰️ (shown as A, originally B (Claude-Opus))
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen: return [seen[target - n], i]
        seen[n] = i
```

**시간복잡도: O(n)**

## 🅱️ (shown as B, originally A (GPT-5.2))
```python
from typing import List, Tuple

def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], i)
        seen[x] = i
    raise ValueError("No solution")

# Time Complexity: O(n), Space Complexity: O(n)
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: 문제가 "한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로" 요구했는데, A는 핵심 코드와 시간복잡도만 간결하게 제시한 반면, B는 type hints, 예외처리, 공간복잡도 등 요구하지 않은 추가 요소를 포함해 과도하게 복잡하고 요구사항을 정확히 따르지 않음.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **B** 손이 올라감.
