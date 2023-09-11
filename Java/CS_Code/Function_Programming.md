# lambda
메소드를 식으로 표현하며, 익명 함수라고도 부른다.
## args: X, return: X
```
@FunctionalInterface
public interface Printer {
    void print ();

    //  void say (); // 메소드가 2개 이상이면 오류 발생
}
```
람다식 익명 클래스 생성을 위해서는 함수형 인터페이스인 FunctionalInterface를 사용한다.

기본적으로 해당 클래스를 객체로 사용하기 위해 메소드가 1대1일 대응이어야 하므로 해당 클래스 내에는 하나의 메소드만이 존재해야 한다.
```
public class Main {
    public static void main(String[] args) {
        // 기존 override 방식
        Printer printer1 = new Printer() {
            @Override
            public void print() {
                System.out.println("override");
            }
        };

                           // print 메소드에 인자가 없으므로 ()가 옴
        Printer printer2 = () -> {
            System.out.println("lambda1");
        };

        // 반환값이 없는 경우 {} 생략 가능
        Printer printer3 = () -> System.out.println("lambda2");

        // 반환 값이 업더라도 여러줄은 {} 사용
        Printer printer4 = () -> {
            System.out.println("{ lambda3");
            System.out.println("}");
        };

        for (var p : new Printer[] {printer1, printer2, printer3, printer4}) {
            p.print();
        }
    }
}

override
lambda1
lambda2
{ lambda3
}
```
## args: X, return: O
```
@FunctionalInterface
public interface Returner {
    Object returnObj ();
}
```
```
public class Main {
    public static void main(String[] args) {
        Returner returner1 = () -> {return 1;};
        Returner returner2 = () -> 1;

        var returned1 = returner1.returnObj();
        var returned2 = returner2.returnObj();

        System.out.println(returned1);
        System.out.println(returned2);
    }
}
```
반환하는 코드가 있는 경우 반환할 값만 입력해도 된다.
## args: O, return: O
```
public interface SingleParam {
    int func (int i);
}
```
```
public class Main {
    public static void main(String[] args) {
        SingleParam square = (i) -> i * i;
        SingleParam cube = i -> i * i * i;

        var squared = square.func(3);
        var cubed = cube.func(3);

        System.out.println(squared);
        System.out.println(cubed);
    }
}

9
27
```
인자가 하나만 존재하는 경우 ()는 생략해도 된다.
***
```
@FunctionalInterface
public interface DoubleParam {
    int func(int a, int b);
}
```
```
public class Main {
    public static void main(String[] args) {
        DoubleParam add = (a, b) -> a + b;
        DoubleParam multAndPrint = (a, b) -> {
            var result = a * b;
            System.out.printf("%d * %d = %d%n", a, b, result);
            return result;
        };

        var added = add.func(2, 3); // added: 5
        var multiplied = multAndPrint.func(2, 3);
    }
}

2 * 3 = 6
```
인자가 2개 이상이면 ()로 감싸야 한다.
## 예외
`java.util.Comparator` 는 함수형 인터페이스지만 추상 메소드가 2개인데, 이는 자바 8 이전에 만들어진 클래스이기 때문이다.

이 경우 사용자는 `equals`는 이미 `Object` 클래스에 있으므로 `compare` 메소드만 정의한다.
# java.util.function 패키지
람다를 사용하기 위해서는 인터페이스를 형식에 맞게 선언해야 했다.

이를 개선하기 위해 `java.util.function`에서 몇 가지 인터페이스를 제공한다.

|함수형 인터페이스|메소드|인자|반환 타입|
|----------------|-----|----|-----------|
|`Runnable`|`run`|||
|`Supplier<T>|`get`||`T`|
|`Consumer<T>`|`accept`|||
|`BiConsumer<T, U>`|`accept`|||
|`Function<T, R>`|`apply`|`T`|`R`|
|`BiFunction<T, U, R>`|`apply`|`T`,`U`|`R`|
|`Predicate<T>`|`test`|`T`|'boolean`|
|`BiPredicate<T, U>`|`test`|`T`,`U`|'boolean`|
|`UnaryOperator<T>`|`apply`|`T`|`T`|
|`BinaryOperator<T>`|`apply`|`T`,`T`|`T`|

