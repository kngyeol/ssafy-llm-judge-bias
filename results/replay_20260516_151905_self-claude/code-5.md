# SQL 두 번째 높은 급여  (code)  [replay/self-claude]

**문제**
> Employee(id INT, salary INT) 테이블에서 두 번째로 높은 급여를 구하는 SQL 쿼리를 작성하라. 같은 급여가 여러 명일 경우 중복은 1번만 센다. 없으면 NULL 반환. 쿼리만.

## 🅰️ (shown as A, originally A (GPT-5.2))
```sql
SELECT (
  SELECT DISTINCT salary
  FROM Employee
  ORDER BY salary DESC
  LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

## 🅱️ (shown as B, originally B (Claude-Opus))
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

## ⚖️ 심판 (CLAUDE_OPUS_4_5_20251101)
**WINNER: TIE**

**REASON:** 두 쿼리 모두 정확히 동작함 - A는 DISTINCT + OFFSET으로, B는 서브쿼리 MAX로 두 번째 높은 급여를 구하며, 둘 다 해당 값이 없으면 NULL을 반환하고 중복도 올바르게 처리함.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
