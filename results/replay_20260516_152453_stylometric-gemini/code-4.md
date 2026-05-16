# 괄호 검증  (code)  [replay/stylometric-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: A는 타입 힌트를 제공하며, 괄호가 아닌 문자가 포함된 경우를 명확하게 `False`로 처리하여 문제의 일반적인 해석에 더 부합한다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
