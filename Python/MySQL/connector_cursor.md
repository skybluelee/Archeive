# 코드
```
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': '*',
    'password': '*',
    'database': '*'
}
connector = mysql.connector.connect(**db_config)
cursor = conn.cursor()
```
# connector
MySQL 데이터베이스와 Python 프로그램 간의 연결을 설정하고 관리하는 데 사용되는 라이브러리나 모듈입니다. 

파이썬과 MySQL 간의 통신을 용이하게 만들어준다. `mysql-connector-python`이나 `mysql-connector-python-rf`와 같은 패키지를 사용한다.

## 주요 역할과 특징
- MySQL 서버에 연결을 설정하고 해제하는 역할을 한다.
- 연결 구성 옵션(호스트, 사용자 이름, 암호, 데이터베이스 등)을 설정한다.
- SQL 쿼리를 실행하기 위한 Cursor 객체를 생성한다.
- 연결 관련 오류 처리 및 관리를 담당한다.
# cursor
Cursor는 MySQL 데이터베이스와 상호작용하며 SQL 쿼리를 실행하고 결과를 처리하는 객체이다.

하나의 연결(Connection)에 여러 개의 Cursor를 만들어 다수의 SQL 작업을 동시에 처리할 수 있다.

## 주요 역할과 특징
- SQL 쿼리를 실행하고 결과를 검색, 수정 또는 삭제하는 데 사용된다.
- 쿼리의 실행 결과를 검색하고 처리할 수 있으며, fetchall(), fetchone(), fetchmany()와 같은 메서드를 사용하여 데이터를 추출한다.
- SQL 쿼리를 실행할 때 매개 변수를 사용하여 동적으로 값을 전달할 수 있다.
- 커서를 사용하여 트랜잭션을 관리하고 롤백 또는 커밋할 수 있다.
