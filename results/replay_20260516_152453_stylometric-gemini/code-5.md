# SQL 두 번째 높은 급여  (code)  [replay/stylometric-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: A
REASON: 두 쿼리 모두 올바르게 작동하지만, A는 `DISTINCT`, `ORDER BY`, `LIMIT`, `OFFSET`을 사용하여 두 번째로 높은 유일한 값을 찾는 문제에 더 직접적이고 명시적인 해결책을 제시합니다.

**해석**: 심판이 A를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
