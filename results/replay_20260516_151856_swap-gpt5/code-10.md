# SQL 조인 집계  (code)  [replay/swap-gpt5]

**문제**
> Orders(id, user_id, amount), Users(id, name) 두 테이블에서 사용자별 총 주문 금액을 구하되, 주문이 한 건도 없는 사용자도 0으로 포함하는 SQL 쿼리를 작성하라. 쿼리만.

## 🅰️ (shown as A, originally B (Claude-Opus))
```sql
SELECT u.id, u.name, COALESCE(SUM(o.amount), 0) AS total_amount
FROM Users u
LEFT JOIN Orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

## 🅱️ (shown as B, originally A (GPT-5.2))
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

## ⚖️ 심판 (GPT_5)
WINNER: TIE
REASON: 두 쿼리 모두 LEFT JOIN과 COALESCE로 주문 없는 사용자까지 0으로 집계하며, GROUP BY도 적절해 기능적으로 동일하고 차이는 서식뿐이다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
