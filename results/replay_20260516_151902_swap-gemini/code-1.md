# Two Sum  (code)  [replay/swap-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: B
REASON: B는 타입 힌트와 명시적인 오류 처리를 통해 더 견고하고 가독성 높은 코드를 제공하며, 반환 값도 문제에서 명시된 튜플 형식에 더 가깝습니다. 추가로 제공된 공간복잡도 정보는 유익합니다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
