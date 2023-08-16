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

`DATE`는 년-월-일로 시간을 변형

`TIME`은 시:분:초로 시간을 변형

`MONTHNAME, DAYNAME`은 결과가 TEXT임
### SYSDATE, NOW
```
SELECT NOW(), NOW() + 0, NOW() + 0.00, SYSDATE(), SYSDATE() + 0, SYSDATE() + 0.00;

+-------------------+--------------+-----------------+-------------------+--------------+-----------------+
|    NOW()|               NOW() + 0|     NOW() + 0.00|          SYSDATE()| SYSDATE() + 0| SYSDATE() + 0.00|
+-------------------+--------------+-----------------+-------------------+--------------+-----------------+
|2023-08-16 10:26:03|20230816102603|20230816102603.00|2023-08-16 10:26:03|20230816102603|20230816102603.00|
+-------------------+--------------+-----------------+-------------------+--------------+-----------------+
```
SYSDATE과 NOW는 현재 시간에 대해 컨텍스트에 따라 문자형 혹은 숫자형으로 출력한다.
```
+-------------------+--------+-------------------+-------------------+--------+-------------------+
|              NOW()|SLEEP(5)|              NOW()|          SYSDATE()|SLEEP(5)|          SYSDATE()|
+-------------------+--------+-------------------+-------------------+--------+-------------------+
|2023-08-16 10:29:05|       0|2023-08-16 10:29:05|2023-08-16 10:29:10|       1|2023-08-16 10:29:10|
+-------------------+--------+-------------------+-------------------+--------+-------------------+
```
차이점으로는 SYSDATE은 시스템의 현재 시각, NOW는 명령어가 실행 시작된 시각을 나타낸다.

