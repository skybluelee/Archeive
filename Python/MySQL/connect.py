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

sql = f"INSERT INTO dataknows.building_info VALUES ();"
print(sql)
cur.execute(sql)
conn.commit()
