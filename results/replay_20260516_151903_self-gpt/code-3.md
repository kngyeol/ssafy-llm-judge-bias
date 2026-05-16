# 이진 탐색  (code)  [replay/self-gpt]

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

## ⚖️ 심판 (GPT_5_2)
WINNER: A  
REASON: 요구사항인 “코드만, 시간복잡도 한 줄”을 A는 코드 블록 내에 시간복잡도 한 줄까지 포함해 정확히 충족하지만, B는 코드 외부에 마크다운 텍스트로 시간복잡도를 적어 “코드만” 조건을 위반했다.  
감점 요인: B는 시간복잡도 표기가 코드가 아닌 서술 형식이라 형식 요구 불충족.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
