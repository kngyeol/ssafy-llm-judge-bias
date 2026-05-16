# SQL 조인 집계  (code)  [replay/stylometric-claude]

**문제**
> Orders(id, user_id, amount), Users(id, name) 두 테이블에서 사용자별 총 주문 금액을 구하되, 주문이 한 건도 없는 사용자도 0으로 포함하는 SQL 쿼리를 작성하라. 쿼리만.

## 🅰️ (shown as A, originally A (GPT-5.2))
```sql
SELECT
    u.id,
    u.name,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM Users u
LEFT JOIN Orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```sql
SELECT
  u.id,
  u.name,
  COALESCE(SUM(o.amount), 0) AS total_amount
FROM Users AS u
LEFT JOIN Orders AS o
  ON o.user_id = u.id
GROUP BY
  u.id,
  u.name;
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 쿼리는 본질적으로 동일하며, 모두 LEFT JOIN과 COALESCE를 사용해 주문 없는 사용자를 0으로 포함하는 요구사항을 정확히 충족한다. B의 AS 키워드와 줄바꿈 스타일은 가독성 선호도일 뿐 기능상 차이가 없다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
