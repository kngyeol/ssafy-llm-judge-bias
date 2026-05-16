# 정규식 한국 휴대폰  (code)  [replay/stylometric-claude]

**문제**
> 한국 휴대폰 번호를 매칭하는 Python 정규식을 작성하라. 형식: 010-XXXX-XXXX 또는 010XXXXXXXX (X는 숫자, 하이픈은 있어도 되고 없어도 됨, 010만 허용). 정규식 패턴 한 줄과 re.fullmatch 예시 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
pattern = r"^010-?\d{4}-?\d{4}$"
```

```python
import re
print(re.fullmatch(pattern, "010-1234-5678"))  # Match
print(re.fullmatch(pattern, "01012345678"))    # Match
```

## 🅱️ (shown as B, originally B (Claude-Opus))
# 한국 휴대폰 번호 정규식

## 정규식 패턴

```python
pattern = r"010-?\d{4}-?\d{4}"
```

## re.fullmatch 예시

```python
import re

pattern = r"010-?\d{4}-?\d{4}"

# 테스트
print(re.fullmatch(pattern, "010-1234-5678"))  # ✅ Match
print(re.fullmatch(pattern, "01012345678"))    # ✅ Match
print(re.fullmatch(pattern, "0101234-5678"))   # ✅ Match (혼합도 허용)
print(re.fullmatch(pattern, "011-1234-5678"))  # ❌ None (011 불가)
print(re.fullmatch(pattern, "010-123-5678"))   # ❌ None (3자리 불가)
```

## 패턴 설명

| 부분 | 의미 |
|------|------|
| `010` | 010 고정 |
| `-?` | 하이픈 0개 또는 1개 |
| `\d{4}` | 숫자 4자리 |
| `-?` | 하이픈 0개 또는 1개 |
| `\d{4}` | 숫자 4자리 |

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: 두 답변 모두 정확한 정규식을 제공하지만, A는 `^`와 `$` 앵커를 포함하여 fullmatch와의 중복을 보여주는 교육적 가치가 있고, 문제가 요구한 "정규식 패턴 한 줄과 re.fullmatch 예시 한 줄"을 정확히 충족한다. B는 과도한 설명과 테스트 케이스로 간결성 요구사항을 벗어났으며, `0101234-5678` 같은 혼합 형식을 허용한다고 표시했으나 이는 일반적으로 유효하지 않은 형식으로 오해의 소지가 있다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
