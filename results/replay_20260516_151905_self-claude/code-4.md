# 괄호 검증  (code)  [replay/self-claude]

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

## ⚖️ 심판 (CLAUDE_OPUS_4_5_20251101)
WINNER: A
REASON: 두 답변 모두 정확하고 올바르게 동작하나, A는 괄호 문자가 아닌 입력에 대해 False를 반환하여 더 엄격한 검증을 수행하고, `stack.pop() != pairs[ch]`로 pop과 비교를 한 번에 처리하여 더 간결하며, 타입 힌트도 포함되어 있어 코드 품질이 약간 더 우수함.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
