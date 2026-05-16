# Two Sum  (code)  [replay/stylometric-gemini]

**문제**
> Python으로 'Two Sum' 문제를 풀어라. 입력: 정수 배열 nums와 target. 출력: nums[i] + nums[j] == target 인 (i, j) 인덱스. 한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
from typing import List, Tuple

def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    raise ValueError("No solution")

# O(n) time, O(n) space
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
def two_sum(nums, target):
    idx = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in idx:
            return [idx[need], i]
        idx[x] = i
```

**시간복잡도: O(n)**

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: A는 해결책이 없는 경우를 처리하고 타입 힌트를 제공하여 더 견고하고 가독성이 높은 코드를 제공하며, 시간 복잡도 설명도 코드 내에 깔끔하게 포함했습니다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
