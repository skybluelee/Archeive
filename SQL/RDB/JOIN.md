# 조건 추가
```
SELECT	*
FROM	  offices O 
  	    JOIN employees USING (officeCode)
        LEFT JOIN customers ON employeeId = salesRepId
      	LEFT JOIN orders ON (customers.customerId = orders.customerId AND YEAR(orderDate) = 2004);
```
FROM JOIN 내부에 조건을 추가하여 쿼리 실행 시간 단축 가능.
