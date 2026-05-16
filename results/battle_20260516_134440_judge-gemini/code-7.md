# 리팩토링  (code)

**문제**
> 다음 Python 코드를 한 줄짜리 리스트 컴프리헨션으로 리팩토링하라. 결과 코드만:

result = []
for x in range(20):
    if x % 2 == 0:
        result.append(x * x)

## 🅰️  GPT-5.2
```python
result = [x * x for x in range(20) if x % 2 == 0]
```

## 🅱️  Claude-Opus-4.5
```python
result = [x * x for x in range(20) if x % 2 == 0]
```

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: TIE
REASON: 두 답변 모두 주어진 Python 코드를 한 줄짜리 리스트 컴프리헨션으로 완벽하게 리팩토링했습니다.
