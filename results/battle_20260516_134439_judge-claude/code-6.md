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
print(re.fullmatch(pattern, "010-1234-5678"))  # ✓ Match
print(re.fullmatch(pattern, "01012345678"))    # ✓ Match
print(re.fullmatch(pattern, "0101234-5678"))   # ✓ Match (하이픈 혼합도 허용)
print(re.fullmatch(pattern, "011-1234-5678"))  # ✗ None (010만 허용)
print(re.fullmatch(pattern, "010-123-4567"))   # ✗ None (자릿수 불일치)
```

## 패턴 설명

| 요소 | 의미 |
|------|------|
| `010` | 리터럴 "010" |
| `-?` | 하이픈 0개 또는 1개 |
| `\d{4}` | 숫자 4자리 |

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 답변 모두 동일하게 작동하는 정규식 패턴(`010-?\d{4}-?\d{4}`)을 제시하고 re.fullmatch 예시를 포함했다. A는 간결하고, B는 추가 테스트 케이스와 설명을 제공하지만, 문제는 "패턴 한 줄과 예시 한 줄"만 요구했으므로 핵심 요구사항 충족도는 동일하다. 다만 B의 패턴은 `^`, `$` 앵커가 없는데 fullmatch는 자동으로 전체 매칭하므로 실제로는 문제없으나, A가 명시적으로 앵커를 포함한 점은 정규식 이해도 측면에서 미세하게 우수하나 fullmatch 컨텍스트에서는 불필요하므로 실질적 차이 없음.
