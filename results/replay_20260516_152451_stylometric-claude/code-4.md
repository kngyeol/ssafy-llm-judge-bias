# 괄호 검증  (code)  [replay/stylometric-claude]

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            return False
    
    return len(stack) == 0
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
def is_valid(s):
    stack = []
    match = {')': '(', ']': '[', '}': '{'}

    for ch in s:
        if ch in match.values():
            stack.append(ch)
        elif ch in match:
            if not stack or stack.pop() != match[ch]:
                return False

    return not stack
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: B

REASON: B가 더 우수함. A는 괄호가 아닌 문자('a', '1' 등)가 입력되면 즉시 False를 반환하여 "()a[]" 같은 케이스를 잘못 처리함. B는 괄호만 검사하고 나머지는 무시하여 더 robust하며, `return not stack`이 `return len(stack) == 0`보다 pythonic함.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **B** 손이 올라감.