**현재 시간은 표준시간으로 나오므로 한국 시간으로 변경하기 위해서는 + 9HOUR가 필요하다**
### WEEKDAY
```
SELECT  CASE WEEKDAY(birthDate)
                WHEN 0 THEN '월'
                WHEN 1 THEN '화'
                WHEN 2 THEN '수'
                WHEN 3 THEN '목'
                WHEN 4 THEN '금'
                WHEN 5 THEN '토'
                WHEN 6 THEN '일'
        END AS dayIndex1_0_Mon,
        CASE DAYOFWEEK(birthDate)
                WHEN 1 THEN '월'
                WHEN 2 THEN '화'
                WHEN 3 THEN '수'
                WHEN 4 THEN '목'
                WHEN 5 THEN '금'
                WHEN 6 THEN '토'
                WHEN 7 THEN '일'
        END AS dayIndex1_0_Mon,
        CASE DATE_FORMAT(birthDate, '%w')
                WHEN 0 THEN '일'
                WHEN 1 THEN '월'
                WHEN 2 THEN '화'
                WHEN 3 THEN '수'
                WHEN 4 THEN '목'
                WHEN 5 THEN '금'
                WHEN 6 THEN '토'
        END AS dayIndex2_0_Sun,
```
WEEKDAY는 요일을 숫자로 출력한다.
### INTERVAL
TIMESTAMP의 경우 +, - 연산이 불가능하다.
```
SELECT DATE(NOW()) + INTERVAL 5 YEAR, DATE(NOW()) + INTERVAL 5 MONTH, DATE(NOW()) + INTERVAL 5 DAY

+-----------------------------+------------------------------+----------------------------+
|DATE(NOW()) + INTERVAL 5 YEAR|DATE(NOW()) + INTERVAL 5 MONTH|DATE(NOW()) + INTERVAL 5 DAY|
+-----------------------------+------------------------------+----------------------------+
|          2028-08-16 00:00:00|           2024-01-16 00:00:00|         2023-08-21 00:00:00|
+-----------------------------+------------------------------+----------------------------+
```
### TIMESTAMPDIFF
`TIMESTAMPDIFF(<unit>, begin, end)` 형식으로 unit에는 `YEAR, HOUR, MINUTE, SECOND`가 존재
```
SELECT  TIMESTAMPDIFF(YEAR, '2000-08-02', '2021-05-15') AS 기준일전,
        TIMESTAMPDIFF(YEAR, '2000-08-02', '2021-08-02') AS 기준일,
        TIMESTAMPDIFF(YEAR, '2000-08-02', '2021-09-15') AS 기준일후;

+-------+------+-------+
|기준일전|기준일|기준일후|
+-------+------+-------+
|     20|   21|      21|
+-------+------+-------+
```
기준일이거나 기준일을 넘어야 카운트되고 기준일 전이라면 카운트되지 않는다.
### DATE_FORMAT
```
SELECT  DATE_FORMAT(NOW(), '%Y-%m-%d %h:%i:%s %p') AS 12시간,
        DATE_FORMAT(NOW(), '%Y, %M %D, %H:%i:%S') AS 24시간;

+-----------------------+--------------------------+
|                 12시간|                     24시간|
+-----------------------+--------------------------+
|2023-08-16 01:02:33 PM|2023, August 16th, 13:02:33|
+-----------------------+--------------------------+
```
```
%a: 요일(Mon,Tue,Wed,...), %b: 월(Jan,Feb,Mar,...), %c: 월(0,1,2,...), %D: 일(0th,1st,2nd,3rd,...), %d: 일(00,01,..,31)
%e: 일(0,1,..,31), %f: microsecond, %H: 시간(00,01,..23), %h: 시간(01,02,..12), %I: 시간(01,02,..12), %i: 분(00,01,..59)
%j: 일(001,002,..,365), %k: 시간(0,1,..23), %l: 시간(1,2,..12), %M: 월(January,..,December), %m: 월(00,01,..,12)
%p: AM,PM, %r: TIME 영역을 (hh:mm:ss AM or PM)로 변환, %S: 초(00,01,..59) 서순(1st,..), %s: 초(00,01,..59) 정수
%T: TIME 영역을 24시간(hh:mm:ss)로 변환, %U: 주(00,01,..53 - 1년은 52 혹은 53주임) - WEEK() mode 0
%u: 주(00,01,..53) - WEEK() mode 1, %V: 주(00,01,..53) - WEEK() mode 2, %v: 주(00,01,..53) - WEEK() mode 3
%W: 요일(Sunday,..,Saturder), %w: 요일(0=Sunday,..,6=Saturday), %X: 연 - %V와 같이 사용, %x: 연 - %v와 같이 사용
%Y: 연 - 4글자, %y: 연 - 2글자
```
- mode 0: 일요일부터 시작하는 주 (주의 시작이 1년의 첫 번째 일요일부터)
- mode 1: 월요일부터 시작하는 주 (주의 시작이 1년의 첫 번째 월요일부터)
- mode 2: 일요일부터 시작하는 주 (주의 시작이 1년의 첫 번째 일요일 또는 1월 4일 이후)
- mode 3: 월요일부터 시작하는 주 (주의 시작이 1년의 첫 번째 월요일 또는 1월 4일 이후)
### GET_FORMAT
```
GET_FORMAT(DATE,'USA'): %m.%d.%Y, GET_FORMAT(DATE,'JIS'): %Y-%m-%d, GET_FORMAT(DATE,'ISO'): %Y-%m-%d
GET_FORMAT(DATE,'EUR'): %d.%m.%Y, GET_FORMAT(DATE,'INTERNAL'): %Y%m%d

GET_FORMAT(DATETIME,'USA'): %Y-%m-%d %H.%i.%s, GET_FORMAT(DATETIME,'JIS'): %Y-%m-%d %H:%i:%s
GET_FORMAT(DATETIME,'ISO'): %Y-%m-%d %H:%i:%sGET_FORMAT(DATETIME,'EUR'): %Y-%m-%d %H.%i.%s
GET_FORMAT(DATETIME,'INTERNAL'): %Y%m%d%H%i%s

GET_FORMAT(TIME,'USA'): %h:%i:%s %p, GET_FORMAT(TIME,'JIS'): %H:%i:%s, GET_FORMAT(TIME,'ISO'): %H:%i:%s
GET_FORMAT(TIME,'EUR'): %H.%i.%s, GET_FORMAT(TIME,'INTERNAL'): %H%i%s
```
### STR_TO_DATE
`STR_TO_DATE(string, '<format>');`
```
SELECT STR_TO_DATE('21,5,2013', '%d,%m,%Y') AS Trans_Date;

+-------------------+
|         Trans_Date|
+-------------------+
|2013-05-21 00:00:00|
+-------------------+
```
문자열을 날짜/시간 타입으로 변환함.
## 타입 변환 함수
> 변환 가능 타입
> **숫자형**: SIGNED[INTEGER], UNSIGNED[INTEGER], REAL, DOUBLE, FLOAT, DECIMAL
> 
> **문자형**: CHAR, CHAR(n)
> 
> **이진 문자형**: BINARY, BINARY(n)
> 
> **날짜형**: DATE, TIME, DATETIME

