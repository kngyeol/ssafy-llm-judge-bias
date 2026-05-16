# SQL 두 번째 높은 급여  (code)  [replay/swap-gemini]

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

## ⚖️ 심판 (GEMINI_2_5_FLASH)
WINNER: B
REASON: 두 쿼리 모두 올바르게 작동하지만, B는 `DISTINCT` 키워드와 `LIMIT 1 OFFSET 1`을 사용하여 "중복은 1번만 센다" 및 "두 번째로 높은" 이라는 요구사항을 더 명시적이고 직관적으로 해결합니다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **A** 손이 올라감.