## Runnable
```
public class Main {
    public static void main(String[] args) {
        Runnable dogButtonFunc = () -> System.out.println("dog");
        Runnable catButtonFunc = () -> System.out.println("cat");
        Runnable cowButtonFunc = () -> System.out.println("cow");

        dogButtonFunc.run();
        catButtonFunc.run();
        cowButtonFunc.run();
    }
}

dog
cat
cow
```
Runnable 인터페이스는 인자 반환값 없이 메소드를 실행하는 역할을 한다.
***
```
public class Button {
    private String text;
    public Button(String text) { this.text = text; }
    public String getText() { return text; }

    private Runnable onClickListener;
    public void setOnClickListener(Runnable onClickListener) {
        this.onClickListener = onClickListener;
    }
    public void onClick () {
        onClickListener.run();
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        Runnable dogButtonFunc = () -> System.out.println("dog"); // dog를 출력하는 Runnable 객체 생성
        Button dogButton = new Button("puppy");        // 이름이 dogButton Button 클래스 객체를 puppy인자를 주며 생성
        dogButton.setOnClickListener(dogButtonFunc);   // dogButton에 Runnable 객체를 전달
        dogButton.onClick();                           // Runnable 객체를 실행

        Button catButton = new Button("cat");
        catButton.setOnClickListener(() -> {
            System.out.println("cute" + catButton.getText()); // 람다 함수로 override
        });                                                   // 바꾼 코드 자체가 Runnable 객체임!
        catButton.onClick();                                  // Runnable 객체를 실행
    }
}

dog

cute cat
```
## Supplier
```
public class Main {
    public static void main(String[] args) {
        Supplier<String> appName = () -> "twice";
        Supplier<Double> rand0to10 = () -> Math.random() * 10;
        Supplier<Boolean> randTF = () -> Math.random() > 0.5;

        var supp1 = appName.get();    // supp1: "twice"
        var supp2 = rand0to10.get();  // supp2: 1.15
        var supp3 = randTF.get();     // supp3: true
    }
}
```
`Supplier`는 인자를 받지 않으며, `get()`메소드를 통해 값을 불러온다.

인자에 대한 자료형을 제네릭에 명시해야 한다.
## Consumer, BiConsumer
```
public class Main {
    public static void main(String[] args) {
        Runnable dogButtonFunc = () -> System.out.println("dog"); 
        Button dogButton = new Button("puppy");

        Consumer<Integer> sayOddEven = i -> System.out.printf( // sayOddEven은 integer값을 입력으로 사용
                "%d은 %c수입니다.%n", i, "짝홀".charAt(i % 2)
        );

        Consumer<Button> clickButton = b -> b.onClick();       // clickButton은 Button 클래스의 객체를 입력으로 사용

        BiConsumer<Button, Integer> clickButtonNTimes = (b, n) -> {
            for (var i = 0; i < n; i++) { b.onClick(); }
        };

        sayOddEven.accept(3); // 3은 홀수입니다.
        sayOddEven.accept(4); // 4은 짝수입니다.

        clickButton.accept(dogButton); // dog

        clickButtonNTimes.accept(dogButton, 5);
    }
}
```
`Consumer`와 `BiConsumer`는 각각 하나와 두개의 인자를 갖고, `accept()`메소드를 사용하며 반환하는 값은 없다.

인자에 대한 자료형을 제네릭에 명시해야 한다.
## Function, BiFunction
```
package sec09.chap02;

import sec07.chap04.*;

import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Function<Integer, Boolean> isOdd = i -> i % 2 == 1;       // 정수를 입력받아 boolean을 반환

        var isOdd3 = isOdd.apply(3);  // true
        var isOdd4 = isOdd.apply(4);  // false

        Function<String, Button> getButton = s -> new Button(s);  // 문자열을 입력받아 객체를 반환

        var goatButton = getButton.apply("goat");  // goatButton: text = "goat", onClickListener = null


        BiFunction<String, Runnable, Button> getButtonWFunc = (s, r) -> {
            var b = new Button(s);    // s라는 이름의 Button 객체 b를 생성
            b.setOnClickListener(r);  // 객체 b에 대해 setOnClickListener 메소드 실행
            return b;                 // 객체 b 반환
        };

         getButtonWFunc.apply("duck", () -> System.out.println("quak quak")) // 객체 b 생성
                       .onClick();                                           // b에 대해 onClick 메소드 실행
    }
}

quak quak
```
`Function`과 `BiFunction`은 각각 하나와 두개의 인자를 갖고, `apply()`메소드를 사용하며 반환하는 값이 존재한다.

