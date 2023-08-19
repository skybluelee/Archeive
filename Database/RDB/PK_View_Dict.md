# PK, FK
## PK 제약 조건
- DB의 개체 무결성 유지
- PK 제약 조건은 한 번만 선언
  - PK는 한 개 이상의 컬럼, 즉 컬럼의 집합
  - PK선언이 되지 않으면, 컬럼중 UNIQUE, NOT NULL이 같이 설정된 첫번째 컬럼이 PK가 됨
## PK 제약조건 유지를 위한 DBMS 동작
- INSERT/UPDATE 문에서 테이블의 PK값으로 NULL 또는 기존 PK 값이 시도되는 경우 DBMS가 거절
## FK 제약 조건
- 자식 테이블의 FK 값은 부모 테이블의 PK 값 중 하나이거나, NULL 값이어야 함
- FK는 여러번 선언 가능
## FK 제약조건 유지를 위한 DBMS 동작
- INSERT, UPDATE 문에서 부모 테이블의 PK에 존재하지 않는 값이 자식 테이블의 FK 값으로 시도될 경우, DBMS가 이 명령의 실행을 거부함
- DELETE, UPDATE 문에서 부모 테이블의 PK값을 삭제/수정할 경우 아래 동작을 실행
  -  NO ACTION, RESTRICT: 자식 테이블의 FK에 해당하는 PK 값을 갖는 튜플이 한 개 이상 존재하면, DBMS가 명령 실행 거부
  -  SET NULL, SET DEFAULT: 해당 PK 값을 갖는, 자식 테이블의 모든 FK 값을 NULL 혹은 디폴트 값으로 수정
  -  CASCADE: 자식 테이블의 FK에 해당 PK 값을 갖는 모든 튜플을 연속적으로 삭제/수정
## FK 제약 조건 설정
```
SET foreign_key_checks = 0; // FK 검사 비활성화
SET foreign_key_checks = 1; // FK 검사 활성화, 디폴트
```
## 참조 무결성 옵션
- NO ACTION, RESTRICT: 부모 테이블에 대한 DELETE/UPDATE 문에 의해 영향받는 자식 테이블의 튜플이 존재하면, 실행 거부. 디폴트는 NO ACTION
- SET NULL, SET DEFAULT: 부모 테이블에 대한 DELETE/UPDATE 문에 의해 영향 받는 자식 테이블의 모든 튜플에 대해 FK 값을 NULL 또는 디폴트 값으로 대체
- CASCADE: 부모 테이블에 대한 DELETE/UPDATE 문에 의해 영향받는 자식 테이블의 모든 튜플에 대해서도 삭제/수정을 연속적으로 실행
## 참조 무결성 옵션 설정
- ON DELETE NO ACTION, ON UPDATE NO ACTION: 삭제/수정 거부(디폴트)
- ON DELETE NO ACTION, ON UPDATE CASCADE: 삭제 거부, 수정 허용(안전한 모드, 가장 많이 사용)
- ON DELETE SET NULL, ON UPDATE CASCADE: 삭제/수정 허용, 부모 튜플 제거시 자식 튜플은 독립적으로 존재
- ON DELETE CASCADE, ON UPDATE CASCADE: 삭제/수정 허용, 부모 튜플 제거시 자식 튜플도 삭제
**모든 자손 테이블의 FK가 ON DELETE CASCADE인 경우**: 부모 테이블의 삭제가 자손 테이블로 전파됨
  
