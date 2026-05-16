# SQL 두 번째 높은 급여  (code)  [replay/swap-claude]

**문제**
> Employee(id INT, salary INT) 테이블에서 두 번째로 높은 급여를 구하는 SQL 쿼리를 작성하라. 같은 급여가 여러 명일 경우 중복은 1번만 센다. 없으면 NULL 반환. 쿼리만.

## 🅰️ (shown as A, originally B (Claude-Opus))
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

## 🅱️ (shown as B, originally A (GPT-5.2))
```sql
SELECT (
  SELECT DISTINCT salary
  FROM Employee
  ORDER BY salary DESC
  LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: B

REASON: B는 DISTINCT로 중복 급여를 제거하고 OFFSET으로 정확히 두 번째 값을 찾으며, 서브쿼리로 감싸 값이 없을 때 자동으로 NULL을 반환한다. A는 중복 제거 없이 MAX를 사용해 같은 급여가 여러 명일 때도 정상 작동하지만, 두 번째 높은 급여가 없을 경우(직원 1명 또는 모두 같은 급여) NULL 대신 그 급여값을 반환하는 치명적 오류가 있다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
