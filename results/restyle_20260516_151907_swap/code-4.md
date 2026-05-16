# 괄호 검증  (code)

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️  GPT-5.2
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

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (RESTYLED — replay_judge.py 로 채점 필요)
(아직 심판 호출 전. 이 디렉토리에 replay_judge.py --from-battle 이 디렉토리 ... 실행)
