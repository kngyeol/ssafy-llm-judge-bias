# Two Sum  (code)  [replay/stylometric-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: A
REASON: A는 해시맵으로 O(n) 풀이를 제시하고 튜플 반환 및 시간복잡도를 코드 주석 한 줄로 명시했으며, B는 시간복잡도를 코드 밖에 쓰고 무해결 시 처리가 없어 감점.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
