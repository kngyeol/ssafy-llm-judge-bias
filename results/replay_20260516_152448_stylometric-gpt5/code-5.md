# SQL 두 번째 높은 급여  (code)  [replay/stylometric-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: TIE
REASON: 두 쿼리 모두 중복을 제거한 두 번째 높은 급여를 정확히 반환하고 없으면 NULL을 반환한다; 다만 A는 LIMIT/OFFSET 등 특정 DB 방언 의존성이 있고, B는 보다 표준적이나 MAX 서브쿼리로 테이블을 두 번 스캔하는 점이 감점 요인이다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
