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
