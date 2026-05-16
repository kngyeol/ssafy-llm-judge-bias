# Two Sum  (code)  [replay/self-gpt]

**문제**
> Python으로 'Two Sum' 문제를 풀어라. 입력: 정수 배열 nums와 target. 출력: nums[i] + nums[j] == target 인 (i, j) 인덱스. 한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로.

## 🅰️ (shown as A, originally A (GPT-5.2))
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

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen: return [seen[target - n], i]
        seen[n] = i
```

**시간복잡도: O(n)**

## ⚖️ 심판 (GPT_5_2)
WINNER: A
REASON: A는 요구한 출력 형식(인덱스 쌍)과 시간복잡도 표기를 코드 내 한 줄로 포함해 요구사항을 더 완전하게 충족하며, 해가 없을 때의 처리도 명확하다. B는 시간복잡도를 코드 밖에 따로 적었고(“코드만” 위반), 출력이 튜플이 아닌 리스트이며 해가 없을 때 반환이 없다(감점).

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
