# SQL 두 번째 높은 급여  (code)

**문제**
> Employee(id INT, salary INT) 테이블에서 두 번째로 높은 급여를 구하는 SQL 쿼리를 작성하라. 같은 급여가 여러 명일 경우 중복은 1번만 센다. 없으면 NULL 반환. 쿼리만.

## 🅰️  GPT-5.2
```sql
SELECT (
  SELECT DISTINCT salary
  FROM Employee
  ORDER BY salary DESC
  LIMIT 1 OFFSET 1
) AS SecondHighestSalary;
```

## 🅱️  Claude-Opus-4.5
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

## ⚖️  심판 (CLAUDE_SONNET_4_5)
WINNER: A

REASON: A는 DISTINCT와 OFFSET을 사용해 두 번째로 높은 급여를 정확히 찾고, 서브쿼리로 감싸 존재하지 않을 때 NULL을 올바르게 반환한다. B는 두 번째로 높은 급여를 찾지만, 급여가 1개뿐일 때 그 값을 반환하는 오류가 있으며(NULL이어야 함), 로직상 "최고 급여 미만의 최댓값"은 정확하나 엣지케이스 처리가 미흡하다.
