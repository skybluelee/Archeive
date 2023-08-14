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
		<div class="media_end_head_top">
			<a href="https://www.yna.co.kr/" class="media_end_head_top_logo">
				<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/logo_001_6_20200915184213.png" width="" height="32" alt="연합뉴스" title="연합뉴스" class="media_end_head_top_logo_img light_type">
				<img src="https://mimgnews.pstatic.net/image/upload/office_logo/001/2020/09/15/dark_logo_001_6_20200915144859.png" width="" height="32" alt="연합뉴스" title="연합뉴스" class="media_end_head_top_logo_img dark_type">
			</a>
	  ...
	  <div class="media_end_head_title">
			<h2 id="title_area" class="media_end_head_headline"><span>전북지사 "잼버리 통해 수십조 SOC 구축 등 허위사실 강경 대처"</span></h2>
	</div>
``` 
