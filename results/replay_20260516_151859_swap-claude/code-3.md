# 이진 탐색  (code)  [replay/swap-claude]

**문제**
> 정렬된 정수 배열 nums와 target이 주어진다. target의 인덱스를 반환하고, 없으면 -1을 반환하는 이진 탐색 함수를 Python으로 작성하라. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally B (Claude-Opus))
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**시간복잡도: O(log n)**

## 🅱️ (shown as B, originally A (GPT-5.2))
```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Time: O(log n)
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 올바른 이진 탐색 구현이며, 로직이 동일하고(변수명만 left/right vs lo/hi로 다름), 시간복잡도 O(log n)도 정확히 명시했다. A는 elif 사용, B는 if 연속 사용의 스타일 차이일 뿐 기능적으로 동등하며, 문제 요구사항을 모두 충족한다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
