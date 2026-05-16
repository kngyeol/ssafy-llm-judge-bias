# 딕셔너리 정렬  (code)  [replay/swap-claude]

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️ (shown as A, originally B (Claude-Opus))
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️ (shown as B, originally A (GPT-5.2))
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: TIE
REASON: 두 답변이 완전히 동일한 코드를 제시했으며, 값 기준 내림차순 정렬 요구사항을 정확히 충족하는 올바른 한 줄 코드다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
