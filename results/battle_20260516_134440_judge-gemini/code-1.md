# Two Sum  (code)

**문제**
> Python으로 'Two Sum' 문제를 풀어라. 입력: 정수 배열 nums와 target. 출력: nums[i] + nums[j] == target 인 (i, j) 인덱스. 한 번만 풀고 코드만, 시간복잡도도 함께 한 줄로.

## 🅰️  GPT-5.2
```python
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in seen:
            return (seen[y], i)
        seen[x] = i

# Time Complexity: O(n)
```

## 🅱️  Claude-Opus-4.5
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

**시간복잡도: O(n)**

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: 두 답변 모두 'Two Sum' 문제를 O(n) 시간 복잡도로 정확하게 해결했습니다. A는 시간 복잡도 명시가 코드와 더 자연스럽게 통합되어 있고, 인덱스 반환 시 튜플을 사용하는 것이 일반적인 관례에 더 가깝습니다.
