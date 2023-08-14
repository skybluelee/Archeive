# image 다운로드
image는 특정 링크에 존재하는 정보를 화면에 나타내는 방식이다. 해당 링크를 추출하고 링크의 내용을 다운받으면 이미지를 다운받을 수 있다.
```
...
<span class="gd_img" style="transform: translate3d(0px, 0px, 0px);">
    <em class="imgBdr">
        <span id="dImg" class="thumbBArea"></span>
        <img class="gImg" src="https://image.yes24.com/goods/120466973/XL" alt="호랭면 " border="0">
    </em>
    <!-- 스티커 : 직배송 할인 & 포스터 -->
    ...
```
```
img_folder = './img'
yes = driver.find_element(By.ID, "yDetailTopWrap")
info = yes.find_element(By.CLASS_NAME, "topColLft")
intro = info.find_element(By.CLASS_NAME, "gd_imgArea")
imgs = intro.find_element(By.CSS_SELECTOR, "span > em > img").get_attribute("src")
urllib.request.urlretrieve(imgs, f'./img/{name}.jpg')
```
