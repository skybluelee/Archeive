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
```
<div class="media_end_head_top">
		<a href="https://www.yna.co.kr/" class="media_end_head_top_logo">
			<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/logo_001_6_20200915184213.png" width="" height="32" alt="연합뉴스" title="연합뉴스" class="media_end_head_top_logo_img light_type">
			<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/dark_logo_001_6_20200915144859.png" width="" height="32" alt="연합뉴스" title="연합뉴스" class="media_end_head_top_logo_img dark_type">
		</a>
```
