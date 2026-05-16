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

## ⚖️  심판 (GPT_5)
WINNER: B
REASON: 둘 다 요구사항을 충족하지만 B는 표준 SQL로 이식성이 높고, A는 LIMIT/OFFSET 방언 의존으로 감점.
