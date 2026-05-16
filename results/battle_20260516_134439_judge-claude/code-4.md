# 괄호 검증  (code)

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️  GPT-5.2
```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opens = set(pairs.values())

    for ch in s:
        if ch in opens:
            stack.append(ch)
        elif ch in pairs:
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

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: B

REASON: A는 괄호가 아닌 문자(예: 'a', '1')가 입력되면 즉시 False를 반환하여 문제 요구사항(괄호 문자열 검증)을 벗어난 과도한 제약을 추가했다. B는 괄호만 처리하고 다른 문자는 무시하는 더 유연하고 일반적인 구현이며, 핵심 로직도 간결하다.
