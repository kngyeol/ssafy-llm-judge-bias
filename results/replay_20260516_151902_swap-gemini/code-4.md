# 괄호 검증  (code)  [replay/swap-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: B
REASON: B는 괄호 이외의 문자가 입력된 경우를 처리하여 더 견고하며, 타입 힌트를 포함하여 가독성이 좋다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
