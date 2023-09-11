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
동시에 선언 가능하다.
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
### 명시적 형변환
```
byte byteNum;
int smallIntNum = 123;

// 명시적 형변환
byteNum = (byte) smallIntNum;
```
강제로 큰 자료형을 작은 자료형으로 변형한다.

`()`에는 기존에 설정한 자료형이 들어가야 하며, 작은 자료형 범위 밖의 숫자를 변환한다면 overflow가 발생한다.
### 연산과 형 변환
```
int a = 1;
int b = 2;
int c = a + b; // 오류 X
long d = a + b; // 오류 X

short e = a + b; // 오류 발생. int -> short는 묵시적 형변환 불가
short f = (short) a + b; // 오류 발생. 이 경우 a에만 명시적 형변환이 적용됨
short g = (short) (a + b); // 오류 X
```
```
byte b1 = 1;
byte b2 = 2;
short s1 = 1;
short s2 = 2;

// 전부 오류 발생
byte b3 = b1 + b2;
short s3 = b1 + b2;
short s4 = b1 + s2;
short s5 = s1 + s2;

// 전부 오류 X
int i1 = b1 + b2;
int i2 = s1 + s2;
int i3 = b1 + s1;
```
`byte, short`의 경우 연산 수행시 int로 연산하므로 같은 자료형임에도 연산이 불가능하다.
## 실수 자료형
### float
```
float flt1 = 3.14f;
```
`float`도 `long`과 마찬가지로 뒤에 float을 나타내는 `f`를 추가한다.

이는 자바에서 기본적으로 `double` 형태로 인식하기 때문이다.
### double vs float
`double`이 `float`에 비해 범위도 넓고, 정밀도도 높다.
### 연산
```
float flt01 = 4.124f;
float flt02 = 4.125f;
double dbl01 = 3.5;

float flt03 = flt01 + flt02; // 오류 없음

float flt04 = flt01 + dbl01; // 오류 발생
float flt04 = float(flt01 + dbl01);
double flt04 = flt01 + dbl01; 
```
`float`과 `double`을 동시에 연산하는 경우 `double`을 `float`으로 명시적 형 변환을 하거나, 큰 자료형인 `double`로 연산하는 방법이 있다.
## 문자 자료형
`short`와 동일하게 2바이트 사용한다.

문자형 '1'과 숫자 1은 다르다. 연산이 제대로 수행되지 않는다.
### 문자 번호
```
char ch5 = '가';     
char ch6 = '가' + 1; // ch6: '각' 44033
```
각 문자별로 해당하는 값이 존재한다.
### char -> int
```
int int_d1 = Character.getNumericValue('1');

또는

int int_d1 = '1' - '0';
```
### 빈 문자열
```
char empty = '';  // 오류 O
char empty = ' '; // 오류 X
String emptyStr = ""; 
```
`char`에는 공백은 올 수 있지만, 빈 문자는 올 수 없다.

빈 문자는 `String`을 사용하여 생성할 수 있다.
## 불리언 자료형
### 부정 연산자
```
boolean bool3 = !true;   // false

boolean bool5 = !!bool3; // false
boolean bool6 = !!!bool3;// true
```
`!`를 사용하면 `not`, `!`의 개수만큼 반전된다. (-)연산과 동일하다.
### 삼항 연산자
`a ? b : c`
`a`는 boolean 값이며, `a`가 true이면 `b`를 반환하고 `a`가 false이면 `c`를 반환한다.
```
int num1OE = num1 % 2 == 1 ? 1 : 2;
char char1OE = num1 % 2 == 1 ? '홀' : '짝';
```
삼항 연산자의 경우 리턴 값의 자료형에 맞게 설정한다.
## 문자열 자료형
리터럴 방식: `String str1 = "Hello World!";`

인스턴스 생성 방식: `String str4 = new String("Hello World!");`
### 문자열 비교
```
String hl1 = "Hello";
String hl2 = "Hello";

boolean bool1 = hl1 == hl2; // true
```
```
String hl3 = new String("Hello");
String hl4 = new String("Hello");

boolean bool3 = hl3 == hl4; // false
```
리터럴 방식에서는 문자열 비교가 가능하지만, 인스턴스 생성 방식에서는 `==`으로 문자열 비교가 불가능하다.
```
boolean bool4 = hl1.equals(hl2); // true
boolean bool4 = "Hello".equals(hl2); // true
```
인스턴스 생성 방식의 경우 `equals()`를 사용하여 비교할 수 있다.
### 문자열 합치기
`+`를 사용하여 문자열을 합칠 수 있다. 

