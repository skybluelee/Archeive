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
## RANK
### PARTITION BY가 없음
```
SELECT	country, city, COUNT(customerId) no_customer,
        RANK() OVER (
                    ORDER BY COUNT(customerId) DESC
                    ) AS rank_all
FROM    s_customers
GROUP 	BY country
ORDER 	BY rank_all, country;
```
### PARTITION BY가 있음
