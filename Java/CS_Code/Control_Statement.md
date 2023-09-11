# if
```
boolean strat1 = true;
boolean strat2 = true;
boolean strat3 = true;

if (strat1) {
    String num = "";

    //  필요에 따라 적절한 것 사용
    num = strat2 ? "1" : "2";
}
else if (strat3) {
    System.out.println("3")
else {
    String num = "3";
}

System.out.println(num); // 오류 발생
```

`if (조건문) {실행 함수}` 형식으로 작성한다.

실행할 명령문이 하나라면 `{}`를 사용하지 않아도 된다. `if (open) System.out.println("open");`

`if`문 내에서 사용되는 변수는 밖에서는 확인할 수 없다. 따라서 `if`문 내의 변수`num`을 `if`문 밖에서 출력하려고 오류가 발생한다.
# switch
```
byte month = 1;
String quarter = "";

switch (month) {
    case 1:
    case 2:
    case 3:
        quarter += "Q1";
    case 4: case 5: case 6:
        quarter += "Q2";
    case 7:
        quarter += "Q3";
        break;
    case 8: case 9:
        quarter += "Q3";
        break;
    case 10: case 11: case 12:
        quarter += "Q4";
        break;
    default:
        quarter += "error";
}

System.out.println(quarter);
```
```
byte month: 1 -> quarter: Q1Q2Q3
byte month: 4 -> quarter: Q2Q3
byte month: 7 -> quarter: Q3
```
`switch (<변수>) case <변수>: <실행문>;` 형식으로 작성한다.

switch에서 사용 가능한 변수로는 `byte, short, int, char, String, enum`이 존재한다.

`case`의 경우 동일한 실행문에 대해 한번만 작성 가능하다. `case 4: \n case 5: \n case 6:`와 `case 4: case 5: case 6:`는 동일하다.

`break`을 사용하지 않는 경우 해당 실행문부터 아래의 모든 실행문을 `break`이 나올 때까지 실행한다.

`default`는 if문의 `else`와 동일하다.
# for
```
for (int i = 0; i < 10; i++) {
    System.out.println(i);
    i += 2;
    System.out.println(i);
    System.out.println("- - - - -");
}

0
2
- - - - -
3
5
- - - - -
6
8
- - - - -
9
11
- - - - -
```
`for (<변수>; <조건>; <변수 변화>) {<실행문>}` 형식으로 작성한다.

`for` 제어에 사용하는 변수 `i`와 `for` 문 내에서 사용하는 변수 `i`는 동일하다.
```
int count = 3;
int[] multiOf4 = new int[10];

for (int i = 1, c = 0; c < count; i++) {
    if (i % 4 == 0) {
        multiOf4[c++] = i; // multiOf4: [4, 8, 12]
    }
}
```
조건에 사용하는 변수는 여러개 사용 가능하며, 단 자료형은 동일해야 한다.
## 변수 범위
```
for (int i = 1; i < 10; i++) {
    for (int j = 1; j < 10; j++) {
        System.out.printf("%d X %d = %2d%n", i, j, i * j);
    }
    System.out.println(j); // 오류 발생 X
}
System.out.println(j); // 오류 발생 O
```
`for`문에서 사용한 변수는 해당 `for`문 블록 내에서는 사용가능하며, 블록 바깥에서는 사용 불가능하다.
## 무한 루프
```
for (;;) {
    System.out.println("영원히");
}
System.out.println("닿지 않아"); // 컴파일 오류 발생
```
`for (;;)`를 사용한 무한루프의 경우 애초에 실행되지 않는다.
## continue, break
```
for (int i = 0; i < 100; i++) {
    if (i % 3 == 0) continue;
    if (i == 6) break;
    System.out.println(i);
}

1
2
4
5
6
```
`continue`는 한 루프만 건너 뛰고, `break`은 루프를 탈출한다.
## labeling
```
outer:
for (int i = 0; i < 10; i++) {

    inner:
    for (int j = 0; j < 10; j++) {
        if (j % 2 == 0) continue inner;
        if (i * j >= 30) continue outer;

        if (j > 8) break inner;
        if (i - j > 7) break outer;

        System.out.printf("i: %d, j: %d%n", i, j);
    }
}
```
`outer`와 `inner`는 해당 루프를 라벨링하는 것으로 `continue inner`는 `inner` 루프에 대해 한 루프 건너 뛰기를 `break outer`는 `outer` 루프를 탈출함을 의미한다.

보기 쉽게 명시하기 위해 사용한다.
## for each
`for each`는 변수를 사용하지 않는다는 점에서 `for`보다 사용이 권장된다.

`for each`는 배열이나 콜렉션에 주로 사용한다.
```
for (int num : multiOf4) { // multiOf4: [4, 8, 12]
    System.out.println(num);
}

4
8
12
```
`for(<변수> : <반복할 대상>) {<실행문>}`의 형식으로 사용한다.

위의 경우 `multiOf4` 배열의 요소를 `num`으로 받아서 실행문에서 출력하는 형태이다.
```
for (String s : "hello".split("")) {
    System.out.println(s);
}

h
e
l
l
o
```
문자열의 경우 `split`을 사용하여 요소별로 출력할 수 있다.
# while
```
int i = 1;
while (true) {
    int cur = i++;

    if (cur == 100) break;
    if (cur % 3 != 0) continue;

    System.out.println(cur);
}

3
6
9
...
```
`while (<조건>) {실행문}` 형식으로 사용한다.

`while`에서 `continue`를 사용하는 경우 `continue` 이하가 계속 생략되어 무한 루프에 빠지게 될 가능성이 있으므로 `break`을 통한 루프 탈출을 미리 지정하는 것이 예방하는 방법 중 하나이다.
## do while
```
int x = 10;

do {
    System.out.println(x++);
} while (x < 10);

int x = 10 -> 1
int x = 1 -> 1 2 3 4 5 6 7 8 9
```
`do {<실행문>} while (<조건>)` 형식으로 사용한다.

`do`의 실행문을 먼저 수행하고, `while`의 조건을 확인한 뒤, 조건을 만족하면 반복하는 방식이다.
