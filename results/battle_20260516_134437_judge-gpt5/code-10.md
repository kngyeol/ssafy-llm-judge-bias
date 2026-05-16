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

## ⚖️  심판 (GPT_5)
WINNER: TIE
REASON: 두 쿼리 모두 Users 기준 LEFT JOIN과 COALESCE(SUM)으로 주문 없는 사용자까지 0 합계를 포함해 요구사항을 정확히 충족하며 기능적으로 동일함; 감점 요인 없음.