```
int intNum = 123;
float fltNum = 3.14f;
boolean bool = true;
char character = '가';
String str_d1 = "자, 이어붙여볼까요? ";

String str_d2 = str_d1 + intNum + fltNum + bool + character;
// "자, 이어붙여볼까요? 1233.14true가"
```
파이썬과는 다르게 자료형을 `String`으로 지정하면 다른 자료형이더라도 문자열로 만들어 합친다.
### 문자열로 변환
```
String str1 = String.valueOf(true); // "true"
```
`valueOf` 함수를 사용한다.
***
```
String str6 = true + ""; // "true"
```
빈 값을 추가하여 동일한 효과를 얻을 수 있다.
### 이스케이프 표 escape sequence
`String` 내부에 `"`를 사용하면 오류가 발생하고, 엔터는 인식하지 못한다.

아래 표를 참조한다.

|이스케이프 표 escape sequence|대체|
|------|------|
|`\"`|큰따옴표|
|`\’`|작은따옴표|
|`\n`|줄바꿈|
|`\t`|탭|
|`\\`|백슬래시 하나|

경로의 경우 `\` 하나만 사용하지만, 자바에서는 인식하지 못하므로 `\\`를 사용한다.
## 문자열 메소드
### 문자열 길이 반환
`length()`
```
int int3 = "Hello".length();

int3 = 5
```
### 빈 문자열
```
String str1 = "";
String str2 = " \t\n";

boolean bool1 = str1.isEmpty(); // true
boolean bool2 = str2.isEmpty(); // false

boolean bool3 = str1.isBlank(); // true
boolean bool4 = str2.isBlank(); // true
```
`isEmpty()`의 경우 문자열의 길이가 0인지 아닌지를 확인한다.

`isBlank()`의 경우 공백을 제외한 문자열의 길이가 0인지 아닌지를 확인한다.
### 트리밍
파이썬의 `strip()`과 유사하다.
```
String str3 = "\t he llo \n";

String str4 = str3.trim(); // str4 = "he llo"
```
### 문자 반환
```
String str1 = "Hello World";

char ch1 = str1.charAt(0); // ch1 = 'h'
```
***
```
char ch1 = str1.charAt(str1.length() - 1); // 마지막 문자 얻기
```
### 인덱스 반환
파이썬의 `find()`와 유사하다.
```
String str2 = "얄리 얄리 얄라셩 얄라리 얄라";

int int1 = str2.indexOf('얄'); // int1 = 0
int int2 = str2.indexOf('얄', 4);
// int2 = 6,  str[4:]에서 해당 글자를 찾음

int  int4 = str2.lastIndexOf("얄라");
// int 4 = 14, lastIndexOf는 마지막에서부터 찾음
```
해당하는 값이 없으면 -1을 리턴한다.
### 포함 여부 확인
```
boolean bool_b1 = str_b1.contains("호랑이");

boolean bool_b5 = str_b1.startsWith("호랑이", 4);

boolean bool_b7 = str_b1.endsWith("호랑이");
```
리턴 값은 bool이며, `contains`는 문자열 내부에 해당하는 값이 존재하는지 판단하고, 

`startsWith`는 문자열이 해당 값으로 시작하는지를 판단한다. 이때 `indexOf`와 동일하게 슬라이싱하여 확인할 수 있다.

`endsWith`는 문자열이 해당 값으로 끝나는지 판단한다.
### 문자열 비교 2
```
String str_a1 = "ABC";
String str_a2 = "ABCDE";
String str_a3 = "ABCDEFG";

//  같은 문자열이면 0 반환
int int_a1 = str_a1.compareTo(str_a1); // int_a1 = 0

//  시작하는 부분이 같을 때는 글자 길이의 차이 반환
int int_a2 = str_a1.compareTo(str_a2); // int_a2 = -2
int int_a3 = str_a2.compareTo(str_a1); // int_a3 = 2

String str_a4 = "HIJKLMN";

//  시작하는 부분이 다를 때는 첫 글자의 정수값 차이 반환
int int_a6 = str_a1.compareTo(str_a4); // int_a6 = -7
int int_a7 = str_a4.compareTo(str_a3); // int_a7 = 7
```
***
```
// compareToIgnoreCase : 대소문자 구분 없이 비교
int int_b2 = str_b1.compareToIgnoreCase(str_b2); // int_b2 = -3
```
### 대문자 소문자 변형
`toUpperCase(), toLowerCase()`
### 이어붙이기
```
String str_b2 = str_b1 + true + 1 + 2.34 + '가';

