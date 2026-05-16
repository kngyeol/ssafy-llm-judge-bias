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

## ⚖️  심판 (GEMINI_2.5_FLASH)
WINNER: A
REASON: A는 DISTINCT와 LIMIT/OFFSET을 사용하여 두 번째로 높은 유일한 급여를 정확히 찾고, 해당 급여가 없을 경우 NULL을 반환합니다. B는 두 번째로 높은 유일한 급여가 여러 명일 경우 잘못된 결과를 반환할 수 있습니다.
