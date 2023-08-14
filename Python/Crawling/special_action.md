# iframe
iframe은 같은 인터넷 창에 존재하지만 또다른 html 문서를 삽입한 형태로 iframe내로 진입하고자 하면 `NoSuchElementException` 오류가 발생한다.
```
<iframe name="iframeDialog" id="iframeDialog" frameborder="0" class="ui-dialog-content ui-widget-content" style="overflow: auto; padding: 0px 0px 10px; margin: 0px; width: 100%; min-height: 0px; max-height: none; height: 719.797px;" title="팝업" tabindex="0"></iframe>
    #document
        <!DOCTYPE html>
    ...
```
iframe 형태는 위와 같다. iframe name, id가 존재하고 `<!DOCTYPE html>`에서 iframe의 존재를 확인할 수 있다.

이 문제는 iframe 전환을 통해 해결할 수 있다.
```
driver.switch_to.frame("<iframe name> or <iframe id>") # iframe으로 전환
driver.switch_to.default_content() # iframe 나가기
```
