# SQL 두 번째 높은 급여  (code)  [replay/swap-gpt5]

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

## ⚖️ 심판 (GPT_5)
WINNER: TIE
REASON: 두 쿼리 모두 중복을 하나로 보고 두 번째로 높은 급여를 정확히 반환하며 없을 경우 NULL을 돌려준다; 다만 B는 LIMIT/OFFSET에 의존한 비표준 문법이라 이식성 측면에서 감점 요인이 있다.

**해석**: 심판이 TIE를 골랐고, 원본 라벨 기준 **TIE** 손이 올라감.