**자식 테이블의 FK가 ON DELETE SET NULL | DEFAULT, ON UPDATE CASCADE, ON UPDATE SET NULL | DEFAULT인 경우**: 자식 테이블만 영향 받음(파급 효과가 한 레벨에만 영향을 줌)
# View
- 하나 이상의 기본 테이블로부터 유도된 가상 테이블
- 검색문(SELECT 문)을 사용하여 정의
- DBMS는 뷰의 정의(SELECT 문)만 저장, 뷰에 대한 검색 요청시 결과가 동적으로 생성됨.
## 생성
```
CREATE VIEW 뷰_이름 [(컬럼명_리스트)] AS
SELECT 문
[WITH CHECK OPTION];
```
WITH CHECK OPTION
- Updatable view에 대한 삽입/수정 명령이 실행될 때, 뷰의 정의 조건(SELECT 문의 WHERE 절)이 위배되면, 삽입/수정 명려의 실행이 거부됨
### WHERE
```
CREATE VIEW abnormalOrders AS
SELECT *
FROM   orders
WHERE  status IN ('Cancelled', 'Disputed', 'On Hold') // WHERE의 조건은 'Cancelled', 'Disputed', 'On Hold' 3가지 상태여야 함
WITH CHECK OPTION;

INSERT INTO abnormalOrders
VALUES (20001, '2021-07-01', '2021-07-21', '2021-07-12', 'Shipped', NULL, 181); // Shipped는 WHERE 절에 위배되므로 삽입 명령 거부
```
### FROM
```
CREATE VIEW ParisOffice_customers (companyName, contactPerson, country) AS -- Create에서 ()내부에 지정한 값이 컬럼 값이 됨
SELECT C.name, CONCAT(C.contactFirstName, ' ', C.contactLastName), C.country
FROM   offices O
       JOIN  employees E USING (officeCode)
       JOIN customers C ON E.employeeId = C.salesRepId
WHERE  O.city = 'Paris'
WITH CHECK OPTION;

+---------------+---------------+-------+
|    companyName|  contactPerson|country|
+---------------+---------------+-------+
|Lyon Souveniers|Daniel Da Silva| France|
+---------------+---------------+-------+
```
```
CREATE VIEW nonFranch_ParisOffice_customers AS
SELECT *
FROM ParisOffice_customers
WHERE country <> 'France'
WITH CHECK OPTION;
```
WITH 절 처럼 생성한 view를 FROM에서 사용 가능
## 뷰 제거
```
DROP VIEW 뷰_이름 {RESTRICT|CASCADE}
```
- RESTRICT: 제거하려는 뷰에서 유도한 다른 뷰가 있으면 실행 거부(디폴트)
- CASCADE: 제거하려는 뷰에서 유도한 다른 뷰가 있으면 함께 제거
## 질의 재작성
```
CREATE  VIEW customersPerEmployee AS
SELECT  O.city AS office, CONCAT(E.firstName, ' ', E.lastName) AS employee, E.jobTitle, C.name AS customer
FROM    s_offices O LEFT JOIN s_employees E USING (officeCode)
        LEFT JOIN customers C ON E.employeeId = C.salesRepId;
```
```
SELECT  *
FROM    customersPerEmployee
WHERE   office = 'San Francisco'
ORDER   BY office, employee, customer;
```
WITH 절과 유사
## 뷰 수정
수정 가능한 뷰
- 뷰의 튜플이 기본 테이블의 튜플과 일대일 대응할 때(뷰의 정의에 기본 테이블의 PK가 포함될 때)

수정 불가능한 뷰
- 집계 함수
- DISTINCT
- GROUP BY
- HAVING
- UNION
- scalar subquery(SELECT 절 서브쿼리)
- 일부 조인 연산
## 장단점
### 장점
- 독립성
  - 기본 테이블 구조를 변경해도, 뷰를 통해 테이블을 사용하는 응용 프로그램은 영향받지 않음
  - 테이블 확장 및 구조 변경에 용이
- 편리성
  - 복잡한 질의의 일부를 뷰로 미리 정의함으로써, 최종 질의를 단순하게 작성할 수 있음
  - 해당 뷰를 자주 사용할 때 유용
- 보안성
  - 숨기고 싶은 정보는 제외하고 뷰를 생성하여 사용자에게 특정 정보를 감출 수 있음(접근 제어)
- 사용자 권한에 따라 다양한 뷰를 제공함
### 뷰의 단점
- 독자적인 인덱스가 없음
- 데이터 갱신(INSERT, DELETE, UPDATE)에 제약이 많음
- 정의를 변경할 수 없음
# 데이터 사전
데이터에 대한 데이터, 즉 메타데이터의 집합

**INFORMATION SCHEMA**: 설계자가 DDL로 정의한 스키마 정보를 담고 있는 스키마
- MySQL 시스템이 내부적으로 유지
- 데이터 사전 역할
## SCHEMATA
```
USE INFORMATION_SCHEMA;
SELECT *
FROM SCHEMATA;
```
```
SELECT *
FROM   INFORMATION_SCHEMA.SCHEMATA;
```
MySQL에 생성된 모든 스키마 정보를 제공
## TABLES
```
SELECT *
FROM INFORMATION_SCHEMA.TABLES;
```
정의된 모든 테이블 정보를 제공
## COLUMNS
```
SELECT *
FROM INFORMATION_SCHEMA.COLUMNS;
```
정의된 모든 컬럼 정보를 제공
## KEY_COLUMN_USAGE
```
SELECT CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME,
REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE CONSTRAINT_SCHEMA = 'classicmodels'
ORDER BY CONSTRAINT_NAME DESC;
```
정의된 모든 PK, FK에 대한 정보 제공
## REFERENTIAL_CONSTRAINTS
```
SELECT CONSTRAINT_SCHEMA, CONSTRAINT_NAME, DELETE_RULE, UPDATE_RULE, TABLE_NAME,
REFERENCED_TABLE_NAME
FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'classicmodels';
```
정의된 모든 FK의 참조 무결성 옵션에 대한 정보 제공
## CHECK_CONSTRAINTS
```
SELECT *
FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'classicmodels';
```
정의된 모든 CHECK 제약 조건에 대한 정보 제공