인자와 반환값에 대한 자료형을 제네릭에 명시해야 한다.
## Predicate, BiPredicate
```
package sec09.chap02;

import sec07.chap04.*;

import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Predicate<Integer> isOddTester = i -> i % 2 == 1;                   // integer를 입력받고 boolean을 반환        

        var isOddT3 = isOddTester.test(3); // true
        var isOddT4 = isOddTester.test(4); // false

        Predicate<String> isAllLowerCase = s -> s.equals(s.toLowerCase());  // string을 입력받아 boolean을 반환

        var isAL1 = isAllLowerCase.test("Hello"); // false
        var isAL2 = isAllLowerCase.test("world"); // true

        BiPredicate<Character, Integer> areSameCharNum = (c, i) -> (int) c == i; // 문자열과 정수를 입력으로 받아 boolean을 반환

        var areSameCN1 = areSameCharNum.test('A', 64); // false
        var areSameCN2 = areSameCharNum.test('A', 65); // true
    }
}

```
`Predicate`과 `BiPredicate`은 각각 하나와 두개의 인자를 갖고, boolean을 반환한다. `test`메소드를 사용하여 실행한다.

인자에 대한 자료형을 제네릭에 명시해야 한다.
## UnaryOperator, BinaryOperator
```
package sec09.chap02;

import sec07.chap04.*;

import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        UnaryOperator<Integer> square = i -> i * i; // 인자와 반환값의 자료형이 동일

        var squared = square.apply(3); // squared: 9

        BinaryOperator<Double> addTwo = (i, j) -> i + j;

        var added = addTwo.apply(12.34, 23.45); // added: 35.79
    }
}

```
`UnaryOperator`과 `BinaryOperator`은 각각 하나와 두개의 인자를 갖고, boolean을 반환한다. `test`메소드를 사용하여 실행한다.

인자(들)에 대한 자료형과 반환값에 대한 자료형이 동일해야 한다.
# 메소드 참조
메소드를 어느 변수에 저장하거나 인자로 넣어줌을 의미한다.

람다식의 어떤 메소드 하나만 호출하는 경우 즉 해당 메소드가 인터페이스와 인자, 반환값 구성이 동일할 때 간단하게 만들 수 있다.
```
public class Main {
    public static void main(String[] args) {
        //  클래스의 클래스 메소드에 인자 적용하여 실행
        Function<Integer, String> intToStrLD = (i) -> String.valueOf(i);
        Function<Integer, String> intToStrMR = String::valueOf;           // 위 둘의 식은 동일함

        UnaryOperator<String> toLCaseLD = s -> s.toLowerCase();
        UnaryOperator<String> toLCaseMR = String::toLowerCase;            // 위 둘의 식은 동일함
    }
}
```
## 클래스 메소드 참조 - 생성자
```
public class Button {
    private String text;
    public Button(String text) { this.text = text; }
    public Button(String text, String sound) {
        this(text);
        onClickListener = () -> System.out.println(sound + " " + sound);
    }
    public String getText() { return text; }

    private Runnable onClickListener;
    public void setOnClickListener(Runnable onClickListener) {
        this.onClickListener = onClickListener;
    }
    public void onClick () {
        onClickListener.run();
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        //  클래스의 생성자 실행
        Function<String, Button> strToButtonLD = s -> new Button(s);
        Function<String, Button> strToButtonMR = Button::new; // 버튼 클래스 객체 생성
        Button button1 = strToButtonMR.apply("Dog"); // 인자가 1개이므로 `public Button(String text)` 생성자로 값이 넘어감
        System.out.println(button1.getText());
        // Dog

        BiFunction<String, String, Button> twoStrToButtonLD = (s1, s2) -> new Button(s1, s2);
        BiFunction<String, String, Button> twoStrToButtonMR = Button::new; // 버튼 클래스 객체 생성
        Button button2 = twoStrToButtonMR.apply("cute", "cat"); // 인자가 2개이므로 `public Button(String text, String sound)` 생성자로 값이 넘어감
        button2.onClick();
        // cat cat
    }
}
```
생성자를 실행하는 경우`::new`를 붙여 사용한다.
## 클래스 메소드 참조 - 메소드
```
public class Button {
    private String text;
    public Button(String text) { this.text = text; }
    public Button(String text, String sound) {
        this(text);
        onClickListener = () -> System.out.println(sound + " " + sound);
    }
    public String getText() { return text; }

    private Runnable onClickListener;
    public void setOnClickListener(Runnable onClickListener) {
        this.onClickListener = onClickListener;
    }
    public void onClick () {
        onClickListener.run();
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        BiFunction<String, String, Button> twoStrToButtonMR = Button::new; // 버튼 클래스 객체 생성
        Button button2 = twoStrToButtonMR.apply("cute", "cat");

        // 객체의 메소드 실행
        Runnable catCryLD = () -> button2.onClick();
        Runnable catCryMR = button2::onClick;
        catCryMR.run();
    }
}
```
객체에 대해 메소드를 참조하는 경우 `new`없이 `::<method>`를 사용한다.
# 스트림
스트림은 일련의 데이터를 연속적으로 가공하는데 유용하며
- 내부적으로 수행하여 중간 과정이 밖으로 드러나지 않고
- 배열, 콜렉션, I/O 등을 동일한 프로세스로 가공하고,
- 함수형 프로그래밍을 위한 다양한 기능을 제공하고,
- 가독성을 향상하고
- 원본을 수정하지 않는
특징이 있다.

