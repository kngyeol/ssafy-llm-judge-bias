# 정규식 한국 휴대폰  (code)  [replay/self-gpt]

**문제**
> 한국 휴대폰 번호를 매칭하는 Python 정규식을 작성하라. 형식: 010-XXXX-XXXX 또는 010XXXXXXXX (X는 숫자, 하이픈은 있어도 되고 없어도 됨, 010만 허용). 정규식 패턴 한 줄과 re.fullmatch 예시 한 줄.

## 🅰️ (shown as A, originally A (GPT-5.2))
```python
pattern = r"^010-?\d{4}-?\d{4}$"
```

```python
import re; print(bool(re.fullmatch(pattern, "010-1234-5678")), bool(re.fullmatch(pattern, "01012345678")))
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

## ⚖️ 심판 (GPT_5_2)
WINNER: A  
REASON: A는 `^...$`로 전체 문자열을 엄격히 고정하고 요구된 “패턴 한 줄 + fullmatch 예시 한 줄” 형식을 정확히 만족한다. B는 앵커가 없어(요구가 fullmatch이긴 하지만) 문제의 “한 줄” 요구를 어기고 불필요한 출력/설명을 추가했다는 감점 요인이 있다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
