# 디버깅  (code)  [replay/stylometric-gemini]

**문제**
> 다음 Python 코드의 버그를 찾고 1줄로 설명한 뒤 고친 코드를 보여라:

def find_max(nums):
    max_val = 0
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val

## 🅰️ (shown as A, originally A (GPT-5.2))
**버그:** `max_val = 0`으로 초기화하면 모든 원소가 음수일 때 실제 최댓값이 아닌 0을 반환하고, 빈 리스트일 때도 의미 없는 0이 나온다.

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

## 🅱️ (shown as B, originally B (Claude-Opus))
## 버그(1줄 설명)
`max_val`을 0으로 시작하면 입력이 전부 음수일 때 최댓값 대신 0을 반환하는 오류가 난다.

## 수정 코드
```python
def find_max(nums):
    max_val = float('-inf')  # 또는 nums[0]
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val
```

## 테스트 비교
```python
# 원본 코드: find_max([-5, -3, -1]) → 0 (오류)
# 수정 코드: find_max([-5, -3, -1]) → -1 (정상)
```

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: B
REASON: B는 버그를 '1줄'로 정확히 설명했고, 핵심 버그를 고치는 코드와 함께 유용한 테스트 비교를 제공했습니다. A의 설명은 1줄 요구사항을 약간 벗어났습니다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **B** 손이 올라감.
