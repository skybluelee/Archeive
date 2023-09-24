# JavaDoc
Java로 작성된 소스 코드를 HTML 형태로 문서화하여 인터넷 창에서 확인할 수 있게 해준다.

직접 인터넷을 사용하는 것이 아닌 Java가 제어하는 인터넷 UI를 통해 확인할 수 있다.
## 문서화
```
javadoc -encoding UTF-8 -charset UTF-8 -d docs ./src/sec13/chap05/*.java
```
를 사용하여 해당 경로의 java 파일을 문서화할 수 있다.

이 경우
```
/**
 * @author ㅁㅁ
 * @version 1.0
 */
public class Person {
    /**
    * comment
    */
    private String name;
}
```
위와 같이 주석처리된 코드는 문서화되지 않는다. 주석을 포함하여 문서화하고자 한다면
```
javadoc -author -version -private -encoding UTF-8 -charset UTF-8 -d docs ./src/sec13/chap05/*.java
```
을 사용한다.
## 문서화 - 어노테이션
코드와 별개로 특징을 설명해준다.

종류
- `@author` : 작성자 정보
- `@version` : 코드의 버전
- `@deprecated` : 더 이상 사용되지 않음
- `@see` : 참조 링크 - 다른 메소드를 참조할 경우 앞에 `#` 붙임
- `@since` : 해당 요소가 추가된 버전
- `@inheritDoc` : 부모 클래스의 문서에서 해당 요소 값을 가져옴
- `@throws` : 발생 가능한 예외
- `@Documented` : 해당 어노테이션이 사용되는 곳의 문서에 어노테이션 정보 표시

`@Documented`를 선언하지 않는다면 커스터마이징한 어노테이션은 코드에 표기되지 않는다.
