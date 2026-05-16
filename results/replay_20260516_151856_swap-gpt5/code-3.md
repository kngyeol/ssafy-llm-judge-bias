# 이진 탐색  (code)  [replay/swap-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: B
REASON: 두 코드 모두 정답이나, B는 시간복잡도를 코드 주석 한 줄로 제공해 "코드만, 시간복잡도 한 줄" 요구를 충실히 따르며 A는 코드 밖 굵은글씨로 표기해 형식 위반 감점.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
