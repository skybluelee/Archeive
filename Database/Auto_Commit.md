# autocommit=False
```
try:
    cur.execute("DELETE FROM kusdk.name_gender;")
    cur.execute("INSERT INTO kusdk.name_gender VALUES ('Claire', 'Female');")
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    conn.rollback()
```
try - except를 사용하여 제어
# autocommit=True
```
try:
    cur.execute("BEGIN;")
    cur.execute("DELETE FROM kusdk.name_gender;")
    cur.execute("INSERT INTO kusdk.name_gender VALUES ('Claire', 'Female');")
    cur.execute("END;")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    cur.execute("ROLLBACK;")
finally :
    conn.close()
```
autocommit이 True이므로 `conn.commit()`이 존재하지 않음
