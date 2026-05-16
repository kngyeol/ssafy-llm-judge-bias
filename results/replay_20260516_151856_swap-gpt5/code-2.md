# 디버깅  (code)  [replay/swap-gpt5]

**문제**
> 다음 Python 코드의 버그를 찾고 1줄로 설명한 뒤 고친 코드를 보여라:

def find_max(nums):
    max_val = 0
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val

## 🅰️ (shown as A, originally B (Claude-Opus))
## 버그 설명
`max_val`을 0으로 초기화하면 모든 요소가 음수인 리스트에서 잘못된 결과(0)를 반환한다.

## 고친 코드
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
# 원본 코드: find_max([-5, -3, -1]) → 0 (잘못됨)
# 수정 코드: find_max([-5, -3, -1]) → -1 (정상)
```

## 🅱️ (shown as B, originally A (GPT-5.2))
버그(1줄 설명): `max_val`을 0으로 시작해서 입력이 모두 음수이거나 빈 리스트일 때 잘못된 결과(0 반환/의미 없는 값)를 낸다.

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

## ⚖️ 심판 (GPT_5)
WINNER: B
REASON: B는 음수만 있는 경우를 고치면서 빈 리스트도 예외로 안전하게 처리한 반면 A는 빈 리스트에서 -inf를 반환하는 문제가 남는다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
