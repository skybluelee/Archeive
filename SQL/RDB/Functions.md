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
해당하는 단어를 포함하는 값을 반환,  m으로 시작하는 문자열을 갖는 값을 반환, m으로 끝나는 문자열을 갖는 값을 반환
# HAVING
GROUP BY 절로 생성한 그룹 중, HAVING 절의 그룹 조건식을 만족하는 특정 그룹만 선택하게 해줌.
