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

## ⚖️  심판 (GPT_5)
WINNER: TIE
REASON: 두 답변 모두 동일한 한 줄짜리 리스트 컴프리헨션으로 정답을 정확히 제시했으며 감점 요인 없음.
