# 딕셔너리 정렬  (code)  [replay/self-gpt]

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## ⚖️ 심판 (GPT_5_2)
WINNER: TIE
REASON: 두 답변 모두 값(x[1]) 기준 내림차순으로 정렬한 뒤 dict로 변환하는 정확한 한 줄 코드이며 요구사항을 동일하게 충족한다; 감점 요인 없음.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
