# getMessage, printStackTrace
```
public class Main {
    public static void main(String[] args) {
        int[] ints = {1, 2, 3};
        try {
            System.out.println(ints[3]);
        } catch (Exception e) {
            String errMsg = e.getMessage(); // errMsg: Index 3 out of bounds for length 3
            e.printStackTrace(); // e: java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
        }
    }
}
```
`getMessage`메소드는 는 예외 상황에 대한 간략 정보를 문자열로 반환한다.

`printStackTrace`메소드는 에러의 종류, 발생위치, 호출 스택을 출력한다.
# try, catch, finally, exception
```
public class Main {
    public static void main(String[] args) {
        IntStream.rangeClosed(0, 4).forEach(Main::withFinally);
        // withFinally 메소드에 0~3까지 값 입력
    }

    public static void withFinally (int i) {
        try {
            switch (i) {
                case 1: System.out.println((new int[1])[1]);
                case 2: System.out.println("abc".charAt(3));
                case 3: System.out.println((Knight) new Swordman(Side.RED));
                case 4: System.out.println(((String) null).length());
            }

        } catch (ArrayIndexOutOfBoundsException | StringIndexOutOfBoundsException e) {
            System.out.printf("%d : BoundsException%n", i);
        } catch (ClassCastException e) {
            System.out.printf("%d : ClassException%n", i);
        } catch (Exception e) {
            System.out.printf("%d : Exception%n", i);
        } finally {
            System.out.println("final");
        }
    }
}
```
`catch` 조건에 다양한 오류 조건을 넣고자 한다면 `|`를 사용하여 OR 연산을 할 수 있다.

`finally`은 `try` 혹은 `catch` 이후에 반드시 실행된다. 위의 경우에는 `catch` 이후에 `finally`없이 출력이 가능하지만,
```
		public static char withFinally2 (int index) {
        String str = "Hello";
        try {
            char result = str.charAt(index);
            return result;
        } catch (Exception e) {
            return '!';
        } finally {
            System.out.println("final");
        }
    }
```
위와 같이 반환값이 존재하는 메소드의 경우 `return`이 동작하는 순간 메소드가 끝나기 때문에 `finally`를 사용해야만 원하는 값을 얻을 수 있다.
# 예외 정의
## RuntimeException
```
public class Main {
    public static void main(String[] args) {
        throw new RuntimeException();

        throw new RuntimeException("error!");


        throw new RuntimeException("원인: ",
                new IOException(
                        new NullPointerException()
                )
        );
    }
}
```
`throw new RuntimeException()`는 강제로 오류를 발생시킨다. 문자열을 인자로 넣을 수 있으며, 인자를 넣으면 해당 값을 오류가 발생한 터미널에서 확인할 수 있다.

`RuntimeException()` 인자에 새로운 오류를 집어 넣어 어떤 것이 원인인지 지정할 수 있다.
## 오류 넘어가기
```
package sec10.chap03;

import java.io.*;

public class Main2 {
    public static void main(String[] args) {
        try {
            registerDutyMonth("ㅁㅁㅁ", 13);
        } catch (Exception e) {}
    }
}
```
`catch` 이후에 실행할 코드를 남기지 않으면 오류시 아무 일도 일어나지 않는다.
## 커스터마이징
```
public class WrongMonthException extends RuntimeException {
    public WrongMonthException(int month) {
        // super는 RuntimeException의 생성자
        super(
                ("%d월은 존재하지 않습니다").formatted(month)
        );
    }
}
```
```
public class Main3 {
    public static void main(String[] args) {
        try {
            registerDutyMonth("lee", 13);
        } catch (WrongMonthException we) {
            we.printStackTrace();
        }
    }

    public static void registerDutyMonth (String name, int month) {
        if (month < 1 || month > 12) {
            throw new WrongMonthException(month);
        }
        System.out.printf("%s 신청 완료: %d월");
    }
}

sec10.chap03.WrongMonthException: 13월은 존재하지 않습니다
```
# 예외 떠넘기기, 예외 되던지기
```
public class Main {
    public static void main(String[] args) {
        
    }

    public static void maybeException () {
        if (new Random().nextBoolean()) {      // 임의의 bool값이 true면 오류 발생
            throw new FileNotFoundException();
        }
    }
}
```
maybeException 메소드의 경우 코드의 완성도와 상관없이 오류가 발생할 수 있다.

이러한 경우 컴파일이 진행되지 않는다.
## throws exception
```
public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        maybeException();
    }

    public static void maybeException () throws FileNotFoundException {
        if (new Random().nextBoolean()) {
            throw new FileNotFoundException();
        }
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        try {
            maybeException();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public static void maybeException () throws FileNotFoundException {
        if (new Random().nextBoolean()) {
            throw new FileNotFoundException();
        }
    }
}
```
첫번째 해결책은 오류 메소드에 `throws FileNotFoundException`를 사용하는 것이다. 이는 예외 발생시 자바가 책임을 지지 않는다고 해석하면 된다.

