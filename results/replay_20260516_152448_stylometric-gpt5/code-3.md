# 이진 탐색  (code)  [replay/stylometric-gpt5]

**문제**
> 정렬된 정수 배열 nums와 target이 주어진다. target의 인덱스를 반환하고, 없으면 -1을 반환하는 이진 탐색 함수를 Python으로 작성하라. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
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

# 시간복잡도: O(log n)
```

## 🅱️ (shown as B, originally B (Claude-Opus))
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
```

**시간복잡도: O(log n)**

## ⚖️ 심판 (GPT_5)
WINNER: A
REASON: 두 코드 모두 정답이나 A는 코드 내 주석으로 시간복잡도 한 줄을 제공해 '코드만' 요구를 충족했고, B는 복잡도 문장을 코드 밖(마크다운)으로 작성해 형식 위반 감점.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
