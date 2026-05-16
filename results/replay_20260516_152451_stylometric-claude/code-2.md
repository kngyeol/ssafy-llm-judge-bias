# 디버깅  (code)  [replay/stylometric-claude]

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

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: 두 답변 모두 핵심 버그(0 초기화 시 음수 배열 오류)를 정확히 지적했으나, A는 빈 리스트 예외처리까지 포함해 더 robust한 해결책을 제시했고, B의 `float('-inf')` 방식은 빈 리스트에서 `-inf`를 반환하는 새로운 논리적 오류를 만들어낸다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
