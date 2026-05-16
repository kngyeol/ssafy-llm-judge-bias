# 괄호 검증  (code)

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️  GPT-5.2
```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            return False
    return not stack
```

## 🅱️  Claude-Opus-4.5
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        elif char in '([{':
            stack.append(char)
    
    return len(stack) == 0
```

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: A는 문자열 내 괄호가 아닌 다른 문자가 포함될 경우를 명확하게 처리하여 False를 반환하는 반면, B는 이를 묵묵히 무시한다. 또한 A는 타입 힌트를 사용하여 코드 가독성과 유지보수성을 높였다.