이 방식을 사용하는 경우 메인 메소드에도 `throws FileNotFoundException`를 사용하거나, 오류 메소드를 `try catch`문으로 감싸야 한다.
## try catch
```
public class Main {
    public static void main(String[] args) {
        maybeException();
    }

    public static void maybeException () {
        if (new Random().nextBoolean()) {
            try {
                throw new FileNotFoundException();
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```
오류 메소드를 `try catch`로 감싸면 메인 메소드에 바로 사용할 수 있다.
## 예외 떠넘기기, 예외 되던지기 - 상세
```
public class WrongMonthException extends Exception {
    public WrongMonthException(String message) {
        super(message);
    }

    public WrongMonthException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        try {
            registerDutyMonth("lee", 13);
        } catch (WrongMonthException we) {
            we.printStackTrace();
        }
    }

    public static void registerDutyMonth (String name, int month) {
        if (month < 1 || month > 12) {
            throw new WrongMonthException(month);
        }
        System.out.printf("%s 신청 완료: %d월", name, month);
    }
}
```
예외 떠넘기기는 오류 발생시 해당 오류에 대한 설명을 하고 끝난다.
***
```
public class WrongMonthException extends Exception {
    public WrongMonthException(String message) {
        super(message);
    }

    public WrongMonthException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        try {
            registerDutyMonthSafer("lee", 13);
        } catch (WrongMonthException we) {
            we.printStackTrace();
        }
    }

    public static void registerDutyMonthSafer (String name, int month) throws WrongMonthException {
        try {
            if (month < 1 || month > 12) {
                throw new WrongMonthException(
                        "wrong month"
                );
            }
            System.out.printf("%s 신청 완료: %d월.%n", name, month);
        } catch (WrongMonthException we) { // 오류 객체 we 생성
            System.out.printf(
                    "%s 임의 신청 완료: %d월.%n",
                    name, new Random().nextInt(1, 12 + 1)
            );
            throw we; // 적절한 처리 후 객체 we 반환
        }
    }
}
```
예외 되던지기는 오류가 발생한 경우 자동 처리함을 의미한다.
## 예외의 버블링
하위 메소드에서 처리하지 못한 예외를 상위 메소드에서 처리하는 방식이다.
```
public class Main3 {
    public static void main(String[] args) {
        IntStream.rangeClosed(0, 3)
                .forEach(Main3::large);
    }

    public static void small (int i) throws LargeException, MediumException {
        try {
            switch (i) {
                case 1: throw new SmallException();
                case 2: throw new MediumException();
                case 3: throw new LargeException();
                default:
                    System.out.println("small issue1");
            }
        } catch (SmallException se) { // SmallException 클래스에서 se 객체 생성
            System.out.println(se.getMessage() + ": small issue2");
        } catch (Exception e) {
            throw e;
        }
    }

    public static void medium (int i) throws LargeException {
        try {
            small(i);
        } catch (MediumException me) { // MediumException 클래스에서 me 객체 생성
            System.out.println(me.getMessage() + ": medium issue");
        } catch (Exception e) {
            throw e;
        }
    }

    public static void large (int i) {
        try {
            medium(i);
        } catch (LargeException xe) { // LargeException 클래스에서 xe 개체 생성
            System.out.println(xe.getMessage() + ": large issue");
        }
    }
}
```
작동원리는 아래와 같다.
1. 가장 상위 메소드에 인자를 전달한다.
2. 상위 메소드 -> 하위 메소드로 순서대로 인자를 전달한다.
3. 하위 메소드는 받은 인자를 바탕으로 작업을 수행하거나 예외처리를 진행한다.
4. 예외처리를 진행하는 경우 하위 메소드는 경우에 따라 중간 메소드나 상위 메소드로 오류를 전송(throw)한다.
5. 해당 메소드에서 정해진 작업을 진행한다.
## 연결된 예외 (chained exception)
특정 예외가 발생할 때 이를 원인으로 하는 다른 예외를 던진다.
```
public class WrongMonthException extends Exception {
    public WrongMonthException(String message) {
        super(message);
    }

    public WrongMonthException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
```
public class Main4 {
    public static void main(String[] args) {
        Map<String, Integer> dutyRegMap = new HashMap<>();
        dutyRegMap.put("ㅁㅁㅁ", 8);

        dutyRegMap.forEach((name, month) -> {
            try {
                chooseDutyMonth(name, month);
            } catch (WrongMonthException we) {
                we.printStackTrace();
                System.out.printf("%s: 오류 발생%n", name);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    public static void chooseDutyMonth (String name, int index) throws WrongMonthException {
        int[] availables = {1, 3, 4, 7, 9, 12};

        try {
            int month = availables[index - 1];
            System.out.printf("%s: %d월%n", name, month);
        } catch (ArrayIndexOutOfBoundsException ae) {
            WrongMonthException we = new WrongMonthException(
                    "%d번은 없어요.".formatted(index)
            );

            we.initCause(ae); // 원인으로 ae 객체 즉 ArrayIndexOutOfBoundsException를 지목

            throw we;
        }
    }
}

...
Caused by: java.lang.ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 6
...
```
# try with resource
사용한 뒤 닫아주어야 하는 리소스를 `try`문을 사용하여 제어할 때 `finally`를 사용하여 리소스를 닫아야 했는데, 만약 실수로 닫지 않았다면
메모리를 계속해서 차지하고 있기 때문에 오류가 발생할 가능성이 있다.

이때 리소스를 닫는 행위 자체를 `try`문에서 실행한다면 위와 같은 오류를 방지할 수 있다.
```
public class Main {
    public static void main(String[] args) {
        var correctPath = "./src/sec09/chap04/turtle.txt";
        var wrongPath = "./src/sec09/chap04/rabbit.txt";

        openFile(correctPath);
        openFile(wrongPath);
    }

    public static void openFile1 (String path) {
        Scanner scanner = null;
        try {
            scanner = new Scanner(new File(path));
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } finally {
            System.out.println("close the scanner");  // 기존 방식: finally문에서 리소스를 닫음
            if (scanner != null) scanner.close();
        }
    }

    public static void openFile2 (String path) {
        try (Scanner scanner = new Scanner(new File(path))) {  // try with resource문을 사용한 방식
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.out.printf("%s no file!%n", path);
        }
    }
}
```
`try with resource`는
```
try (자원을 초기화하는 코드) {
    // 자원을 사용하는 코드
} catch (예외 타입) {
    // 예외 처리 코드
}
```
형식으로 이루어지며, 리소스를 초기화하는 코드에 scanner를 넣어 구현하였다.
# NPE, Optional
null값을 잘못 사용하면 NPE(NullPointerException)가 발생한다. 이를 방지하는 것인 Optional이다.

`Optional<T>`는 `null`일 수도 있는 `T` 타입의 값으로 `null` 일 수 있는 값을 보다 안전하고 간편하게 사용하기 위해 사용한다.
## Optional.of
```
Optional<String> catOpt = Optional.of("Cat");
```
`Optional.of`는 인자가 무조건 null이 아닐 때 사용한다. 인자에 null값이 들어오면 NPE가 발생한다.
## Optional.ofNullable
```
Optional<String> dogOpt = Optional.ofNullable("Dog"); // dogOpt: "Optional[Dog]"   - value = "Dog"
Optional<String> cowOpt = Optional.ofNullable(null);  // cowOpt: "Optional.empty"  - value = null
```
`Optional.ofNullable`은 인자에 null 값이 와도 오류가 발생하지 않는다.
## Optional.empty
```
Optional<String> henOpt = Optional.empty();
```
처음부터 null 값을 넣고자 한다면 `Optional.empty`를 사용한다.
## ifPresent, ifPresentOrElse
```
public class Main {
    public static void main(String[] args) {
        randomUnitOpts.stream()
                .forEach(opt -> {
                    opt.ifPresent(unit -> System.out.println(unit));

                    opt.ifPresentOrElse(
                          unit -> System.out.println(unit),       // consumer
                          () -> System.out.println("(no value)")  // runner
                    );

					opt.orElse("no value")  // runner
                    );
                });
    }
}
```
`ifPresent`는 consumer로 인자를 받아 실행한다. 위의 경우 optional에 값이 있다면 해당 메소드를 실행한다.

`ifPresentOrElse`는 인자를 2개 받는데, 첫번째 인자는 optional에 값이 있다면 인자가 존재하는 해당 메소드를 실행하고, 두번째 인자는 runner로 인자 없는 메소드를 실행한다.

`orElse`는 supplier로 값이 null인 경우 지정한 메소드를 반환한다.
## 스트림의 경우
```
public class Main {
    public static void main(String[] args) {
        List<Optional<Integer>> optInts = new ArrayList<>();
        IntStream.range(0, 20)
                .forEach(i -> {
                    optInts.add(Optional.ofNullable(
                            new Random().nextBoolean() ? i : null
                    ));
                });

        optInts.stream()
                .forEach(opt -> {
                    System.out.println(
                            opt.filter(i -> i % 2 == 1)            // 짝수라면
                               .map(i -> "%d 출력".formatted(i))   // 문자열을 출력
                               .orElse("(SKIP)")                   // (SKIP)-문자열을 println함
                    );
                });
    }
}

(SKIP)
(SKIP)
(SKIP)
(SKIP)
(SKIP)
(SKIP)
(SKIP)
7 출력
...
```
스트림에서 filter + Optional 메소드를 사용하는 경우 해당 값이 null일 때 값을 제거하는 것이 아닌 원하는 메소드를 실행한다.
## 메소드
- `isPresent()`
	- Optional에 값이 있다면(null이 아니면) true
- `isEmpty()`
	- Optional에 값이 null이면 true
- `get()`
	- Optional에 값이 있다면 리턴, 없다면 NPE 발생
- `orElse(<value>)`
	- Optional에 값이 있다면 리턴, 없다면 value 리턴
