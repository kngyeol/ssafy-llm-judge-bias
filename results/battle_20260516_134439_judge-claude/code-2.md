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
버그(1줄 설명): `max_val`을 0으로 초기화해서 입력이 모두 음수이거나 빈 리스트일 때 잘못된 결과(또는 예외 미처리)가 난다.

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
`max_val`을 0으로 초기화하면 **모든 요소가 음수인 리스트에서 실제 최댓값 대신 0을 반환**하는 오류가 발생한다.

---

## 고친 코드

```python
def find_max(nums):
    max_val = float('-inf')  # 또는 nums[0]으로 초기화
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val
```

---

## 테스트 비교

| 입력 | 기존 코드 | 수정 코드 |
|------|----------|----------|
| `[-5, -2, -8]` | `0` ❌ | `-2` ✅ |
| `[3, 1, 4]` | `4` ✅ | `4` ✅ |

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: B는 `float('-inf')` 초기화로 음수 문제는 해결했으나 **빈 리스트 입력 시 `-inf`를 반환하는 치명적 결함**이 남아있고, A는 빈 리스트 예외 처리까지 완벽히 구현했다. 문제는 "버그를 찾고 고쳐라"인데 A만이 모든 엣지 케이스를 처리했으며, B의 표 장식은 핵심 결함을 가리는 감점 요소다.
