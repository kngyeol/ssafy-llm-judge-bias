# 정규식 한국 휴대폰  (code)

**문제**
> 한국 휴대폰 번호를 매칭하는 Python 정규식을 작성하라. 형식: 010-XXXX-XXXX 또는 010XXXXXXXX (X는 숫자, 하이픈은 있어도 되고 없어도 됨, 010만 허용). 정규식 패턴 한 줄과 re.fullmatch 예시 한 줄.

## 🅰️  GPT-5.2
```python
pattern = r"^010-?\d{4}-?\d{4}$"
```

```python
import re; print(bool(re.fullmatch(pattern, "010-1234-5678")), bool(re.fullmatch(pattern, "01012345678")))
```

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (GPT_5)
WINNER: A
REASON: A는 패턴 한 줄과 re.fullmatch 예시 한 줄로 요구를 충족하며 두 형식을 매칭한다; B는 예시가 여러 줄이고 불필요한 내용이 많으며 혼합 하이픈을 명시적으로 허용해 스펙에서 벗어난다(둘 다 혼합 하이픈 허용은 감점).