String str_b3 = str_b1.concat(true)
                      .concat(1)
                      .concat(2.34)
                      .concat('가'); // 오류 발생
```
`+`를 사용하는 경우 자료형이 `String`이 아니어도 명시적으로 자료형이 변경된다.

반면 `concat`을 사용하는 경우 `String` 자료형끼리만 이어붙일 수 있다.
***
```
String str_c1 = null;
String str_c3 = str_c1 + null + "ABC"; // str_c3: "nullnullABC"

String str_c4 = str_c1.concat("ABC"); // 오류 발생
```
`+`를 사용하는 경우 null 값이 "null"로 변경되어 붙여진다.

반면 `concat`을 사용하는 경우 null 값에 대해 오류가 발생한다.
***
```
String str_d1 = "a" + "b" + "c" + "d";

String str_d2 = new StringBuilder("a").append("b")
                                      .append("c")
                                      .append("d")
                                      .toString();
```
`+`를 사용하는 경우 내부에서 `append`를 사용한다. 즉 하나의 객체만 존재한다.
```
String str_d3 = "a".concat("b") // "ab"가 생성됨
                   .concat("c") // "abc"가 생성됨
                   .concat("d"); // "abcd"가 생성됨
```
반면 `concat`을 사용하는 경우 사용할 때마다 새로운 객체를 생성한다.

**일반적으로 `+`가 `concat`보다 성능이 좋다**
### 반복
```
String str_a1 = "hello";
String str_a2 = str_a1.concat(" ") // "hello "
                      .repeat(3)   // "hello hello hello "
                      .trim();     // "hello hello hello"
```
### 잘라내기
파이썬의 슬라이싱과 유사하다.
```
String str_b1 = "대한민국 다 job 구하라 그래";

String str_b2 = str_b1.substring(7);     // str_b1: "job 구하라 그래"
String str_b3 = str_b1.substring(7, 10); // str_b3: "job"
```
`substring`의 첫번째 인자만 입력하면 해당 값에서 부터 끝가지를 리턴하고, 두번째 인자까지 입력하면 해당 값까지만 리턴한다.
### 치환
```
String str_c1 = "hello world";
String str_c2 = str_c1.replace("world", "world2"); // str_c2: "hello world2"
```
파이썬의 `replace`와 동일하다. 값이 여러개 존재한다면 전부 다 교체한다.
### format

|사용 코드|자료형|
|------|------|
|`%b`|불리언|
|`%d`|10진수 정수|
|`%f`|실수|
|`%c`|문자|
|`%s`|문자열|
|`%n`|(포맷 문자열 내 바꿈)|

formatting의 경우 `\n`이 아닌 `$n`을 사용한다.
```
String str1 = "%s의 둘레는 반지름 X %d X %f입니다.";

String circle = "원";
int two = 2;
double PI = 3.14;

String str2 = str1.formatted(circle, two, PI);
// str2: "원의 둘레는 반지름 X 2 X 3.140000입니다."

String str3 = String.format(str1, circle, two, PI);
// str3: "원의 둘레는 반지름 X 2 X 3.140000입니다."
```
`formatted`는 해당 `String` 값을 지정하고, `format`은 첫번째 인자를 `String` 값을 사용한다.

`formatted`는 13버전부터 사용 가능하다.
### null
`""`는 비어있는 공간을 부여받고, null은 어떠한 공간도 부여받지 않는다.

따라서 `"" != null`이다.
```
Object obj = null;
System sys = null;

Integer nullInt1 = null;
Double nullDbl1 = null;
Boolean nullBool1 = null;
Character nullChr1 = null;
```
참조 자료형은 null로 초기화할 수 있으며,
```
int nullInt2 = null;
double nullDbl2 = null;
boolean nullBool2 = null;
char nullChr2 = null;     // 오류 발생
```
원시 자료형은 null로 초기화가 불가능하다.
## 배열
동일한 타입의 데이터를 고정된 개수만큼 담을 수 있다.
### 선언
```
char[] hello = new char [] {'h', 'e', 'l', 'l', 'o'};
char[] hello = {'h', 'e', 'l', 'l', 'o'};
```
`<자료형>[] <배열 이름> = {<value>}`형식으로 초기화한다.

`<자료형>[] <배열 이름> = new <자료형> [] {<value>}` 방식이 조금 더 엄격한 방식이며, 작동 방식은 동일하다.
***
```
boolean[] boolAry = new boolean[3]; // boolAry: [false, false, false]
int[] intAry = new int[3];          // intAry: [0, 0, 0]
double[] dblAry = new double[3];    // dblAry: [0.0, 0.0, 0.0]
char[] chrAry = new char[3];        // chrAry의 경우 \u0000값이 들어감
String[] strAry = new String[3];    // strAry: [null, null, null]
```
초기화 없이 선언도 가능하다. 이때 default 값이 배열에 생성된다.
```
intAry[0] = 123;
intAry[1] = 456;
intAry[2] = 789;
// intAry: [123, 456, 789]
```
배열의 값 변경 가능하다.
***
```
char[] dirAry3;

