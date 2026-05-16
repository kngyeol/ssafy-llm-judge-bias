# Two Sum  (code)  [replay/self-claude]

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

## ⚖️ 심판 (CLAUDE_OPUS_4_5_20251101)
WINNER: TIE

REASON: 두 답변 모두 동일한 해시맵 방식으로 O(n) 시간복잡도의 정확한 Two Sum 솔루션을 제시했으며, A는 타입힌트와 예외처리가 더 견고하고 B는 더 간결하지만 핵심 알고리즘과 요구사항 충족도는 동등함.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
