# find_element(s)의 종류
```
driver.find_element(By.CLASS_NAME, 'class_name')
driver.find_element(By.ID, 'id')
driver.find_element(By.CSS_SELECTOR, 'css_selector')
driver.find_element(By.TAG_NAME, 'tag_name')

driver.find_element(By.LINK_TEXT, 'link_text')
driver.find_element(By.PARTIAL_LINK_TEXT, 'partial_link_text')
driver.find_element(By.XPATH, 'xpath')
```
# CLASS_NAME, ID
```
<div class="newsct_wrapper _GRID_TEMPLATE_COLUMN _STICKY_CONTENT"><div id="ct" class="newsct" role="main">
<div class="media_end_head go_trans">	
	  ...
	</div>
	<div class="media_end_head_title">
		<h2 id="title_area" class="media_end_head_headline"><span>전북지사 "잼버리 통해 수십조 SOC 구축 등 허위사실 강경 대처"</span></h2>
	</div>
``` 
CLASS_NAME, ID는 `class="" , id=""` 인 경우에 사용한다. 
```
title_area = total.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
title_info = title_area.find_element(By.CLASS_NAME, "media_end_head_title")
title = title_info.text

title = '전북지사 "잼버리 통해 수십조 SOC 구축 등 허위사실 강경 대처"'
```

`find_elements` 를 사용하는 경우 해당 값의 type은 list이다.
```
inde_txt = printArea.find_elements(By.CLASS_NAME, "inde_txt")
print(type(inde_txt))

list
```

CLASS_NAME, ID뿐 아니라 모든 변수가 WebElement이므로 알맞게 데이터를 바꾸어야 한다(ex .text).
# CSS_SELECTOR, TAG_NAME
`<ul>, <li>, <span>, <a>, <thead>, <tbody>, <tr>` 등에 사용
CSS_SELECTOR, TAG_NAME의 동작 원리는 동일하며 해당 line의 첫 태그를 사용한다. 이때 CSS_SELECTOR와 다른 점은 tag를 이어서 사용 가능하다.
```
<div class="cal_bottom" data-month="08" data-year="2023">
	<ul>
		<li data-val="01"><button type="button"><span class="blind">2019년</span>1</button></li>
		<li data-val="02"><button type="button"><span class="blind">2019년</span>2</button></li>
		<li data-val="03"><button type="button"><span class="blind">2019년</span>3</button></li>
		<li data-val="04"><button type="button"><span class="blind">2019년</span>4</button></li>
		<li data-val="05"><button type="button"><span class="blind">2019년</span>5</button></li>
		<li data-val="06"><button type="button"><span class="blind">2019년</span>6</button></li>
		<li data-val="07"><button type="button"><span class="blind">2019년</span>7</button></li>
		<li data-val="08" class="active"><button type="button"><span class="blind">2019년</span>8</button><b class="blind">현재 선택된 달</b></li>
		<li data-val="09"><button type="button"><span class="blind">2019년</span>9</button></li>
		<li data-val="10"><button type="button"><span class="blind">2019년</span>10</button></li>
	<li data-val="11"><button type="button"><span class="blind">2019년</span>11</button></li>
		<li data-val="12"><button type="button"><span class="blind">2019년</span>12</button></li>
	</ul>
</div>

month = sub_content_box.find_element(By.CLASS_NAME, "cal_bottom")
month_button = month.find_elements(By.CSS_SELECTOR, "ul > li")
```
`ul`, `li`를 사용하여 WebElement를 수집하였다.
## getAttribute
```
<div class="media_end_head_top">
		<a href="https://www.yna.co.kr/" class="media_end_head_top_logo">
			<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/logo_001_6_20200915184213.png" width="" height="32" alt="연합뉴스" title="연합뉴스">
			<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/dark_logo_001_6_20200915144859.png" width="" height="32" alt="연합뉴스" title="연합뉴스">
		</a>
```
class, id가 없는 경우에 사용
```
pub_info = title_area.find_element(By.CLASS_NAME, "media_end_head_top")
pub = pub_info.find_element(By.CSS_SELECTOR, "img").get_attribute("title")

pub = "연합뉴스"
```
추출하고자 하는 text가 해당 WebElement에 <>="text" 형태로 존재한다면 getAttribte을 사용하여 원하는 text를 얻을 수 있다.
```
tag_a = i.find_element(By.TAG_NAME, 'a')
href = tag_a.get_attribute("href")
```
위는 <a href="link">의 형태에서 링크를 추출하는 방법이다.
## thead, tbody
표의 데이터를 수집하는 경우 `thead`에 표의 인덱스가 있고 `tbody`에 데이터가 존재하는 경우가 많다.
```
인덱스 수집
for tbody in table_total[idx].find_elements(By.TAG_NAME, 'thead'):
	for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
	    supply_target_list.append(tr.text)
# 데이터 수집
for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
	for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
	    supply_target_data.append(tr.text) 
```
위와 같은 형식으로 수집하는 것이 효율적이라 생각한다. 위의 경우 각 리스트에 matching하는 방식으로 데이터를 수집하였다.
