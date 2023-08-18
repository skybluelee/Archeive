# 집계 함수(Aggregated Functions)와 윈도우 함수(Window Functions)
집계 함수의 경우 해당 그룹의 통계와 그룹의 튜플을 보기 위해서는 WITH 절을 사용하여 JOIN 해야 한다

반면 윈도우 함수의 경우 한 쿼리로 구현 가능하다

서브 쿼리로도 구현 가능
## 집계 함수
**집계 함수 + GRUOP BY 절**
- GROUP BY 절을 사용해 여러개의 그룹(테이블의 일부 = subset)을 생성함
- 집계 함수는 각각의 그룹에 한번씩 적용함
  - GROUP BY 절을 생략하면, 테이블 전체를 하나의 그룹으로 간주함. 즉 집계 함수를 테이블 전체에 적용함
- 집계 함수는 그룹마다 하나의 튜플을 리턴함
## 윈도우 함수
**윈도우 함수 + PARTITION BY 절**
- PARTITION BY 절을 사용해, 여러개의 파티션(테이블의 일부 = subset)을 생성함
- 윈도우 함수는 파티션별로 모든 튜플에 각각 적용하고, 계산된 값을 튜플마다 추가함
  - PARTITION BY 절을 생략하면 테이블 전체를 하나의 파티션으로 간주함. 즉 윈도우 함수를 테이블 전체에 적용함
- 윈도우 함수는 결과로 파티션의 모든 튜플들을 리턴함
- 윈도우 함수는 집계 함수의 확장형임
# 윈도우 함수 종류
- 집계 함수: COUNT, SUM, AVG, MIN, MAX
- 순위 함수: RANK, DENSE_RANK, ROW_NUMBER
- 비율 함수: PERCENT_RANK, CUME_DIST, NTILE
- 행 순서 함수: FIRST_VALUE, LAST_VALUE, LAG, LEAD
# 윈도우 함수 형식
```
window_function(exp) OVER
(
    [PARTITION BY exp {, exp}*]                   /* partition definition */
    [ORDER BY exp [ASC|DESC] {, exp [ASC|DESC]}*] /* order definition */
    [ROWS|RANGE <frame_start>|<frame_between>]    /* frame definition */
)
<frame_start> := UNBOUNDED PRECEDING|N PRECEDING|CURRENT ROW
<frame_between> := BETWEEN <frame_start> AND <frame_end>
<frame_end> := UNBOUNDED FOLLOWING|N FOLLOWING|CURRENT ROW
```
`()`는 안에 내용이 없더라도 존재함
## SELECT 문에서의 적용
```
SELECT  window_function(컬럼) OVER
        (
            [PARTITION BY 컬럼_리스트]
            [ORDER BY 컬럼_리스트]
            [ROWS|RANGE <frame_start>|<frame_between>]
        )
FROM 테이블
[ORDER BY 컬럼_리스트];
```
- PARTITION BY 절: 기준 컬럼 값이 같은 튜플끼리 묶어, 테이블을 여러 개의 파티션으로 나눔
- ORDER BY 절: 파티션 내에서, 기준 컬럼으로 튜플을 정렬
  - 윈도우 함수의 ORDER BY 절: 윈도우 함수를 계산할 때, 파티션 내에서의 행 정렬 기준
  - SELECT 문의 ORDER BY 절: 출력할 때, 테이블 전체의 행 정렬 기준
- ROWS/RANGE 절: 파티션 내에서 프레임 정의. (프레임: 파티션 내의 현재 행에 대해 윈도우 함수를 계산할 때 입력하는 행의 집합)
# 프레임
파티션 내의 현재 행에서 윈도우 함수를 계산할 때, 입력(계산의 대상)하는 행의 집합

프레임의 시작과 끝은 파티션의 현재 행에 상대적으로 정의하여, 현재 행이 바뀔 때 프레임이 파티션 내에서 움직일 수 있음
## 프레임 단위
**프레임의 시작과 끝을 정의하는 방법**
- ROW 절: 현재 행과 프레임 시작/끝 행과의 차이를 행의 개수로 나타냄
- RANGE 절: 현재 행과 프레임 시작/끝 행과의 차이를 ORDER BY 기준 컬럼 값으로 나타냄

