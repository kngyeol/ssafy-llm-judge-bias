# 디버깅  (code)

**문제**
> 다음 Python 코드의 버그를 찾고 1줄로 설명한 뒤 고친 코드를 보여라:

def find_max(nums):
    max_val = 0
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val

## 🅰️  GPT-5.2
버그: `max_val`을 0으로 고정해 두면 리스트가 전부 음수일 때 결과가 0으로 잘못 나온다.

```python
def find_max(nums):
    if not nums:
        raise ValueError("nums must not be empty")
    max_val = nums[0]
    for n in nums[1:]:
        if n > max_val:
            max_val = n
    return max_val
```

## 🅱️  Claude-Opus-4.5
## 버그 설명
`max_val = 0`으로 초기화하면 모든 요소가 음수인 리스트에서 실제 최댓값이 아닌 0을 반환한다.

## 고친 코드
```python
def find_max(nums):
    max_val = float('-inf')  # 또는 nums[0]
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val
```

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: A는 버그를 정확히 설명하고 `nums[0]`으로 초기화하여 올바르게 수정했으며, 빈 리스트에 대한 예외 처리까지 추가하여 더 견고한 코드를 제공합니다.
