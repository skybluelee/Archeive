# 접속(Ubuntu)
```
sudo mysql
```
# 계정 확인
```
select user, host, plugin, authentication_string from mysql.user;
```
# 계정 생성
```
create user '<user_name>'@'%' identified by '<password>'; 
```
# 권한 부여 및 권한 반영
```
grant all privileges on *.* to '<user_name>'@'%';
flush privileges;
```