> 변환 불가능 타입
> **숫자형 중 정수형**: TYNYINT, SMALLINT, MEDIUMINT, INT, BIGINT
> 
> **문자형 중 가변문자형**: VARCHAR(n)
> 
> **문자형 중 텍스트형**: TYNYTEXT, TEXT, MEDIUMTEXT, LONGTEXT
> 
> **날짜형 중 일부**: TIMESTAMP, YEAR
### 표현식
`CAST(expr AS datatype);`
`CONVERT(expr, datatype);`

AS 사용 여부의 차이.
## NULL 관련 함수
`COALESCE(expr1, expr2, expr3, ...)`

만약 COALESCE에 변수가 2개라면 MySQL의 `IFNULL(e1,e2)`, Oracle의 `NVL(e1,e2), SQL Server의 `ISNULL(e1,e2)`와 동일하다.

변수가 3개 이상인 경우 expr1이 NULL이면 expr2 값을 넣고, expr2도 NULL이라면 expr3 값을 넣고, ... , exprn값을 리턴한다.
## 정규식 함수
### Anchor
`^`: 문자열의 시작점
`$`: 문자열의 종료점
### Character Set
```
Character Group  Meaning
[:alnum:]        Alphanumeric
[:cntrl:]        Control Character
[:lower:]        Lower case character
[:space:]        Whitespace
[:alpha:]        Alphabetic
[:digit:]        Digit
[:print:]        Printable character
[:upper:]        Upper Case Character
[:blank:]        whitespace, tabs, ect
[:graph:]        Printable and visible character
[:punct:]        Punctuation
[:xdigit:]       Extended Digit
```
### 특수 기능 문자
- `-`: 문자의 범위 지정
- `.`: 임의의 한 문자
- `^`: NOT
- `|`: OR
- `(...)`: 괄호 안의 정규식을 한 단위로 취급
### Modifier
- `{n}`: 정확히 n회 반복
- `{m, n}`: m부터 n회까지 반복 가능, 단 m < n
- `a?`: a{0,1}, 0 혹은 1회
- `a+`: a{1,}, 1회 이상 반복
- `a*`: a{0,}, 0회 이상 반복
### Character Escape
`^, $, ., ?, +, *, {, }, [, ], (,)` 등 특수문자의 경우 \\를 추가

ex) `\\.$`: .으로 끝나는 문자열
### 정규식 함수의 종류
`REGEXP_LIKE(expr, pattern[, <match_type>])`: 문자열 expr에서, 정규식 pattern과 일치하는 부분 문자열(substring)이 있는지 검사함. 존재하면 true (1), 존재하지 않으면 false (0)을 리턴함.
```
SELECT  name
FROM    s_customers
WHERE   REGEXP_LIKE(name, '^[A]');

+--------------------------+
|                      name|
+--------------------------+
|         Atelier graphique|
|Australian Collectors, Co.|
+--------------------------+
```
A로 시작하는 name을 선택


`REGEXP_INSTR(expr, pattern[, pos[, occurrence[, <match_type>]]])`: 문자열 expr에서, 정규식 pattern과 일치하는 부분 문자열의 시작 위치를 리턴함.

`REGEXP_SUBSTR(expr, pattern[, pos[, occurrence[, <match_type>]]])`: 문자열 expr에서, 정규식 pattern과 일치하는 부분 문자열을 리턴함.

`REGEXP_REPLACE(expr, pattern[, replace[, pos[, occurrence[,<match_type>]]]])`: 문자열 expr에서, 정규식 pattern과 일치하는 모든 부분 문자열을 대체 문자열로 수정함.

`REGEXP_COUNT(expr, pattern[, pos[, occurrence[, <match_type>]]])`: 문자열 expr에서, 정규식 pattern과 일치하는 모든 부분 문자열의 개수를 리턴함.
## 논리 제어 함수
`IF(<condition_expr>, then_result, else_result)`
```
SELECT  country, state, IF(country = 'USA', state, country) AS if_country
FROM    s_customers;

+-------+-----+----------+
|country|state|if_country|
+-------+-----+----------+
| France|     |    France|
|    USA|   NV|        NV|
+-------+-----+----------+
```
# 집합 연산자
`UNION, UNION DISTINCT`는 중복 튜플 제거.

`UNION ALL`은 중복 저장.

`INTERSECT`는 교집합.

`EXCEPT`는 차집합.
