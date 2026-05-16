# 괄호 검증  (code)  [replay/swap-claude]

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️ (shown as A, originally B (Claude-Opus))
```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    
    return len(stack) == 0
```

## 🅱️ (shown as B, originally A (GPT-5.2))
```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            return False
    return not stack
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 스택 기반으로 괄호 검증을 정확히 구현했으며 핵심 로직이 동일하다. A는 `stack[-1]` 확인 후 `pop()`, B는 `pop()` 직접 사용으로 미세하게 간결하나, B의 `else: return False`는 괄호 외 문자를 거부하는 추가 검증(문제에서 명시 안 됨)이므로 장단점이 상쇄되어 실질적 차이 없음.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
