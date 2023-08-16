# JOIN에 조건 추가
```
SELECT	*
FROM	offices O 
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
## 집계 함수
집계 함수는 WHERE 내부에서 사용 불가능
# 집계 함수
`COUNT, SUM, AVG, MIN, MAX, STDDEV, VARIAN, GROUP_CONCAT`
`STDDEV`는 표준편차, `VARIAN`은 분산, `GROUP_CONCAT`은 NULL 값을 제외한 모든 컬럼 값을 `,`로 연결한 문자열 생성
## GROUP_CONCAT
``` 
SELECT  GROUP_CONCAT(city) AS cities
FROM    s_offices;

+------------------------------+
|                        cities|
+------------------------------+
|San Francisco,Boston,NYC,Paris|
+------------------------------+
```
```
SELECT  GROUP_CONCAT(city ORDER BY city ASC SEPARATOR ', ') AS cities
FROM    s_offices;

+---------------------------------+
|                           cities|
+---------------------------------+
|Boston, NYC, Paris, San Francisco|
+---------------------------------+
```