**ORDER BY 절의 기준 컬럼 값이 동일한 행들의 처리**
- ROW 절: 기준 컬럼 값에 관계 없음
- RANGE 절: 동일한 값을 갖는 행들은 반드시 같은 프레임에 포함됨
## 프레임 시작/끝에 사용 가능한 값
- UNBOUNDED PRECEDING: 파티션의 첫번째 행
- UNBOUNDED FOLLOWING: 파티션의 마지막 행
- _N_ PRECEDING: 현재 행에서 앞으로 _N_ 번째 행 또는 ORDER BY 컬럼값 - _N_
- _N_ FOLLOWING: 현재 행에서 뒤로 _N_ 번째 행 또는 ORDER BY 컬럼값 + _N_
- CURRENT ROW: 현재 행
```
        +---------------------+
________|                     |
        | UNBOUNDED PRECEDING |
   p    |                     |
   A    |     N PRECEDING     |  - ROW: 현재 행에서 앞으로 N번째 행(N=2)
   R    |                     |  - RANGE: 현재 행의 ORDER BY 기준 컬럼 값 - N
   T    |     CURRENT ROW     |
   I    |                     |
   T    |                     |
   I    |     N FOLLOWING     |  - ROW: 현재 행에서 뒤로 N번째 행(N=3)
   O    |                     |  - RANGE: 현재 행의 ORDER BY 기준 컬럼 값 + N
   N    |                     |
________| UNBOUNDED FOLLOWING |
        |                     |
        +---------------------+
```
## 디폴트 프레임
파티션 정의(ROW|RANGE 절)가 없으면 디폴트 프레임이 적용됨
**ORDER BY 절이 없는 경우**
- 행들이 정렬되지 않았으므로, 프레임을 구체적으로 정의할 수 없음
- 파티션 전체가 프레임
- ROW BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
**ORDER BY 절이 있는 경우**
- 행들이 정렬되어 있으므로, 프레임을 구체적으로 정의할 수 있음
- 파티션 첫번째 행부터 현재 행 까지가 프레임
- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
**ROW_NUMBER의 경우**
ORDER BY 절 사용 여부에 상관 없이 ROW 절을 적용