dirAry3 = {'동', '서', '남', '북'}; // 오류 발생
dirAry3 = new char[] {'동', '서', '남', '북'};
```
배열의 개수 없이 선언하는 경우 `new <자료형>[]`가 필요하다.
### 다중 배열
```
boolean[][] dblBoolAry = new boolean[3][3];
// dblBoolAry: [false, false, false]
               [false, false, false]
               [false, false, false]

int[][] dblIntAry = {{1, 2, 3},
                     {4, 5},
                     {6, 7, 8, 9}};
```
다중 배열의 경우 각 배열의 크기가 다를 수 있다.
### 원시 자료형 vs 참조 자료형
**배열은 참조 자료형이다.**
```
int int1 = 1;
int int2 = 2;
int2 = int1;   // int1: 1, int2: 1
int2 = 3;      // int1: 1, int2: 3
```
원시 자료형의 경우 서로 다른 객체이다.
***
```
int[] intAry1 = { 1, 2, 3 };
int[] intAry2 = { 4, 5 };
intAry2 = intAry1;           // intAry1: [1, 2, 3], intAry2: [1, 2, 3]
intAry2[1] = 100;            // intAry1: [1, 100, 3], intAry2: [1, 100, 3]
```
참조 자료형의 경우 동일한 객체를 사용하므로 한 배열의 값이 바뀌면 동일한 객체를 바라보는 다른 배열의 값도 바뀐다.
***
문자형(`String`)의 경우 참조형 객체이지만, 원시형처럼 다룬다.
***
배열 앞에 `final`을 추가하면 상수 배열이 된다.

```
final int[] NUMBERS = {1, 2, 3, 4, 5};

NUMBERS = new int[] {2, 3, 4, 5, 6}; // 오류 발생

NUMBERS[0] = 11; // NUMBERS: [11, 2, 3, 4, 5]
```
상수 배열의 경우 초기화한 상태에서 다른 배열을 할당하는 것은 불가능하다. 하지만 배열의 요소를 바꾸는 것은 가능하다.
### string join
```
String[] strings = {"hello", "world", "my", "name"};

String join1 = String.join(", ", strings); // join1: "hello, world, my, name"
String join2 = String.join("", strings);   // join2: "helloworldmyname"
```
## var
```
var intNum = 1;
var doubleNum = 3.14;
var charLet = 'A';
var StringWord = "안녕하세요";

var notInit; // 초기화가 안 됨
var nullVar = null; // null로 초기화
```
자료형 대신에 `var`를 사용하여 변수를 선언할 수 있다. 이 방식은 일반적으로 가독성이 좋기 때문에 사용한다.
***
```
intNum = 1.11; // 오류
```
기존과 같이 정해진 자료형을 변경할 수 없다.
***
```
var chars = new char[] {'A', 'B', 'C', 'D', 'E'};
```
배열의 경우 `new <자료형>[]`을 사용하여 초기화해야 한다.
## 단축어
- `psvm` - 프로그램을 시작하는 메인 메서드
- `sout` - 한 줄 프린트하기
## print
```
System.out.println("hello");
System.out.println("hello");
System.out.println("hello");

// hello
// hello
// hello
```
print뒤의 ln은 line으로 각 줄로 출력한다.
```
System.out.print("hello");
System.out.print("hello");
System.out.print("hello");

// hellohellohello
```
`print` 함수는 기존에 이어서 출력한다.
```
System.out.printf("%s의 둘레는 반지름 X %d X %f입니다.%n", circle, two, PI);

// 원의 둘레는 반지름 X 2 X 3.140000입니다.
```
`printf`는 formatting할 때 사용하며, `print`와 동일하게 붙이므로 `%n`을 사용하여 엔터 효과를 발생시켰다.
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
  - 줄 내리기-1: **F7**: 중단점 기준으로 해당 메소드로 진입
  - 줄 내리기-2: **F8**: 중단점 기준으로 메인 메소드 안에서 내려감
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
