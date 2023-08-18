# 테이블 생성
```
create table subscription_info (
  name varchar(50) not null,
  supply_type varchar(4) not null, 
  recruit_date datetime not null,
  sub_specific_region_start datetime,
  sub_specific_region_end datetime,
  sub_other_region_start datetime,
  sub_other_region_end datetime,
  sub_all_region_start datetime,
  sub_all_region_end datetime,
  reception_venue varchar(10),
  winner_announce_date datetime,
  winner_announce_link varchar(70),
  contract_date_start datetime,
  contract_date_end datetime,
  estimated_move_in_date datetime,
  PRIMARY KEY (name, supply_type),
  FOREIGN KEY(name) REFERENCES building_info(name)
) engine=InnoDB default charset=utf8;
```
# 테이블 제거
```
drop table skybluelee_db.subscription_info;
```
# 테이블 내용물 제거
```
DELETE FROM skybluelee_db.subscription_info;
```
