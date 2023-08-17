# CTE
CTE(Common Table Expression): 질의 내에서 이름을 갖는 중간 결과를 임시로 생성
- WITH 절을 사용하여 중간 결과를 메모리에 임시 저장하고 이름을 부여
- 질의 내에서 중간 결과는 디스크에 저장된 테이블과 동일하게 다룸
- 질의 실행이 종료되면 중간 결과는 제거
- CTAS(Create Table AS)는 스키마에 테이블을 생성하고 데이터를 디스크에 저장하나 CTE는 스키마에 테이블 생성하지 않고 데이터를 디스크에 저장하지 않음
## 단일 CTE
```
WITH temp AS
(
    SELECT customerId, name 고객, salesRepId, COUNT(*) 결재횟수
    FROM customers LEFT JOIN payments USING (customerId)
    GROUP BY customerId
)
SELECT customerId, 고객, 결재횟수, CONCAT(firstName, ' ', lastName) 담당직원
FROM   temp
       LEFT JOIN employees ON temp.salesRepId = employees.employeeId;
```
## 다중 CTE
```
WITH orderTotal AS
(
    SELECT customerId, name, SUM(quantity * priceEach) AS total
    FROM customers
    JOIN orders USING (customerId)
    JOIN orderDetails USING (orderNo)
GROUP BY customerId
),
paymentTotal AS
(
    SELECT customerId, name, SUM(amount) AS total
    FROM customers JOIN payments USING (customerId)
    GROUP BY customerId
)
SELECT O.customerId, O.name, O.total AS 주문액, P.total AS 결재액
FROM   orderTotal O JOIN paymentTotal P USING (customerId)
WHERE  O.total > P.total
ORDER  BY O.customerId;
```
WITH를 한번만 사용함
## 재귀 CTE
주어진 한 개의 초기행을 이용해 연속해서 다음 행을 생성
```
WITH RECURSIVE cte_name [(column_list)] AS
(
    SELECT 문 /* non-recursive SELECT: return initial row */
    UNION ALL
    SELECT 문 /* recursive SELECT: return additional row set */
)
SELECT ...
```
두번째 SELECT 문의 WHERE 절에서 재귀 호출의 종료 조건을 서술함. 이때 조건이 없다면 DBMS에서 내부적으로 정의한 최대치까지 실행
```
WITH RECURSIVE temp AS
(
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM temp WHERE n < 5 /* 재귀 호출의 종료 조건 */
)
SELECT *
FROM temp;

+-+
|n|
+-+
|1|
|2|
|3|
|4|
|5|
+-+
```
```
WITH RECURSIVE allDates (date) AS
(
    SELECT '2003-11-01'
    UNION ALL
    SELECT date + INTERVAL 1 DAY
    FROM allDates
    WHERE date + INTERVAL 1 DAY <= '2003-11-30'
)
SELECT *
FROM allDates;

+----------+
|      date|
+----------+
|2003-11-01|
|2003-11-02|
|    ...   |
|2003-11-30|
+----------+
```
### 재귀 CTE 관련 설정
시스템 변수를 사용해 실행의 최대치 제어
- cte_max_recursion_depth: 디폴트는 1000회
- max_execution_time: 디폴트는 1초
# Pivot
원시 데이터 테이블의 행을 통계 요약 테이블의 셀로 변환
- 가로축: CASE 표현식을 사용하여 피벗 컬럼에 있는 유일한 값의 개수만큼 컬럼 생성
- 세로축: GROUP BY 기준 컬럼에 있는 유일한 값의 개수만큼 행 생성
- 셀: 그룹별로 생성한 컬럼에 집게 함수를 적용하여 원하는 통계치 계산
## step
```
SELECT  country, orderDate, priceEach, quantity, priceEach * quantity
FROM    s_customers C
        JOIN s_orders D USING(customerId)
        JOIN s_orderdetails O USING(orderNo)
WHERE   YEAR(orderDate) = 2004
ORDER   BY country;

+---------+-------------------+---------+--------+--------------------+
|  country|          orderDate|priceEach|quantity|priceEach * quantity|
+---------+-------------------+---------+--------+--------------------+
|Australia|2004-02-20 00:00:00|    80.39|      37|             2974.43|
|Australia|2004-02-20 00:00:00|   110.61|      47|             5198.67|
|...                                                                  |
|      USA|2004-12-10 00:00:00|   105.34|      28|             2949.52|
+---------+-------------------+---------+--------+--------------------+
```
1. pivot시킬 원시 데이터 테이블 생성
```
SELECT  country,
        CASE MONTH(orderDate) WHEN 1 THEN priceEach*quantity END AS Jan,
        CASE MONTH(orderDate) WHEN 2 THEN priceEach*quantity END AS Feb,
        CASE MONTH(orderDate) WHEN 3 THEN priceEach*quantity END AS Mar,
        CASE MONTH(orderDate) WHEN 4 THEN priceEach*quantity END AS Apr,
        CASE MONTH(orderDate) WHEN 5 THEN priceEach*quantity END AS May,
        CASE MONTH(orderDate) WHEN 6 THEN priceEach*quantity END AS Jun,
        CASE MONTH(orderDate) WHEN 7 THEN priceEach*quantity END AS Jul,
        CASE MONTH(orderDate) WHEN 8 THEN priceEach*quantity END AS Aug,
        CASE MONTH(orderDate) WHEN 9 THEN priceEach*quantity END AS Sep,
        CASE MONTH(orderDate) WHEN 10 THEN priceEach*quantity END AS Oct,
        CASE MONTH(orderDate) WHEN 11 THEN priceEach*quantity END AS Nov,
        CASE MONTH(orderDate) WHEN 12 THEN priceEach*quantity END AS Dec
FROM    s_customers C
        JOIN s_orders D USING(customerId)
        JOIN s_orderdetails O USING(orderNo)
WHERE   YEAR(orderDate) = 2004
ORDER   BY country;

+---------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|  country|    Jan|    Feb|    Mar|    Apr|    May|    Jun|    Jul|    Aug|    Sep|    Oct|    Nov|    Dec|
+---------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|Australia| 0|2974.43|      0|      0|      0|      0|      0|      0|      0|      0|      0|      0|
|Australia|	0|5198.67|      0|      0|      0|      0|      0|      0|      0|      0|      0|      0|
|...                                                                                                      |
|      USA|	     0|5198.67|      0|      0|      0|      0|      0|      0|      0|      0|      0|2949.52|
+---------+------+------+------+------+------+------+------+------+------+------+------+------+-----------+
```
2. 피벗 컬럼을 pivot시킴
```
SELECT country,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 1 THEN priceEach*quantity END)),0) Jan,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 2 THEN priceEach*quantity END)),0) Feb,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 3 THEN priceEach*quantity END)),0) Mar,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 4 THEN priceEach*quantity END)),0) Apr,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 5 THEN priceEach*quantity END)),0) May,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 6 THEN priceEach*quantity END)),0) Jun,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 7 THEN priceEach*quantity END)),0) Jul,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 8 THEN priceEach*quantity END)),0) Aug,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 9 THEN priceEach*quantity END)),0) Sep,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 10 THEN priceEach*quantity END)),0) Oct,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 11 THEN priceEach*quantity END)),0) Nov,
       COALESCE(FLOOR(SUM(CASE MONTH(orderDate) WHEN 12 THEN priceEach*quantity END)),0) Dec,
       COALESCE(FLOOR(SUM(priceEach*quantity)),0) total_price
FROM   s_customers C
       JOIN s_orders D USING(customerId)
       JOIN s_orderdetails O USING(orderNo)
WHERE  YEAR(orderDate) = 2004
GROUP  BY country
ORDER  BY country;

+---------+------+------+------+------+------+------+------+------+------+------+------+------+-----------+
|  country|   Jan|   Feb|   Mar|   Apr|   May|   Jun|   Jul|   Aug|   Sep|   Oct|   Nov|   Dec|total_price|
+---------+------+------+------+------+------+------+------+------+------+------+------+------+-----------+
|Australia|0| 44894|     0|     0|     0|     0| 45221|     0|     0|     0| 82261| 31835|     204213|
|  Austria|0|     0|     0|     0|     0|     0|  6419|     0|     0|     0| 42931| 31835|      49233|
|...                                                                                                      |
|      USA| 57124| 92948| 70903| 36458|159429| 77271| 93991|215256| 60664|168723|377124|116603|    1526499|
+---------+------+------+------+------+------+------+------+------+------+------+------+------+-----------+
```
3. 집계 함수로 통계치 생성
