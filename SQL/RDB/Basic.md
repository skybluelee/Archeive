# JOIN에 조건 추가
```
SELECT	*
FROM	  offices O 
  	    JOIN employees USING (officeCode)
        LEFT JOIN customers ON employeeId = salesRepId
      	LEFT JOIN orders ON (customers.customerId = orders.customerId AND YEAR(orderDate) = 2004);
```
FROM JOIN 내부에 조건을 추가하여 쿼리 실행 시간 단축 가능.
# WHERE
비교 연산자: `>, >=, <, <=, =, <>`
SQL 연산자: `BETWEEN a AND b, NOT BETWEEN a AND b, IN, NOT IN, LIKE, NOT LIKE, IS NULL, IS NOT NULL`
논리 연산자: `AND, OR, NOT`
## LIKE
LIKE은 문자열 내에 pattern과 일치하는 부분 문자열(Substring)이 있는지 검사한다.
