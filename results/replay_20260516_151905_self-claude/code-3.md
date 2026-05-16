# 이진 탐색  (code)  [replay/self-claude]

**문제**
> 정렬된 정수 배열 nums와 target이 주어진다. target의 인덱스를 반환하고, 없으면 -1을 반환하는 이진 탐색 함수를 Python으로 작성하라. 코드만, 시간복잡도 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
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

## 🅱️ (shown as B, originally B (Claude-Opus))
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

## ⚖️ 심판 (CLAUDE_OPUS_4_5_20251101)
WINNER: TIE
REASON: 두 답변 모두 정확한 이진 탐색 구현과 O(log n) 시간복잡도를 제시했으며, 변수명(lo/hi vs left/right)과 주석 위치(코드 내 vs 별도 줄)만 다를 뿐 기능적으로 동등하다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
