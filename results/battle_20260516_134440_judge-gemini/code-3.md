# 이진 탐색  (code)

**문제**
> 정렬된 정수 배열 nums와 target이 주어진다. target의 인덱스를 반환하고, 없으면 -1을 반환하는 이진 탐색 함수를 Python으로 작성하라. 코드만, 시간복잡도 한 줄.

## 🅰️  GPT-5.2
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

# Time Complexity: O(log n)
```

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: 두 모델 모두 정확한 코드와 시간복잡도를 제시했지만, A는 시간복잡도를 코드 내 주석으로 처리하여 "코드만, 시간복잡도 한 줄"이라는 요구사항에 더 부합합니다.
