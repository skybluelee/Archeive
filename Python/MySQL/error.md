# \ 사용
쿼리 문자열의 경우 `\`를 사용하면 오류가 발생한다. 예를 들면
```
sql = f"INSERT INTO dataknows.building_info VALUES ('{name}', '{location}', {scale}, \
                                                    '{inquiry}', '{inquiry_call}');"
cur.execute(sql)
```
와 같이 사용한다면 `cur.execute(sql)`에서 오류가 발생한다.
코드가 길어지더라도 한 줄로 작성해야 한다.
# Null
Null값을 입력하기 위해서는 쿼리의 해당 자리에 Null 값을 배치한다. 이때 형식에 상관없이(varchar, float, timestamp, ...) Null만 와야 한다.
varchar이라고 `'{Null}'`을 사용하면 `'Null'`로 인식되어 `Null`이라는 문자가 입력된다.
```
sql = f"INSERT INTO dataknows.building_info VALUES ('{name}', '{location}', {scale}, '{inquiry}', '{inquiry_call}');"
# Null
sql = f"INSERT INTO dataknows.building_info VALUES ('{name}', Null, Null, Null, Null);"
```
