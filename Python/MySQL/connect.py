# pip install mysql-connector-python
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': '*',
    'password': '*',
    'database': '*'
}

conn = mysql.connector.connect(**db_config)
cur = conn.cursor()

# 큰 따옴표와 작은 따옴표로 문자열 묶기
sql = "INSERT INTO table_name (column1, column2) VALUES ('value1', 'value2')"
cur.execute(sql)
conn.commit()

# 여러 줄 문자열 사용하기
sql = """
INSERT INTO table_name
(column1, column2)
VALUES
('value1', 'value2')
"""
cur.execute(sql)
conn.commit()

# 문자열 연결 연산자 사용하기
sql = "INSERT INTO table_name " \
        "(column1, column2) " \
        "VALUES ('value1', 'value2')"
cur.execute(query)
conn.commit()

# str.format() 사용하기
column1_value = 'value1'
column2_value = 'value2'
sql = "INSERT INTO table_name (column1, column2) VALUES ('{}', '{}')".format(column1_value, column2_value)
cur.execute(sql)
conn.commit()

# f-string 사용하기
column1_value = 'value1'
column2_value = 'value2'
sql = f"INSERT INTO table_name (column1, column2) VALUES ('{column1_value}', '{column2_value}')"
cursor.execute(sql)
conn.commit()
