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
LEFT JOIN Orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

## 🅱️  Claude-Opus-4.5
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

## ⚖️  심판 (RESTYLED — replay_judge.py 로 채점 필요)
(아직 심판 호출 전. 이 디렉토리에 replay_judge.py --from-battle 이 디렉토리 ... 실행)
