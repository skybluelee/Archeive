# java
## 변수
C와 마찬가지로 자료형을 미리 선언해야 한다.
### 변수 변경
자료형의 경우 변경할 수 없다.
```
double pi = 3.14
pi = 3.141592
```
위 경우에는 오류가 발생하지 않는데, 이미 선언한 변수 `pi`의 값을 변경하기 때문이다.
```
double pi = 3.14
double pi = 3.141592
```
하지만 위 경우에는 오류가 발생한다. 이미 선언한 변수 `pi`를 또다시 선언했기 때문이다.
### 변수 선언
```
char ch4 = 'A', ch5 = 'B', ch6 = 'C';
```
### 상수
```
final int INT_NUM = 1;
INT_NUM = 2;
```
`final`을 사용하면 변수의 값을 변경할 수 없어 오류가 발생한다.

상수의 경우 보통 대문자를 사용한다.
한번에 여러개의 변수 선언이 가능하다.
## 정수 자료형

|자료형|크기|표현 범위|
|------|------|-------|
|byte|1바이트 (8비트)|-128 ~ 127 (-2^7 ~ -2^7-1)|
|short|2바이트|-32,768 ~ 32,767|
|int|4바이트|-2,147,483,648 ~ 2,147,483,647|
|long|8바이트|-9,223,372,036,854,775,808 <br> ~ 9,223,372,036,854,775,807|
### 묵시적(암시적) 형변환
```
byte a;
short b = 128;
int c;
c = b;
```
큰 자료형에 작은 자료형의 값을 넣을 수 있다.
***
```
byte a;
short b = 1;
int c;
a = b; // 오류 발생
```
하지만 큰 자료형의 값이 작은 자료형 값 범위 안에 존재하더라도 작은형에 넣을 수 없다.
### long
```
long _8b_long1 = 123456789123456789; // 오류 발생

long _8b_long1 = 123456789123456789L; // 오류 해결
```
`int` 범위를 넘어서는 경우 명시할 필요가 있다.

숫자 끝에 `L`을 추가하면 오류가 발생하지 않는다. 소문자, 대문자 둘 다 가능하며 주로 대문자를 사용한다.
#### 숫자에 , 사용
```
int _4b_int2 = 123_456_789;
long _8b_long2 = 123_456_789_123_456_789L;
```
단위마다 , 대신에 `_`를 사용할 수 있다.
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
## 단축키
- RUN: **shift + F10**
- 중단점 걸고 디버그: **shift + F9**
  - 줄 내리기: **F7**
- 중지: **ctrl+ F2**
# 터미널
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