멀티쓰레딩에서 병렬 처리도 가능하다.
## 스트림 생성
### 배열 - 참조형
```
public class Main {
    public static void main(String[] args) {
        Integer[] integerAry = {1, 2, 3, 4, 5};
        Stream<Integer> fromArray = Arrays.stream(integerAry);
        var fromArray_Arr = fromArray.toArray();

        var ifReuse = fromArray.toArray(); // 오류 발생
    }
}
```
참조형(Integer)으로 배열을 생성한 경우 스트림을 `Stream<type> <stream_name> = []`로 생성한다. 제네릭에 자료형이 들어가야 한다.

`fromArray.toArray()`는 스트림 결과를 보기 위한 메소드로, 스트림 과정을 확인할 수 없어서 추가하였다.

스트림은 한번 흐르면 끝이기 때문에 마지막 줄처럼 종료된 스트림을 다시 보려고 하면 오류가 발생한다.
### 배열 - 원시형
```
public class Main {
    public static void main(String[] args) {
        int[] intAry = {1, 2, 3, 4, 5};
        IntStream fromIntAry = Arrays.stream(intAry);
        var fromIntAry_Arr = fromIntAry.toArray();

        double[] dblAry = {1.1, 2.2, 3.3};
        DoubleStream fromDblAry = Arrays.stream(dblAry);
        var fromDblAry_Arr = fromDblAry.toArray();
    }
}
```
원시값을 배열로 생성한 경우 다른 클래스의 스트림을 사용한다.
### 직접 값 입력
```
public class Main {
    public static void main(String[] args) {
        IntStream withInts = IntStream.of(1, 2, 3, 4, 5);
        Stream<Integer> withIntegers = Stream.of(1, 2, 3, 4, 5);

        Stream<Unit> withUnits = Stream.of(
                new Swordman(Side.BLUE),
                new Knight(Side.BLUE),
                new MagicKnight(Side.BLUE)
        );
    }
}
```
원시형은 해당 자료형에 맞는 스트림 클래스를, 참조형은 `Stream<>`형식으로 스트림을 만드는 것은 동일하며, 이때 `of(<values>)`를 사용하여 직접 스트림에 값을 입력할 수 있다.
### 컬렉션 - list
```
public class Main {
    public static void main(String[] args) {
        Integer[] integerAry = {1, 2, 3, 4, 5};

        List<Integer> intAryList = new ArrayList<>(Arrays.asList(integerAry));
        Stream fromColl1 = intAryList.stream();
        var fromColl1_Arr = fromColl1.toArray();
    }
}
```
배열을 리스트로 바꾸고 `.stream()` 메소드를 사용하여 스트림을 생성할 수 있다.
### 컬렉션 - map
```
public class Main {
    public static void main(String[] args) {
        Map<String, Character> subjectGradeHM = new HashMap<>();
        subjectGradeHM.put("English", 'B');
        subjectGradeHM.put("Math", 'C');
        subjectGradeHM.put("Programming", 'A');
        var fromHashMap_Arr = subjectGradeHM.entrySet().stream().toArray();
    }
}
```
맵의 경우 해당 맵의 요소를 entrySet으로 만든 후 스트림을 생성할 수 있다.
### builder
```
public class Main {
    public static void main(String[] args) {
        Stream.Builder<Character> builder = Stream.builder();
        builder.accept('스');
        builder.accept('트');
        builder.accept('림');
        builder.accept('빌');
        builder.accept('더');
        Stream<Character> withBuilder = builder.build();
        var withBuilder_Arr = withBuilder.toArray();
    }
}
```
builder로 스트림을 생성하는 경우 우선 `Stream.Builder<Character> builder = Stream.builder();`를 사용하여 해당 자료형에 대한 builder를 준비한다.

