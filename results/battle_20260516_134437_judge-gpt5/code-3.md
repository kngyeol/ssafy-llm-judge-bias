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

# Time: O(log n)
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

## ⚖️  심판 (GPT_5)
WINNER: A
REASON: 둘 다 정답이지만 A는 코드만과 시간복잡도 한 줄 요구를 주석으로 충족했고, B는 코드 외 굵은 텍스트를 포함해 형식 요구를 위반했다.
