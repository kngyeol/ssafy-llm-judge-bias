# 딕셔너리 정렬  (code)

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️  GPT-5.2
```python
sorted_d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️  Claude-Opus-4.5
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: B
REASON: B는 요청된 새 딕셔너리를 직접 생성하고 표현식으로 반환하므로 "반환하는 한 줄 코드" 요구사항에 더 정확하게 부합합니다. A는 딕셔너리를 변수에 할당하는 추가적인 단계를 포함합니다.