이후 `accept` 메소드를 사용하여 값을 입력하고 `build()`메소드를 사용하여 최종적으로 스트림을 생성할 수 있다.
### concat
```
public class Main {
    public static void main(String[] args) {
        Stream<Integer> toConcat1 = Stream.of(11, 22, 33);
        Stream<Integer> toConcat2 = Stream.of(44, 55, 66);
        Stream<Integer> withConcatMethod = Stream.concat(toConcat1, toConcat2);
        var withConcatMethod_Arr = withConcatMethod.toArray(); // withConcatMethod_Arr: [11, 22, 33, 44, 55, 66]
    }
}
```
2개의 스트림을 순서대로 연결할 수 있다.
### 이터레이터
```
public class Main {
    public static void main(String[] args) {
        Stream<Integer> withIter1 = Stream
                .iterate(0, i -> i + 2)  // i가 0에서 시작해서 2씩 추가됨 i: 0, 2, 4, ...
                .limit(10);              // 10번만 반복
        var withIter1_Arr = withIter1.toArray(); // withIter1_Arr: [0, 2, 4, ..., 18]

        Stream<String> withIter2 = Stream
                .iterate("홀", s -> s + (s.endsWith("홀") ? "짝" : "홀")) // s가 홀로 시작해서 
                .limit(8);                                                  다음 문자에 따라 홀짝을 번갈아가며 사용
    }
}
```
`iterate`은 순회 조건을 의미한다.

`limit`은 반드시 필요하다. 없으면 오류 발생한다.
### 원시 자료형 스트림
```
public class Main {
    public static void main(String[] args) {
        IntStream fromRange1 = IntStream.range(10, 20);       // 20 미포함
        IntStream fromRange2 = IntStream.rangeClosed(10, 20); // 20 포함

        Stream<Integer> fromRangeBox = fromRange1.boxed();  // 원시형 -> 참조형
    }
}
```
원시 자료형의 경우 `range`를 사용할 수 있다.

원시 자료형에서 참조 자료형으로 변환하는 경우 `boxed()`메소드를 사용하여 변환할 수 있다.
### random 클래스
```
public class Main {
    public static void main(String[] args) {
        IntStream randomInts = new Random().ints(5, 0, 100); // 0에서 100까지의 정수중 5개를 선택

        DoubleStream randomDbls = new Random().doubles(5, 2, 3); // 2에서 3까지의 실수중 5개를 선택
    }
}
```
### 문자열
```
public class Main {
    public static void main(String[] args) {
        IntStream fromString = "Hello World".chars();
        var fromString_Arr = fromString.toArray(); // fromString_Arr: [72, 102, 108, ...]
    }
}
```
`chars()`메소드를 사용하여 각 문자별로 나누어 스트림을 생성한다.

생성된 스트림은 문자에 해당하는 정수값을 갖는다.
### 빈 스트림
```
public class Main {
    public static void main(String[] args) {
        Stream<Double> emptyDblStream = Stream.empty();
    }
}
```
`empty()`메소드를 사용하여 빈 스트림을 생성한다.

스트림을 받는 메소드에서 종종 사용한다.
# 스트림 연산

