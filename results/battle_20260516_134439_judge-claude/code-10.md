# SQL 조인 집계  (code)

**문제**
> Orders(id, user_id, amount), Users(id, name) 두 테이블에서 사용자별 총 주문 금액을 구하되, 주문이 한 건도 없는 사용자도 0으로 포함하는 SQL 쿼리를 작성하라. 쿼리만.

## 🅰️  GPT-5.2
```sql
SELECT
  u.id,
  u.name,
  COALESCE(SUM(o.amount), 0) AS total_amount
FROM Users u
LEFT JOIN Orders o
  ON o.user_id = u.id
GROUP BY u.id, u.name;
```

## 🅱️  Claude-Opus-4.5
```sql
SELECT u.id, u.name, COALESCE(SUM(o.amount), 0) AS total_amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: TIE

REASON: 두 쿼리 모두 LEFT JOIN으로 주문 없는 사용자를 포함하고, COALESCE로 NULL을 0 처리하며, GROUP BY로 사용자별 집계를 정확히 수행한다. JOIN 조건 순서(o.user_id = u.id vs u.id = o.user_id)와 포매팅 차이만 있을 뿐 기능적으로 완전히 동일하다.
