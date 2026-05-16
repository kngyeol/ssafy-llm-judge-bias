# 딕셔너리 정렬  (code)  [replay/stylometric-claude]

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```python
{ k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True) }
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 값 기준 내림차순 정렬을 올바르게 구현한 한 줄 코드이며, A는 dict() 생성자, B는 딕셔너리 컴프리헨션을 사용했으나 기능적으로 동일하고 모두 정답이다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