|연산|종류|설명|
|---|---|---|
|`peek`|중간|연산과정 중 스트림에 영향을 끼치지는 <br> 않으면서 주어진 Consumer 작업을 실행|
|`filter`|중간|주어진 Predicate에 충족하는 요소만 남김|
|`distinct`|중간|중복되지 않는 요소들의 스트림을 반환|
|`map`|중간|주어진 Function에 따라 각 요소들을 변경|
|`sorted`|중간|요소들을 정렬|
|`limit`|중간|주어진 수 만큼의 요소들로 스트림을 반환|
|`skip`|중간|앞에서 주어진 개수만큼 요소를 제거|
|`takeWhile`/`dropWhile`|중간|주어진 Predicate를 충족하는 동안 취하거나 건너뜀|
|`forEach`|최종|각 요소들에 주어진 Consumer를 실행|
|`count`|최종|요소들의 개수를 반환|
|`min`/`max`|최종|주어진 Comparator에 따라 최소/최대값을 반환|
|`reduce`|최종|주어진 초기값과 BinaryOperator로 <br> 값들을 하나의 값으로 접어 나감|

최종 연산을 사용하면 그 이후로는 중간 연산을 사용할 수 없다.
## 원시형의 자료형 변환
```
public class Main {
    public static void main(String[] args) {
        String str1 = "Hello World! Welcome to the world of Java~";

        var fromStr1 = str1.chars().boxed()
                .map(i -> String.valueOf((char) i.intValue())) // int 자료형을 char로 변환
                .map(String::toUpperCase)                      // 문자를 대문자로 변환
                .filter(s -> Character.isLetter(s.charAt(0)))  // 첫번째 문자(charAt(0))에 대해 문자가 맞다면(isLetter) 남기고 아니면 필터링
                .sorted()                                      // 정렬
                .distinct()                                    // 유일값만 남김
                .collect(Collectors.joining(", "));            // 문자를 ,로 구분하여 하나의 문자열로 만듦
        // fromStr1: "A, C, D, E, F, H, J, L, M, O, R, T, V, W"
    }
}
```
`chars()`메소드는 intstream을 반환한다. 문자열을 보기 위해서는 다시 자료형을 char로 바꾸어야 하는데, 원시 자료형의 경우 그것이 불가능하다.

따라서 `boxed`를 사용하여 참조형 stream으로 변환한 후에 진행하였다.
## 대표 연산
### filter, forEach
```
public class Main {
    public static void main(String[] args) {
        String str1 = "Hello World! Welcome to the world of Java~";
        str1.chars().sorted()
                    .distinct()
                    .filter(i -> (i >= 'A' && i <= 'Z') || (i >= 'a' && i <= 'z')) // 문자인 경우 데이터를 남김
                    //.filter(Character::isLetter) // 위와 동일한 효과
                    .forEach(i -> System.out.print((char) i));
    }
}

HJWacdefhlmortvw
```
`filter`는 해당 조건이 true이면 데이터를 남기고, false이면 필터링하여 제거한다.

`forEach`는 순회하는 값에 대해 메소드를 실행한다.
### peak
```
public class Main {
    public static void main(String[] args) {
        var oddSquaresR = IntStream.range(0, 10).boxed()
                .peek(i -> System.out.println("초기값: " + i))
                .filter(i -> i % 2 == 1)
                .peek(i -> System.out.println("홀수만: " + i))
                .map(i -> i * i)
                .peek(i -> System.out.println("제곱: " + i))
                .sorted((i1, i2) -> i1 < i2 ? 1 : -1)          // compare의 특성을 반대로 바꾸어 역순으로
                .peek(i -> System.out.println("역순: " + i))
                .map(String::valueOf)                          // char로 자료형 변환
                .collect(Collectors.joining(", "));            // 하나의 문자열로 변형
        // oddSquaresR: "81, 49, 25, 9, 1"
    }
}

초기값: 0
초기값: 1
홀수만: 1
제곱: 1
초기값: 2
초기값: 3
홀수만: 3
제곱: 9
...
```
`peak`은 방식 자체는 `forEach`와 동일하지만, `forEach`와 다르게 진행 중인 스트림에 영향을 주지 않는다.

출력에서 순회하면서 조건에 따른 값의 변화를 확인할 수 있지만 최종 스트림에는 홀수 제곱 역순의 문자열만이 존재한다.
