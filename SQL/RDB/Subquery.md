# 제한 사항
- 일반적으로 서브쿼리는 메인쿼리의 컬럼을 참조할 수 있지만, 메인쿼리는 서브쿼리의 컬럼을 참조할 수 없음.
- WHERE 절 서브쿼리에서는 ORDER BY 절을 사용하지 못함.
# 서브쿼리와 조인의 차이
- 조인은 두 테이블의 Cartesian Product의 부분 집합을 리턴함.
- 연관 서브쿼리를 포함한 메인쿼리는 필터링을 통해 메인쿼리 테이블의 부분 집합을 리턴함.
- 따라서 서브쿼리가 조인보다 성능이 좋음
# WHERE 절 서브쿼리
## 비연관 서브쿼리
### 단일값 서브쿼리
```
SELECT
FROM
WHERE  expr 비교연산자 (subquery);
```
`expr`의 실행 결과는 단일값. 서브쿼리도 단일값을 리턴함.
```
SELECT name, MSRP
FROM   s_products
WHERE  MSRP >= (
                  SELECT AVG(MSRP) * 2 -- 서브쿼리 내 결과는 평균값-단일값임
                  FROM products
                )
ORDER BY MSRP; 
```
### 다중값 서브쿼리
```
SELECT
FROM
WHERE  expr 비교연산자 {ANY|SOME|ALL} (subquery);
```
`expr`의 실행 결과는 단일값. 서브쿼리도 단일값의 집합을 리턴함.
- ANY|SOME: 서브쿼리 결과의 어느 한 값과의 비교 결과가 만족하면 true
- ALL: 서브쿼리 결과의 모든 값과의 비교 결과가 만족해야 true
```
SELECT  officeCode, city
FROM    s_offices
WHERE   s_officeCode = ANY (  -- 다중값의 경우 {ANY|SOME|ALL}가 없다면 오류가 발생.
                              SELECT officeCode -- 다중값 리턴  +----------+
                              FROM   s_employees               |officeCode|
                              WHERE  lastName = 'Patterson'    |         1|
                            )                                  |         2|
ORDER BY officeCode;                                           +----------+
```
위의 경우 `ANY` 대신에 `IN`도 사용 가능.
### 다중행 서브쿼리
```
SELECT
FROM
WHERE  expr [NOT] IN (subquery);
```
```
SELECT
FROM
WHERE  [NOT] EXISTS (subquery);
```
- `expr`의 실행 결과는 한 개의 튜플(단일값)
- 서브쿼리는 튜플(단일값)의 집합을 리턴함
- `IN`: 서브쿼리 결과의 어느 한 튜플(값)이 expr과 동일하면 true
- `EXISTS`: 서브쿼리 결과가 있으면 true. 서브쿼리를 만족하는 튜플을 1개 찾으면 더 이상 검색하지 않음. **EXISTS는 연관 서브쿼리에만 사용**
- `expr`과 서브쿼리가 리턴하는 튜플이 모두 단일값이면 `IN`연산자는 `=ANY` 혹은 `=SOME`으로 대체 가능.
```
SELECT  productLine 상품라인, name 상품명, MSRP 소비자가격
FROM    s_products
WHERE   (productLine, MSRP) IN (  
                                  SELECT  productLine, MIN(MSRP) -- 다중행 리턴
                                  FROM    s_products
                                  GROUP   BY productLine
                               )
ORDER BY productLine, name;
```
## 연관 서브쿼리
서브쿼리에서 메인쿼리 테이블의 컬럼을 참조함.

메인쿼리 테이블의 튜플을 필터링하며 조인과 유사하나, 성능면에서 조인보다 우월함.

메인쿼리 테이블의 튜플마다 서브쿼리가 실행됨
### 단일값 서브쿼리
```
SELECT productLine, name, MSRP
FROM   s_products X
WHERE  MSRP = (
                SELECT MIN(MSRP) -- 단일값
                FROM s_products Y
                WHERE Y.productLine = X.productLine -- 연관 조건
              )
ORDER BY productLine, name;
```
### 다중값 서브쿼리
```
SELECT name
FROM   s_customers C
WHERE  customerId = ANY (
                          SELECT customerId -- 다중값
                          FROM   s_orders O
                          WHERE  O.customerId = C.customerId AND O.status IN ('Cancelled', 'On Hold') -- 연관 조건                          
                        );
```
### 다중행 서브쿼리
```
SELECT  name
FROM    s_customers C
WHERE   EXISTS (
                  SELECT * -- 다중행
                  FROM   s_orders O
                  WHERE  O.customerId = C.customerId AND YEAR(orderDate)=2003 AND MONTH(orderDate)=1 -- 연관 조건
               );
```
```
SELECT productCode, name, MSRP
FROM   products X
WHERE  productLine = 'Classic Cars' AND EXISTS (
                                                  SELECT * 
                                                  FROM products Y
                                                  WHERE Y.productCode = X.productCode AND MSRP >= 200
                                               )
ORDER BY 3 DESC, 2;
```
**교집합 연산**: Classic Car인 동시에 가격이 200 이상인 상품을 리턴
```
SELECT productCode, name, MSRP
FROM   products X
WHERE  productLine = 'Classic Cars' AND NOT EXISTS (
                                                        SELECT * 
                                                        FROM   products Y
                                                        WHERE  Y.productCode = X.productCode AND MSRP >= 200
                                                   )
ORDER BY 3 DESC, 2;
```
**차집합 연산**: Classic Car인 동시에 가격이 200 미만인 상품을 리턴
