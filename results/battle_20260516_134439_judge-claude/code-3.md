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

# Time complexity: O(log n)
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

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 정확한 이진 탐색 구현이며, 로직이 동일하고(변수명만 lo/hi vs left/right 차이), 시간복잡도 O(log n)을 명시했다. A는 elif 대신 if를 사용했으나 기능상 차이 없으며, 둘 다 문제 요구사항을 완벽히 충족한다.
