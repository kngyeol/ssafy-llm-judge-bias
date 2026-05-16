# Two Sum  (code)  [replay/stylometric-claude]

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

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: 두 답변 모두 O(n) 해시맵 솔루션으로 알고리즘은 동일하나, A는 type hints 제공, 예외 처리 포함, 공간복잡도까지 명시하여 더 완전한 솔루션을 제시했고, B는 해가 없는 경우 암묵적 None 반환으로 불완전함.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
