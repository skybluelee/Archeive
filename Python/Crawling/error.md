# NoSuchElementException
## time.sleep()
첫번째 경우는 인터넷 창이 완전히 load되기 이전에 코드가 실행되었기 때문에 `NoSuchElementException`오류를 발생하는 경우이다.
```
import time
time.sleep(1)
```
이 경우 time.sleep()을 사용하여 해결할 수 있다.
## class, id 오류
두번째 경우는 class나 id에 해당하는 값에 공백이 존재하는 경우이다.
```
down_bar = content_detail.find_element(By.CLASS_NAME, "ui-dialog-content ui-widget-content") # 기존
down_bar = content_detail.find_element(By.CLASS_NAME, "ui-dialog-content.ui-widget-content") # 수정
```
이 경우 빈칸을 `.`로 대체하여 해결할 수 있다.
