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

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (GPT_5)
WINNER: A
REASON: A는 음수와 빈 리스트 모두를 정확히 처리(첫 원소로 초기화, 빈 입력 예외)했으며 요구사항 충족; B는 빈 리스트에서 -inf를 반환하도록 수정해 동작이 모호함(감점).
