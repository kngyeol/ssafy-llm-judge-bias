# 딕셔너리 정렬  (code)

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️  GPT-5.2
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️  Claude-Opus-4.5
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## ⚖️  심판 (GPT_5)
WINNER: TIE
REASON: 두 답변이 동일한 한 줄 코드로 값 기준 내림차순 정렬된 새 딕셔너리를 정확히 반환하므로 무승부; 둘 다 코드블록 사용은 '코드만' 요구와 약간 어긋남.
