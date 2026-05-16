# 괄호 검증  (code)  [replay/self-gpt]

**문제**
> Python으로 '()[]{}' 같은 문자열의 괄호가 올바르게 짝지어지고 닫혔는지 검사하는 함수 is_valid(s)를 작성하라. 코드만, 설명 금지.

## 🅰️ (shown as A, originally A (GPT-5.2))
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

## 🅱️ (shown as B, originally B (Claude-Opus))
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

## ⚖️ 심판 (GPT_5_2)
WINNER: A
REASON: A는 괄호 이외의 문자가 들어오면 즉시 False를 반환해 입력 검증까지 확실히 하며, 스택 pop을 한 번에 처리해 간결하다; B는 괄호 이외 문자를 무시해 잘못된 입력도 True가 될 수 있는 감점 요인이 있다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
