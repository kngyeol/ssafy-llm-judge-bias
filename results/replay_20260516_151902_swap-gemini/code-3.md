# 이진 탐색  (code)  [replay/swap-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: 두 모델 모두 정확하고 효율적인 이진 탐색 코드를 제공했지만, A는 시간복잡도를 코드 블록과 분리하여 문제 요구사항인 "코드만, 시간복잡도 한 줄"에 더 정확하게 부합합니다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **B** 손이 올라감.
