**SELECT, FROM, WHERE, GROUP BY, ORDER BY, LIMIT을 제외한 함수에 대해 설명**
# CONCAT
문자열을 연결하여 새로운 컬럼을 생성하는 함수.
```
SELECT  LastName, FirstName, CONCAT(LastName, FirstName) AS concat,
        CONCAT(LastName, ' ', FirstName) AS space,
        CONCAT(LastName, '+', FirstName) AS plus
FROM    s_customers;

+--------+---------+-------------+--------------+--------------+
|LastName|FirstName|       concat|         space|          plus|
+--------+---------+-------------+--------------+--------------+
| Schmitt|   Carine|SchmittCarine|Schmitt Carine|Schmitt+Carine|
+--------+---------+-------------+--------------+--------------+
```
# CASE
## Searched case expression
```
SELECT  customerId,creditLimit,
        CASE
            WHEN creditLimit < 30000 THEN 30000
            WHEN creditLimit < 60000 THEN 60000
            ELSE 100000
        END AS case_fucntion
FROM    s_customers;

+----------+-----------+-------------+
|customerId|creditLimit|case_fucntion|
+----------+-----------+-------------+
        103|   21000.00|        30000|
        128|   59700.00|        60000|
        112|   71800.00|       100000|
+----------+-----------+-------------+
```
CASE문에서 WHEN은 if-else형식이므로 앞에서 사용한 조건은 뒤에서는 자동으로 생략된다.
## Simple case expression
```
SELECT  customerId,creditLimit,
        CASE creditLimit
            WHEN 21000 THEN 30000
            ELSE 100000
        END AS case_fucntion
FROM    s_customers;

+----------+-----------+-------------+
|customerId|creditLimit|case_fucntion|
+----------+-----------+-------------+
        103|   21000.00|        30000|
        128|   59700.00|       100000|
        112|   71800.00|       100000|
+----------+-----------+-------------+
```
Simple Case문의 경우 조건이 `=`로 고정된 상태이다.
# 집계 함수
`COUNT, SUM, AVG, MIN, MAX, STDDEV, VARIAN, GROUP_CONCAT`

`STDDEV`는 표준편차, `VARIAN`은 분산, `GROUP_CONCAT`은 NULL 값을 제외한 모든 컬럼 값을 `,`로 연결한 문자열 생성.
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
## 중첩 불가
```
SELECT  AVG(COUNT(*))
FROM    customers
GROUP   BY country;
```
AVG, COUNT를 동시에 사용하므로 오류 발생.
# LIKE
```
SELECT  LastName                  SELECT  LastName                    SELECT  LastName
FROM    s_customers               FROM    s_customers                 FROM    s_customers
WHERE   LastName LIKE '%m%';      WHERE   LastName LIKE 'm%';         WHERE   LastName LIKE '%m';

+--------+                        +--------+                           +---------+
|LastName|                        |LastName|                           | LastName|
+--------+                        +--------+                           +---------+
| Schmitt|                        |  Murphy|                           |Pfalzheim|
+--------+                        | Messner|                           |   Graham|
                                  +--------+                           +---------+
```  
해당하는 단어를 포함하는 값을 반환,  m으로 시작하는 문자열을 갖는 값을 반환, m으로 끝나는 문자열을 갖는 값을 반환.
# HAVING
GROUP BY 절로 생성한 그룹 중, HAVING 절의 그룹 조건식을 만족하는 특정 그룹만 선택하게 해줌.

WHERE 절은 튜플을 필터링하고, HAVING 절은 그룹을 필터링하는 것에서 차이점이 존재함.

만약 WHERE만 사용 가능하다면 HAVING은 사용하지 말 것. 성능차이가 매우 심함.
```
SELECT  country, COUNT(country) AS cnt
FROM    s_customers
GROUP   BY country HAVING COUNT(country) >= 5;

+---------+---+
|  country|cnt|
+---------+---+
|   France| 12|
|      USA| 36|
|Australia|  5|
|  Germany| 13|
|    Spain|  7|
|       UK|  5|
+---------+---+
```
# 단일행 내장함수
## 문자형 함수
`ASCII, CHAR, LOWER, UPPER, LENGTH, CONCAT, REPEAT, REVERSE, STRCMP, TRIM, INSTR, SUBSTR, REPLACE`

`ASCII, CHAR`는 ASCII코드 값, ASCII 문자를 리턴

`REPEAT(str, n)`은 n번만큼 반복

`REVERSE(str)`은 문자열을 거꾸로 출력

`STRCMP(str1, str2)`는 str1이 str2보다 작으면 -1, 같으면 0, 크면 1을 리턴

`TRIM(str)`은 문자열에서 맨 앞과 뒤의 공백 문자를 제거

`TRIM({BOTH|LEADING|TRAILING} removed_str FROM str)`은 str에서 맨 앞/뒤의 removed_str을 제거

`INSTR(str, substr)`는 str에서 첫번째 나타나는 substr의 위치를 리턴

`SUBSTR(str, start[, end])`는 str의 start부터 end까지 문자열 리턴. end가 없으면 끝까지 리턴, start가 -1이면 뒤에서부터 카운트.

`REPLACE(str, from_str, to_str)`는 str에 있는 모든 from_str을 to_str로 대체함.
### 문자 파싱
`utm_source`뒤의 어떤 사이트인지를 확인함.
```
SET @url = 'http://www.example.com/landing-page?utm_source=google&utm_medium=email&utm_campaign=march2012';
SELECT SUBSTR(
@url,
INSTR(@url, 'utm_source') + 11,
INSTR(SUBSTR(@url, INSTR(@url, 'utm_source')), '&') – 12);  -- 12는 LENGTH(utm_source=g)
      utm_source=google&utm_medium=email&utm_campaign=march2012
                       |
                       &까지 18
                       18 - 12를 빼면 google의 개수임(utm_source= 는 고정이므로)

http://www.example.com/landing-page?utm_source=google&utm_medium=email&utm_campaign=march2012
                                    |          |    |
                                    1          12   |
                                               1    6
```
## 숫자형 함수
`SIGN, ABS, FLOOR, CEILING, ROUND, TRUNCATE, MOD, POWER, LOG, EXP, SQRT, SIN, COS, TAN, ASIN, ACOS, ATAN`

`SIGN(x)`은 x가 음수, 0, 양수에 따라 -1, 0, 1을 리턴

`FLOOR(x), CEILING(x)`은 각각 소수 버림, 올림

`ROUND(x, d)`는 x를 소수점 이하 d 자리까지 반올림(d+1 자리에서 d 자리로 반올림)

`TRUNCATE(x, d)`는 x를 소수점 이하 d 자리까지 유지하고, 나머지는 버림

`MOD(x, y)`는 x % y

`POWER(x, y)`는 x^^y

`LOG(b, x)`는 log_b(x)

`SQRT(x)`는 x^^2
## 날짜형 함수
`SYSDATE, NOW, DATE, TIME, TIMESTAMP, YEAR, QUARTER, MONTH, MONTHNAME, DAY, DAYNAME, WEEKDAY, TIME, HOUR, MINUTE, SECOND, TIMESTAMPDIFF, DATE_FORMAT, GET_FORMAT, STR_TO_DATE`