ROW BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
**frame_start 절**
- 프레임의 시작 행만 정의하고, 종료 행은 명시하지 않음
- 종료 행은 디폴트로 현재 행(CURRENT ROW)임
- ORDER BY 절 유무에 따라 ROWS | RANGE를 선택
# 윈도우 함수 + 집계 함수
## ORDER BY가 없는 경우
```
SELECT	productLine, name, quantityInStock,
        SUM(quantityInStock) OVER
        (
            PARTITION BY productLine
            -- 디폴트: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS total_quantity
FROM	s_products;


+----------------+-------------------------------------+---------------+--------------+
|     productLine|                                 name|quantityInStock|total_quantity|
+----------------+-------------------------------------+---------------+--------------+
|    Classic Cars|             1952 Alpine Renault 1300|           7305|        219183|
|    Classic Cars|                  1972 Alfa Romeo GTA|           3252|        219183|
| ...                                                                                 |
|     Motorcycles|1969 Harley Davidson Ultimate Chopper|           7933|         69401|
|     Motorcycles|                1996 Moto Guzzi 1100i|           7933|         69401|
| ...                                                                                 |
|    Vintage Cars|             1928 Ford Phaeton Deluxe|            136|        124880|
|    Vintage Cars|         1930 Buick Marquette Phaeton|           7062|        124880|
+----------------+-------------------------------------+---------------+--------------+
```
파티션한 그룹에 대해 전체 판매량을 리턴.
## ORDER BY가 있는 경우
```
SELECT	productLine, name, quantityInStock,
        SUM(quantityInStock) OVER
        (
            PARTITION BY productLine
            ORDER BY quantityInStock DESC
            -- 디폴트: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS total_quantity
FROM	s_products;

+----------------+-------------------------------------+---------------+--------------+
|     productLine|                                 name|quantityInStock|total_quantity|
+----------------+-------------------------------------+---------------+--------------+
|    Classic Cars|                     1995 Honda Civic|           9772|          9772|
|    Classic Cars|                  2002 Chevy Corvette|           9446|         19218| -- 9772 + 9446 = 19218
|    Classic Cars|                1976 Ford Gran Torino|           9127|         28345| -- 19218 + 9127 = 28345
| ...                                                                                 |
|     Motorcycles|                     2002 Suzuki XREO|           9997|          9997|
|     Motorcycles|                    1982 Ducati 996 R|           9241|         19238|
|     Motorcycles|1969 Harley Davidson Ultimate Chopper|           7933|         27171|
| ...                                                                                 |
+----------------+-------------------------------------+---------------+--------------+
```
내림차순으로 정렬된 quantityInStock에 대한 누적 판매량을 리턴함
## RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```
SELECT	productLine, name, quantityInStock,
        SUM(quantityInStock) OVER
        (
            PARTITION BY productLine
            ORDER BY quantityInStock DESC
            RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS total_quantity
FROM	s_products;

+----------------+-------------------------------------+---------------+--------------+
|     productLine|                                 name|quantityInStock|total_quantity|
+----------------+-------------------------------------+---------------+--------------+
|    Classic Cars|                     1995 Honda Civic|           9772|        219183|
|    Classic Cars|                  2002 Chevy Corvette|           9446|        219183| 
|    Classic Cars|                1976 Ford Gran Torino|           9127|        219183|
| ...                                                                                 |
|     Motorcycles|                     2002 Suzuki XREO|           9997|         69401|
|     Motorcycles|                    1982 Ducati 996 R|           9241|         69401|
|     Motorcycles|1969 Harley Davidson Ultimate Chopper|           7933|         69401|
| ...                                                                                 |
+----------------+-------------------------------------+---------------+--------------+
```
RANGE를 전체 파티션으로 지정한 결과 해당 그룹의 전체 판매량을 리턴
## ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
```
SELECT	productLine, name, quantityInStock,
        SUM(quantityInStock) OVER
        (
            PARTITION BY productLine
            ORDER BY quantityInStock DESC
            ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
        ) AS total_quantity
FROM	s_products;

+----------------+-------------------------------------+---------------+--------------+
|     productLine|                                 name|quantityInStock|total_quantity|
+----------------+-------------------------------------+---------------+--------------+
|    Classic Cars|                     1995 Honda Civic|           9772|         28345| -- 9772 + 9446 + 9127 = 28345
|    Classic Cars|                  2002 Chevy Corvette|           9446|         37468| -- 9772 + 9446 + 9127 + 9123 = 37468
|    Classic Cars|                1976 Ford Gran Torino|           9127|         46510| -- 9772 + 9446 + 9127 + 9123 + 9042 = 46510
|    Classic Cars|                   1968 Dodge Charger|           9123|         45728| -- 9446 + 9127 + 9123 + 9042 + ... = 45728
|    Classic Cars|                1965 Aston Martin DB5|           9042|         45108|
| ...                                                                                 |
+----------------+-------------------------------------+---------------+--------------+
```
현재 행 기준으로 앞의 2행과 뒤의 2행의 값을 합쳐 계산한 값을 리턴
## SELECT에서 ORDER BY 사용
```
SELECT	productLine, name, quantityInStock,
        SUM(quantityInStock) OVER
        (
            PARTITION BY productLine
            ORDER BY quantityInStock DESC
            RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS total_quantity
FROM	s_products
ORDER   BY productLine, name, total_quantity;

+----------------+-------------------------------------+---------------+--------------+
|     productLine|                                 name|quantityInStock|total_quantity|
+----------------+-------------------------------------+---------------+--------------+
|    Classic Cars|          1948 Porsche 356-A Roadster|           8826|        219183|
|    Classic Cars|       1948 Porsche Type 356 Roadster|           8990|        219183|
|    Classic Cars|                   1949 Jaguar XK 120|           2350|        219183|
| ...                                                                                 |
+----------------+-------------------------------------+---------------+--------------+
```
SELECT에서 ORDER BY를 사용하는 경우 윈도우 함수 내에서 정의한 ORDER BY 순서 대로 정렬되지 않는다.

**따라서 윈도우 함수로 생성한 컬럼 또한 지정해야 하며, 이 때문에 SELECT 문에서 ORDER BY 사용은 가급적 하지 않는다.**
# 윈도우 함수 + 순위 함수
## 함수 종류
**RANK**
- 파티션 내에서 현재 행의 순위를 리턴
- 동점자에게 같은 순위를 주며, 이 경우 다음 순위의 동점자 에게 갭이 발생(1등이 2명이면 다음은 3등부터 시작)

**DENSE_RANK**
- 파티션 내에서 현재 행의 순위를 리턴
- 동점자에게 같은 순위를 주며, 이 경우 다음 순위는 갭 없이 연속적으로 이어짐

**ROW_NUMBER**
- 파티션 내에서 현재 행에 일련번호를 부여(1부터 시작)
- 테이블의 각 행에 일련 번호를 붙이거나, 테이블 출력시 pagination에 사용하거나, 파티션 별로 top-N행을 검색하는데 사용
## RANK, DENSE_RANK
```
SELECT	country, COUNT(customerId) no_customer,
        RANK() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS rank_all,
        RANK() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS dense_rank_all
FROM    s_customers
GROUP   BY country;

+-----------+-----------+--------+--------------+
|    country|no_customer|rank_all|dense_rank_all|
+-----------+-----------+--------+--------------+
|        USA|         36|       1|             1|
|    Germany|         13|       2|             2|
|     France|         12|       3|             3|
|      Spain|          7|       4|             4|
|         UK|          5|       5|             5|
|  Australia|          5|       5|             5|
|New Zealand|          4|       7|             6|
|      Italy|          4|       7|             6|
|...                                            |
+-----------+-----------+--------+--------------+
```
두 경우 모두 동점자를 처리하며 RANK의 경우 동점자 이후 갭이 존재하고, DENSE_RANK의 경우 동점자 이후 갭이 존재하지 않는 것을 확인할 수 있다.
## ROW_NUMBER
```
SELECT  ROW_NUMBER() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS row_no,
        country, COUNT(customerId) no_customer,
        RANK() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS rank_all
FROM    s_customers
GROUP   BY country;

+------+-----------+-----------+--------+
|row_no|    country|no_customer|rank_all|
+------+-----------+-----------+--------+
|     1|        USA|         36|       1|
|     2|    Germany|         13|       2|
|     3|     France|         12|       3|
|     4|      Spain|          7|       4|
|     5|         UK|          5|       5|
|     6|  Australia|          5|       5|
|     7|New Zealand|          4|       7|
|     8|      Italy|          4|       7|
+------+-----------+-----------+--------+
```
ROW_NUMBER는 동점자 처리 없는 것을 확인할 수 있다.
### ROW_NUMBER - Pagination, Top-N
```
WITH temp AS
(
    SELECT  ROW_NUMBER() OVER (
                                  ORDER BY COUNT(customerId) DESC
                              ) AS row_no,
            country, COUNT(customerId) no_customer,
            RANK() OVER (
                            ORDER BY COUNT(customerId) DESC
                        ) AS rank_all
    FROM    s_customers
    GROUP   BY country
)
SELECT  *
FROM    temp
WHERE   row_no BETWEEN 3 AND 7;
/* TOP-N
WHERE   row_no >= 5;
*/

+------+-----------+-----------+--------+
|row_no|    country|no_customer|rank_all|
+------+-----------+-----------+--------+
|     3|     France|         12|       3|
|     4|      Spain|          7|       4|
|     5|         UK|          5|       5|
|     6|  Australia|          5|       5|
|     7|New Zealand|          4|       7|
+------+-----------+-----------+--------+
```
WHERE 내부에서는 윈도우 함수에서 얻은 컬럼을 참조할 수 없으므로 CTE를 사용하여 Pagination 및 Top-N 확인 가능.
# 윈도우 함수 + 비율 함수
## 함수 종류
**PERCENT_RANK**
- 파티션별로 현재 행의 percent rank 값을 리턴

**CUME_DIST**
- 파티션별로 현재 행의 cumulative distribution(누적 분포) 값을 리턴

**NTILE**
- 파티션을 N개의 버킷으로 나눔
- 현재 행이 속한 버킷 번호를 리턴
## PERCENT_RANK
```
SELECT  RANK() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS rnk,
        country, city, COUNT(customerId) no_customer,
        PERCENT_RANK() OVER (
                                ORDER BY COUNT(customerId) DESC
                            ) AS percentRank
FROM    s_customers
WHERE   country = 'France'
GROUP   BY country, city
ORDER   BY country, percentRank;

+------+-------+----------+-----------+-----------+
|   rnk|country|      city|no_customer|percentRank|
+------+-------+----------+-----------+-----------+
|     1| France|     Paris|          3|          0| -- 누적이 0
|     2| France|    Nantes|          2|      0.125| -- (2 - 1) / (9 - 1) = 0.125
|     3| France|      Lyon|          1|       0.25| -- (3 - 2) / (9 - 1) = 0.25
|     3| France|     Lille|          1|       0.25|
|     3| France|Strasbourg|          1|       0.25|
|     3| France|  Toulouse|          1|       0.25|
|...                                              |
+------+-------+----------+-----------+-----------+
```
전체 튜플 개수에 대한 순위의 누적 백분율을 나타냄

공식: (RANK - 1) / (total_rows - 1)
## CUME_DIST
```
SELECT  RANK() OVER (
                        ORDER BY COUNT(customerId) DESC
                    ) AS rnk,
        country, city, COUNT(customerId) no_customer,
        CUME_DIST() OVER (
                                ORDER BY COUNT(customerId) DESC
                            ) AS cumeDistribution
FROM    s_customers
WHERE   country = 'France'
GROUP   BY country, city
ORDER   BY country, percentRank;

+---+-------+----------+-----------+----------------+
|rnk|country|      city|no_customer|cumeDistribution|
+---+-------+----------+-----------+----------------+
|  1| France|     Paris|          3|0.11111111111111| -- 1 / 9 = 0.1111...
|  2| France|    Nantes|          2|0.22222222222222| -- (1 + 1) / 9 = 0.2222...
|  3| France|      Lyon|          1|               1| -- (1 + 1 + 7) / 9 = 1
|  3| France|     Lille|          1|               1|
|  3| France|Strasbourg|          1|               1|
|  3| France|  Toulouse|          1|               1|
|...                                                   |
+---+-------+----------+-----------+----------------+
```
순위를 기준으로 한 튜플 개수의 누적 백분율

공식: (처음부터 같은 등수까지의 튜플 개수) / total_rows
## NTILE
```
SELECT  ROW_NUMBER() OVER (
                                ORDER BY COUNT(customerId) DESC
                          ) AS row_no,
        country, city, COUNT(customerId) no_customer,
        NTILE(2) OVER (
                            ORDER BY COUNT(customerId) DESC
                      ) AS tile_no
FROM    s_customers
WHERE   country = 'Spain'
GROUP   BY country, city;

+------+-------+----------+-----------+-------+
|row_no|country|      city|no_customer|tile_no|
+------+-------+----------+-----------+-------+
|     1|  Spain|    Madrid|          5|      1|
|     2|  Spain| Barcelona|          1|      1|
|     3|  Spain|   Sevilla|          1|      2|
+------+-------+----------+-----------+-------+
```
```
SELECT  ROW_NUMBER() OVER (
                                ORDER BY COUNT(customerId) DESC
                          ) AS row_no,
        country, city, COUNT(customerId) no_customer,
        NTILE(3) OVER (
                            ORDER BY COUNT(customerId) DESC
                      ) AS tile_no
FROM    s_customers
WHERE   country = 'Spain'
GROUP   BY country, city;

+------+-------+----------+-----------+-------+
|row_no|country|      city|no_customer|tile_no|
+------+-------+----------+-----------+-------+
|     1|  Spain|    Madrid|          5|      1|
|     2|  Spain| Barcelona|          1|      2|
|     3|  Spain|   Sevilla|          1|      3|
+------+-------+----------+-----------+-------+
```
파티션을 N개 버킷으로 분할함
# 윈도우 함수 + 행 순서 함수
## 함수 종류 및 형식
**FIRST_VALUE**
- 파티션의 프레임 내에서 첫번째 행의 FIRST_VALUE 기준 컬럼 값

**LAST_VALUE**
- 파티션의 프레임 내에서 마지막 행의 FIRST_VALUE 기준 컬럼 값

**LAG**
- 파티션 내에서 현재 행에 뒤쳐진(lagging) 행, 즉 앞 행의 LAG 기준 컬럼 값

**LEAD**
- 파티션 내에서 현재 행에 앞선(leading) 행, 즉 앞 행의 LEAD 기준 컬럼 값

**LAG, LEAD 형식**
- LAG|LEAD (expr[, N[, default]])
- 첫번째 인자: 기준 컬럼
- 두번째 인자: 앞/뒤의 몇 번째 행을 가져올지 결정(디폴트는 1)
- 세번째 인자: NULL인 경우 대체할 값. COALESCE와 동일
## FIRST_VALUE
```
SELECT  name, country, city,
        FIRST_VALUE(creditLimit) OVER
        (
            PARTITION BY country
            ORDER BY creditLimit DESC
        ) AS max_limit
FROM    s_customers

+---------------------------------+---------+------------+---------+
|                             name|  country|        city|max_limit|
+---------------------------------+---------+------------+---------+
|       Australian Collectors, Co.|Australia|   Melbourne|117300.00|
|          Anna's Decorations, Ltd|Australia|North Sydney|117300.00|
|        Souveniers And Things Co.|Australia|   Chatswood|117300.00|
|...                                                               |
|           Saveley & Henriot, Co.|   France|        Lyon|123900.00|
|                La Rochelle Gifts|   France|      Nantes|123900.00|
|                Auto Canal+ Petit|   France|       Paris|123900.00|
|...                                                               |
+---------------------------------+---------+------------+---------+
```
해당 파티션에 속한 컬럼의 첫번째 값으로 전부 통일됨
## LAG
```
SELECT  name, country, city, creditLimit,
        LAG(creditLimit) OVER 
        (
            ORDER BY creditLimit DESC
        ) AS creditLimit_lag
FROM    s_customers

+---------------------------------+-----------+------------+-----------+---------------+
|                             name|    country|        city|creditLimit|creditLimit_lag|
+---------------------------------+-----------+------------+-----------+---------------+
|           Euro+ Shopping Channel|      Spain|      Madrid|  227600.00|               |
|     Mini Gifts Distributors Ltd.|        USA|  San Rafael|  210500.00|      227600.00|
|                  Vida Sport, Ltd|Switzerland|      Genève|  141300.00|      210500.00|
|               Muscle Machine Inc|        USA|         NYC|  138500.00|      141300.00|
|                   AV Stores, Co.|         UK|  Manchester|  136800.00|      138500.00|
|...                                                                                   |
+---------------------------------+-----------+------------+-----------+---------------+
```
디폴트 값으로는 한칸씩 값이 밀리는 것 확인
```
SELECT  name, country, city, creditLimit,
        LAG(creditLimit, 2, 1000.00) OVER 
        (
            ORDER BY creditLimit DESC
        ) AS creditLimit_lag
FROM    s_customers

+---------------------------------+-----------+------------+-----------+---------------+
|                             name|    country|        city|creditLimit|creditLimit_lag|
+---------------------------------+-----------+------------+-----------+---------------+
|           Euro+ Shopping Channel|      Spain|      Madrid|  227600.00|        1000.00|
|     Mini Gifts Distributors Ltd.|        USA|  San Rafael|  210500.00|        1000.00|
|                  Vida Sport, Ltd|Switzerland|      Genève|  141300.00|      227600.00|
|               Muscle Machine Inc|        USA|         NYC|  138500.00|      210500.00|
|                   AV Stores, Co.|         UK|  Manchester|  136800.00|      141300.00|
|...                                                                                   |
+---------------------------------+-----------+------------+-----------+---------------+
```
2칸씩 밀리고, NULL 값은 1000.00으로 대체됨
# 그룹 함수
## ROLLUP
- GROUP BY 절에서만 사용하는 함수
- 레벨별 통계치를 계산하는 함수
  - 함수의 인자로 컬럼 리스트(grouping column list)를 가짐
  - 컬럼이 N개면 N+1개의 grouping set을 생성하며, 각각의 grouping set에 대해 통계치를 계산
    - L0: (C1, C2, C3) 소계
    - L1: (C1, C2, *)  중계
    - L2: (C1, *, *)   합계
    - L3: (*, *, *)    총계
  - L1, L2, L3에 해당하는 행을 super-aggregate row라 함
- ROLLUP() 함수의 인자는 계층 구조를 형성
- MySQL: `GROUP BY orderYear, productLine WITH ROLLUP;`
- 표준 SQL: `GROUP BY ROLLUP(orderYear, productLine);`
## 집계 함수 + ROLLUP
```
SELECT  productLine, vendor, SUM(buyPrice) AS total_price
FROM	  s_products P
        JOIN s_orderdetails O USING(productCode)
GROUP   BY productLine, vendor WITH ROLLUP;

+--------------+------------------------+-----------+
|   productLine|                  vendor|total_price|
+--------------+------------------------+-----------+
|  Classic Cars|   Autoart Studio Design|    2574.18|
|  Classic Cars|Carousel DieCast Legends|    2477.82|
|  Classic Cars| Classic Metal Creations|   11005.61|
|...                                                |
|  Classic Cars|                        |   65924.62|
|   Motorcycles|   Autoart Studio Design|    2626.67|
|   Motorcycles|           Exoto Designs|    1873.76|
|   Motorcycles|    Gearbox Collectibles|    	651.78|
|...                                                |
|   Motorcycles|                        |   18254.99|
|...                                                |
|              |                        |  163510.11|
+--------------+------------------------+-----------+
```
> L0: productLine, vendor
> L1: productLine, *
> L2: *, *

grouping한 후에 해당 그룹, 해당 그룹의 합, 전체 합을 확인할 수 있음
## 집계 함수 + ROLLUP + GROUPING
GROUPING 함수는 Super-aggreagte row에서 NULL 값을 출력하는 대신 의미있는 레이블을 출력함

GROUPING 함수의 인자에 해당하는 값이 NULL이면 true(1)을 리턴하고 NULL이 아니면 false(0)을 리턴
```
SELECT  productLine, vendor, SUM(buyPrice), GROUPING(productLine), GROUPING(vendor)
FROM	  s_products P
        JOIN s_orderdetails O USING(productCode)
GROUP   BY productLine, vendor WITH ROLLUP;

+--------------+------------------------+-----------+---------------------+----------------+
|   productLine|                  vendor|total_price|GROUPING(productLine)|GROUPING(vendor)|
+--------------+------------------------+-----------+---------------------+----------------+
|  Classic Cars|   Autoart Studio Design|    2574.18|                    0|               0|
|  Classic Cars|Carousel DieCast Legends|    2477.82|                    0|               0|
|  Classic Cars| Classic Metal Creations|   11005.61|                    0|               0|
|...                                                                                       |
|  Classic Cars|                        |   65924.62|                    0|               1|
|   Motorcycles|   Autoart Studio Design|    2626.67|                    0|               0|
|   Motorcycles|           Exoto Designs|    1873.76|                    0|               0|
|   Motorcycles|    Gearbox Collectibles|     651.78|                    0|               0|
|...                                                                                       |
|   Motorcycles|                        |   18254.99|                    0|               1|
|...                                                                                       |
|              |                        |  163510.11|                    1|               1|
+--------------+------------------------+-----------+---------------------+----------------+
```
### CASE를 사용한 NULL 제거
```
SELECT  CASE GROUPING(productLine)
             WHEN 1 THEN 'productLine'
             ELSE productLine
        END AS productLine, SUM(buyPrice) AS total_price
FROM	s_products P
        JOIN s_orderdetails O USING(productCode)
GROUP   BY productLine WITH ROLLUP;

+----------------+-----------+
|     productLine|total_price|
+----------------+-----------+
|    Classic Cars|   65924.62|
|     Motorcycles|   18254.99|
|          Planes|   16675.40|
|           Ships|   11514.33|
|          Trains|    3557.79|
|Trucks and Buses|   17349.36|
|    Vintage Cars|   30233.62|
|     productLine|  163510.11|
+----------------+-----------+
```
## CUBE
ROLLUP 함수의 확장으로 grouping column list의 모든 조합에 대해 통계치를 계산
- 함수의 인자로 컬럼 리스트를 가짐
- 컬럼이 N개면 2^N개의 grouping set을 생성하며, 각각의 grouping set에 대해 통계치를 계산함
- GROUP BY CUBE(C1, C2, C3)라면
  - L0: (C1, C2, C3) 소계
  - L1: (C1, C2, *)  중계
  - L1: (C1, C3, *)  중계
  - L1: (C2, C3, *)  중계
  - L2: (C1, *, *)   합계
  - L2: (C2, *, *)   합계
  - L2: (C3, *, *)   합계
  - L3: (*, *, *)    총계
