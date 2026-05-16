# Two Sum  (code)  [replay/swap-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: B
REASON: B는 (i, j) 튜플을 반환하고 시간복잡도를 코드 내 한 줄 주석으로 제시해 "코드만" 요구를 더 잘 충족한다. 감점: A는 리스트 반환 및 코드 블록 외부에 추가 줄을 둠, B는 불필요한 공간복잡도 표기(주석).

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
