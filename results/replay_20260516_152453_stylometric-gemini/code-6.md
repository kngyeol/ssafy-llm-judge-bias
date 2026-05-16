# 정규식 한국 휴대폰  (code)  [replay/stylometric-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: A가 요구사항인 "정규식 패턴 한 줄과 re.fullmatch 예시 한 줄"에 더 가깝게 응답했으며, 정규식에 `^`와 `$` 앵커를 명시하여 더 명확합니다. B는 불필요하게 많은 `re.fullmatch` 예시와 패턴 설명을 추가했습니다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
