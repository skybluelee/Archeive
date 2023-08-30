# java
## javac
자바로 코딩한 .java 파일을 자바 바이트코드로 compile한다.
```
$ ls                                                     
Main.java

$ javac Main.java

$ ls                                                     
Main.class  Main.java
```
`class` 파일이 추가로 생성된다.

`class` 파일은 바이트 코드를 사용자가 해석할 수 있도록 디코딩한 파일이다.
## java
```
$ java Main
Hello world
```
`.java` 파일을 실행한다.

## 단축어
- `psvm` - 프로그램을 시작하는 메인 메서드
- `sout` - 한 줄 프린트하기
# IntelliJ
## RUN
`Main.java`를 RUN 하면 해당 프로젝트 디렉토리에
```
/out/production/<project_name>/Main
```
`Main.Class`가 생성된다.
```
D:\Java\bin\java.exe "-javaagent:D:\IntelliJ\IntelliJ IDEA Community Edition 2023.2.1\lib\idea_rt.jar=3846:D:\IntelliJ\IntelliJ IDEA Community Edition 2023.2.1\bin" -Dfile.encoding=UTF-8 -classpath D:\Java_Project\project1\out\production\project1 Main
Hello world!

Process finished with exit code 0
```
결과는 위와 같다.

단축키는 **shift + F10**
## 주석
- `/* ~ */`
- Ctrl + `/` (주석 해제도 동일)
- 
