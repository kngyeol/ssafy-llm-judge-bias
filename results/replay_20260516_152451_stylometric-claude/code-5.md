# SQL 두 번째 높은 급여  (code)  [replay/stylometric-claude]

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

## ⚖️ 심판 (CLAUDE_SONNET_4_5)
WINNER: B

REASON: 두 쿼리 모두 작동하지만, B가 더 우수하다. A는 OFFSET을 사용하여 두 번째 값을 가져오는데, 데이터가 1개만 있을 경우 NULL을 올바르게 반환하지만, B는 MAX 함수를 사용하여 최댓값보다 작은 값 중 최댓값을 구하는 더 직관적이고 표준적인 접근법이다. B는 서브쿼리가 명확하고, 두 번째 높은 급여가 없을 때도 자동으로 NULL을 반환하며, DISTINCT나 OFFSET 같은 추가 절이 필요 없어 더 효율적이다.

**해석**: 심판이 B를 골랐고, 원본 라벨 기준 **B** 손이 올라감.
