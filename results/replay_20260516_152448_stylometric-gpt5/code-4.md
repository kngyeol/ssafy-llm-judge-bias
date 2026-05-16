# 괄호 검증  (code)  [replay/stylometric-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: A
REASON: 둘 다 괄호만인 입력에서는 정답이나 A는 비괄호 문자를 False로 처리해 안전한 반면, B는 비괄호 문자를 무시해 'abc'도 True로 되는 감점 요인이 있음.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
