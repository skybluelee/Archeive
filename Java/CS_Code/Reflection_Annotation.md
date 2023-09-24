# Reflection
리플렉션은 런타임에서 클래스, 인터페이스, 메소드, 필드 등을 분석하고 조작할 수 있도록 만든다.

라이브러리나 프레임워크에서 많이 사용하며, 남용시 성능 저하, 보안 등의 문제가 발생할 수 있다.
## 리플렉션에 사용할 클래스
```
public class Button extends FormElement implements Clickable, Hoverable {
    public static int lastNo = 0;
    private int no = ++lastNo;
    private String name;
    private int spaces = 2;
    public boolean disabled = false;

    public Button() {
        name = "Default";
        spaces = 1;
    }
    public Button(String name, int spaces) {
        this.name = name;
        this.spaces = spaces;
    }

    public int getNo() { return no; }

    public String getName() { return name; }

    public int getSpaces() { return spaces; }

    public void onClick (boolean rightClick, int x, int y) {
        System.out.printf(
                "🖱️ %s (%d, %d)%n",
                (rightClick ? "우클릭" : "좌클릭"), x, y
        );
    }
}
```
## 클래스 가져오기
```
public class Main {
    public static void main(String[] args) {
        Class<Button> btnClass1 = Button.class;
        // Class<?> btnClass1_1 = Button.class;   // btnClass1과 동일

        Class<?> btnClass2 = Class.forName("sec13.chap01.ex01.Button");

        boolean areSame = btnClass1 == btnClass2; // areSame: true
```
클래스를 가져오는 경우 동일한 패키지에서 해당 클래스를 가져오며, 클래스 이름을 사용하는 경우와 경로를 사용하는 경우 2가지 방법이 존재한다.

위 방식으로 가져온 객체는 동일한 객체이다.
## 생성자 가져오기
```
        Constructor[] btn1Constrs = btnClass1.getConstructors();
        // btn1Constrs - "public sec13.chap01.ex01.Button()"
                       - "public sec13.chap01.ex01.Button(java.lang.String,int)"

        Constructor<?> btn1Constr = btnClass1.getConstructor(String.class, int.class);
        // "public sec13.chap01.ex01.Button(java.lang.String,int)"
```
`getConstructors`는 모든 생성자를 가져오기 때문에 배열로 생성하였고, `getConstructor`는 인자 타입에 일치하는 생성자만 가져온다.
배열에는 객체가 담긴다.

`getConstructors`는 생성자 `Button()`과 `Button(String name, int spaces)`를 가져왔고, `getConstructor`는 인자 타입이 일치하는 `Button(String name, int spaces)`를 가져왔다.
## 생성자 사용하기
```
        Button button1A = (Button) btn1Constr.newInstance("Enter", 3);
        // button1A: no = 1, name = "Enter", spaces = 3, disabled = false

        Button button1B = (Button)  btn1Constrs[0].newInstance();
        // button1B: no = 2, name = "Default", spaces = 2, disabled = false

        Button button1C = (Button)  btn1Constrs[1].newInstance("Tab", 2);
        // button1C: no = 3, name = "Tab", spaces = 2, disabled = false
```
가져온 생성자에 `newInstance` 메소드에 적절한 인자를 넣어 객체를 생성할 수 있다.

배열에 담긴 요소도 객체이므로 해당 알맞은 인자를 전달하여 객체를 생성할 수있다.
## 필드 가져오기
```
        Field[] btnFields = btnClass1.getDeclaredFields();
       // btnFields: - "public static int sec13.chap01.ex01.Button.lastNo"
                     - "private int sec13.chap01.ex01.Button.no"
                     - "private java.lang.String sec13.chap01.ex01.Button.name"
                     - "private int sec13.chap01.ex01.Button.spaces"
                     - "public boolean sec13.chap01.ex01.Button.disabled"

        for (var f : btnFields) {
            System.out.printf(
                    "변수명: %s\n타입: %s\n선언된 클래스: %s\n\n",
                    f.getName(),  // 필드 이름
                    f.getType(),  // 필드 타입
                    f.getDeclaringClass() // 선언된 클래스
            );
        }

변수명: lastNo
타입: int
선언된 클래스: class sec13.chap01.ex01.Button

변수명: no
타입: int
선언된 클래스: class sec13.chap01.ex01.Button

변수명: name
타입: class java.lang.String
선언된 클래스: class sec13.chap01.ex01.Button

변수명: spaces
타입: int
선언된 클래스: class sec13.chap01.ex01.Button

변수명: disabled
타입: boolean
선언된 클래스: class sec13.chap01.ex01.Button
```
`getDeclaredFields`의 경우 public, private 상관 없이 모든 필드를 가지고 온다.
```
        Field btn1Disabled = btnClass1.getField("disabled");
        // btn1Disabled: "public boolean sec13.chap01.ex01.Button.disabled"
```
`getField`의 경우 해당 필드를 가지고 온다. `getDeclaredFields`와 달리 public한 필드만 가지고 올 수 있다.
## 필드 값 확인, 변경하기
```
        Object button2 = btnClass2
                .getConstructor(String.class, int.class)
                .newInstance("Space", 5);

        Field btn2Disabled = btnClass2.getField("disabled");

        boolean btn2DisabledVal = (boolean) btn2Disabled.get(button2);
        // btn2DisabledVal: false

        btn2Disabled.set(button2, true);
        boolean btn2DisabledVal = (boolean) btn2Disabled.get(button2);
        // btn2DisabledVal: true
```
특정 필드를 얻는 객체에 리플렉션으로 생성한 객체를 인자로 지정하여 필드를 확인 및 변경할 수 있다.
## 메소드 가져오기
```
        Method[] btnMethods = btnClass1.getDeclaredMethods();
        // btnMethods: - "public void sec13.chap01.ex01.Button.onClick(boolean,int,int)"
                       - "public int sec13.chap01.ex01.Button.getNo()"
                       - "public int sec13.chap01.ex01.Button.getSpaces()"
                       - "public java.lang.String sec13.chap01.ex01.Button.getName()"

        for (var m : btnMethods) {
            System.out.printf(
                    "메소드명: %s\n인자 타입(들): %s\n반환 타입: %s\n\n",
                    m.getName(),
                    Arrays.stream(m.getParameterTypes())
                            .map(Class::getSimpleName)    // 클래스의 이름만 반환
                            .collect(Collectors.joining(", ")),
                    m.getReturnType()
            );
        }

메소드명: getName
인자 타입(들): 
반환 타입: class java.lang.String

메소드명: onClick
인자 타입(들): boolean, int, int
반환 타입: void

메소드명: getSpaces
인자 타입(들): 
반환 타입: int

메소드명: getNo
인자 타입(들): 
반환 타입: int
```
`getDeclaredMethods`를 사용하여 모든 메소드를 불러올 수 있다.
## 메소드 사용하기
```
        Method btn2onclick = btnClass2.getMethod("onClick", boolean.class, int.class, int.class);
        btn2onclick.invoke(button2, false, 123, 455);
```
리플렉션으로 생성한 객체에 `getMethod`에 메소드 이름과, 타입을 인자로 지정하여 원하는 메소드를 불러올 수 있다.
## Modifier
Modifier는 리플렉션으로 생성한 객체에 대한 특성을 확인하는 데에 사용한다.
```
        for (var f : objClass.getDeclaredFields()) {
            if (Modifier.isStatic(f.getModifiers())) continue;

            f.setAccessible(true);
            try {

            } catch (IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }
```
위 코드에서는 `isStatic` 메소드를 사용하여 해당 필드가 static이면 생략하는 역할을 한다.

이 외에 `isPublic`, `isSynchronized`, `isTransient` 등의 메소드가 존재한다.
# Annotation
어노테이션은 코드에 메타 데이터(데이터에 대한 정보를 나타내는 데이터)를 추가하는 작업이다. 컴파일 또는 런타임 시에 사용할 수 있다.

주로 리텐션과 함께 사용된다.
## 예시

|어노테이션|설명|
|----------|----|
|`@Deprecated`|더 이상 사용되지 않음|
|`@Override`|오버라이드되는 메소드|
|`@FunctionalInterface`|함수형 인터페이스|
|`@SuppressWarnings`|컴파일러의 경고 무시|

***
```
public class Main {
    public static void main(String[] args) {
        deprecatedMethod();
    }

    @Deprecated
    public static void deprecatedMethod() {}

    @SuppressWarnings("unchecked")
    public static void warnedMethod () {
        ArrayList list = new ArrayList();
        list.add("ㅁㅁㅁ"); // warning
    }
}
```
deprecated한 메소드를 사용하는 경우 _`deprecatedMethod()`_ 기울어진 상태로 표기된다.

SuppressWarnings를 사용하는 경우 warning 즉 노란 줄이 사라진다.
## 메타 어노테이션
사용자 정의 어노테이션의 속성들을 정의하는 어노테이션이다.
### SOURCE, CLASS, RUNTIME
```
@Retention(RetentionPolicy.SOURCE)
// .SOURCE, .CLASS, .RUNTIME 3가지 버전이 존재
public @interface Retention_range { }

public class MyClass {
    @RetSource
    int retSource;

    @RetClass
    int retClass;

    @RetRuntime
    int retRuntime;

    public static void main(String[] args) throws ClassNotFoundException {
        Class<?> myClass = Class.forName("sec13.chap02.MyClass");
}

```
어노테이션 범위는 `Retention`, `RetentionPolicy` 메소드를 사용하여 지정한다.

`SOURCE`의 경우 소스 파일에만 적용하므로 다른 클래스 파일에서 해당 필드를 가져오는 경우 리텐션이 적용되지 않는다.

`CLASS`의 경우 컴파일 과정까지는 사용된다.

`RUNTIME`의 경우 컴파일과 실행중에 사용 가능하다. 따라서 리플렉션을 사용하고자 한다면 RUNTIME으로 지정해야 한다.
### @Target
```
@Target(ElementType.ANNOTATION_TYPE)
public @interface TargAnnot { }
```
`ElementType` 메소드를 사용하여 어노테이션이 적용될 수 있는 대상 지정한다. 종류는 아래와 같다.

- `ANNOTATION_TYPE` : 다른 어노테이션
- `CONSTRUCTOR` : 생성자
- `FIELD` : 필드
- `LOCAL_VARIABLE` : 지역 변수
- `METHOD` : 메소드
- `PACKAGE` : 패키지
- `PARAMETER` : 매개변수
- `TYPE` : 클래스, 인터페이스, enum 등의 타입

```
@TargAnnot // 다른 어노테이션을 지정
@Target(ElementType.CONSTRUCTOR)
public @interface TargConstr {
}

//@TargConstr // 생성자와 필드는 다름
@Target(ElementType.FIELD)
public @interface TargField { }

@Target({
        ElementType.FIELD,
        ElementType.METHOD,
        ElementType.LOCAL_VARIABLE
})
public @interface TargMulti { }
```
`@TargAnnot`의 경우 다른 어노테이션을 지정하므로 `@Target`에 대해 전부 지정할 수 있다.

Target에 따라 사용할 수 있는 지정자가 다르기 때문에 위와 같이 필드에 생성자를 타겟으로 설정하면 오류가 발생한다.

`TargMulti`와 같이 한번에 여러 종류의 필드, 메소드 등을 타겟팅할 수 있다.
```
public class MyClass {
    @TargConstr
    public MyClass() { }

    @TargField
    @TargMulti
    //@TargConstr 필드에 생성자 타겟 불가
    int targField;

    @TargMulti
    public void targMethod () {}

    public static void main(String[] args) throws ClassNotFoundException {}
```
### @Inherited
부모 클래스에서 어노테이션을 지정한 경우 자식 클래스에서도 물려 받을 것인지를 결정한다.
```
@Retention(RetentionPolicy.RUNTIME)
public @interface InheritF { }

@Inherited // 부모로 부터 물려받음
@Retention(RetentionPolicy.RUNTIME)
public @interface InheritT { }
```
```
@InheritF
@InheritT
public class MyClass {
    public static void main(String[] args) throws ClassNotFoundException {}
}
```
메인 클래스에서 사용하는 경우 위와 같이 해당 클래스 이전에 설정한다.
### @Repeatable
반복 사용을 가능하게 만들어준다.
```
@Repeatable(Repeats.class)
@Retention(RetentionPolicy.RUNTIME)
public @interface RepeatT {
    int a();
    int b();
}

@Retention(RetentionPolicy.RUNTIME)
public @interface Repeats {
    RepeatT[] value();
}
```
반복을 직접 실행하는 인터페이스 이름을 반복 메소드에 `Repeatable`로 지정하고, 반복 지정 메소드의 인터페이스 이름을 반복을 직접 실행하는 인터페이스 내부에 지정한다.
```
@Retention(RetentionPolicy.RUNTIME)
public @interface RepeatF {
    int a();
    int b();
}

public class MyClass {
    public static void main(String[] args) throws ClassNotFoundException {
        @RepeatF(a = 1, b = 2)
        //@RepeatF(a = 3, b = 4) // 반복 불가

        @RepeatT(a = 1, b = 2)
        @RepeatT(a = 3, b = 4)
        @RepeatT(a = 5, b = 6)
    }
}
```
두 Repeatable 인터페이스 연계 없이 단독으로 지정한 경우 반복이 불가능하다.
## 어노테이션 만들기
### 값 설정 - 단일 값
```
@Retention(RetentionPolicy.RUNTIME)
public @interface Count {
    // int value();        // 기본값이 없을 때
    int value() default 1; // 기본값 설정
}
```
어노테이션에서는 필드를 메소드처럼 생성한다.

필드 이름은 보통 `value`로 설정한다.
```
public class Main {
    //  <필드명> = <값>
    @Count(value = 3)
    private int apples;
    // apple의 값이 3

    // default(기본 값) 설정시 값 지정 필요 없음
    @Count
    private int bananas;
    // bananas의 값이 1

    // 필드가 하나고 필드명이 value일 시
    // 값만 넣을 수 있음
    @Count(5)
    private int cacaos;
}
```
### 값 설정 - 복수 값
```
@Retention(RetentionPolicy.RUNTIME)
public @interface PersonName {
    String first();
    String last();
}
```
필드 생성 방식은 단일 값과 동일하다.
```
public class Main {
    // <필드명> = <값>
    // 인자 순서는 바뀌어도 상관 없음
    @PersonName(last = "홍", first = "길동")
    private Object seller;
}
```
### 어노테이션 사용
어노테이션에서 다른 어노테이션을 사용할 수 있다.
```
@PersonInfo(
        personName = @PersonName(last = "전", first = "우치"),
        age = 30,
        married = true
)
private Object sellerInfo;
```
`PersonName` 어노테이션의 이름 정보에 나이와 혼인 여부 필드를 추가하여 지정하였다.
### 값 설정 - 배열 
```
@Retention(RetentionPolicy.RUNTIME)
public @interface LocsAvail {
    String[] visit();
    String[] delivery();
    String[] quick();
}
```
```
public class Main {
    @LocsAvail(
            quick = {"서울", "대전", "강원"}, // {} 안에 작성
            visit = "판교",                  // 하나만 있을 시 {} 생략 가능
            delivery = {}                    // 요소가 없을 시 {} 필요
    )
    private Object store;
}  
```
### 어노테이션을 활용한 검증 시스템
```
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Blind { }

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MaxLength {
    int value() default 10;
}

@Target(ElementType.FIELD)
@Repeatable(NumLimits.class)
@Retention(RetentionPolicy.RUNTIME)
public @interface NumLimit {
    LimitType type();
    int to();
}
```
```
public class Introduction {
    @Blind
    @MaxLength(4)
    private String name;

    @NumLimit(type = LimitType.MIN, to = 1)
    private int age;

    @MaxLength
    private String job;

    @MaxLength(50)
    private String description;

    public Introduction(String name, int age, String job, String description) {
        this.name = name;
        this.age = age;
        this.job = job;
        this.description = description;
    }
}

public class Main {
    public static void main(String[] args) throws IllegalAccessException {
        List<Object> objList = new ArrayList<>();
        // 객체 생성
        Object[] objsToVerify = {
                new Introduction(
                        "홍길동", 28, "프로그래머",
                        "외길인생 자바 프로그래머입니다.")};

        var obj = objsToVerify[0];
        Class<?> objClass = obj.getClass();   // objClass: "class sec13.chap03.ex02.Introduction"

        for (var f : objClass.getDeclaredFields()) {.
            // f: "private java.lang.String sec13.chap03.ex02.Introduction.name"
            // f: "private int sec13.chap03.ex02.Introduction.28"
            // f: "private java.lang.String sec13.chap03.ex02.Introduction.job"
            // f: "private java.lang.String sec13.chap03.ex02.Introduction.description"

            f.setAccessible(true);

            Object val = f.get(obj);

            // 필드의 어노테이션 검증 및 처리
            for (var a : f.getAnnotations()) {
                if (a instanceof Blind) {
                    var s = (String) val;
                    f.set(obj, s.substring(0, 1) + "*".repeat(s.length() - 1));
                    // f: name = "홍**"
                }

                //  최대 길이 검증
                 if (a instanceof MaxLength) {
                    int maxLen = ((MaxLength) a).value();
                    // name의 경우 -> maxLen: 4
                    if (((String) val).length() > maxLen) {
                        System.out.println("%s 최대 길이(%d) 초과".formatted(f.getName(), maxLen));
                    }
                }

                if (a instanceof NumLimit) {
                    try {
                        verifyNumLimit(f.getName(), (NumLimit) a, (int) val);
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                }
            }
        }
}
```
#### 객체 생성 및 검증
```
new Introduction("홍길동", 28, "프로그래머","외길인생 자바 프로그래머입니다.")};
```
으로 `Introduction` 클래스를 사용하여 객체를 생성한다.

이때 `Introduction` 클래스는 인자를 어노테이션을 사용하여 초기화하고 생성자를 지정하였다. 이후 검증 과정이 진행된다.

`getClass` 메소드를 통해 해당 클래스 객체를 얻고, `getDeclaredFields` 메소드를 통해 객체의 필드 name, age, job, description을 순회한다.

`getAnnotations` 메소드를 통해 해당 필드의 어노테이션을 확인하며 검증이 시작된다.
#### name
name 필드의 경우 `Blind`, `MaxLength(4)`를 어노테이션으로 지정되어 있다.

`Blind` 어노테이션의 경우 메소드가 없으므로 if 문 내의 코드를 실행한다.

`MaxLength(4)` 어노테이션의 경우 기본값이 10이지만, `Introduction` 클래스에서 값을 4로 지정하였기 때문에 `maxLen`의 값은 4이다.

이후 if 문이 문제없이 진행된다.
#### age
age 필드의 경우 `NumLimit`이 어노테이션으로 지정되어 있다.

`type`은 MIN 값이고(MIN은 열거형 값 중 하나), `to`에 1의 값이 전달된 채로 if 문 코드를 실행한다.
#### job
job 필드의 경우 `MaxLength`가 어노테이션으로 지정되어 있다.

값을 지정하지 않았으므로 `maxLen`의 값은 기본값인 10이므로 어떤 일도 일어나지 않는다.
#### description
job 필드의 경우 `MaxLength`가 어노테이션으로 지정되어 있다.

`MaxLength(50)` 어노테이션은 값이 50로 지정하였기 때문에 `maxLen`의 값은 50이다.

이후 if 문이 문제없이 진행된다.
# ClassLoader
```
ClassLoader loader1 = Main.class.getClassLoader();
ClassLoader loader2 = Thread.currentThread().getContextClassLoader();
ClassLoader loader3 = ClassLoader.getSystemClassLoader();
// (loader1 == loader2 == loader3): true

Class<?> noUseCls1 = NoUse.class;
Class<?> noUseCls2 = Class.forName("sec13.chap04.ex02.NoUse");
Class<?> noUseCls3 = loader1.loadClass("sec13.chap04.ex02.NoUse");
// (noUseCls1 == noUseCls2 == noUseCls3): true
```
ClassLoader 클래스는 동적 클래스 로딩 및 클래스 로딩 관련 커스터마이징에 사용된다.

위의 3줄은 클래스 로더를 사용하여 동일한 객체를 가져오고,

아래의 3줄은 클래스 로더를 사용하여 동일한 클래스를 가져온다.
## 클래스로더를 사용한 어노테이션
```
public class Main {
    public static void main(String[] args) {
        String packageName = Main.class.getPackageName(); // packageName: "sec13.chap04.ex03"
        // 현재 클래스의 패키지 위치를 알려줌

        List<Class<?>> classes = getClasses(packageName); // classes: size = 9
        // classes에는 메인 클래스에 있는 모든 클래스가 담겨있음

        List<Object> characters = classes.stream()
                                         .filter(c -> c.isAnnotationPresent(Character.class))
                                         .map(c -> { ... } )

    }

    public static List<Class<?>> getClasses(String packageName) {
        List<Class<?>> classes = new ArrayList<>();
        ClassLoader classLoader = Thread.currentThread().getContextClassLoader();

        //  패키지 이름을 경로 형식으로 변환
        String path = packageName.replace('.', '/');

        //  ClassLoader의 기능으로 경로에 해당하는 URL을 가져옴
        java.net.URL resource = classLoader.getResource(path);

        String filePath = resource.getFile();

        filePath = java.net.URLDecoder.decode(filePath, StandardCharsets.UTF_8);

        java.io.File file = new java.io.File(filePath);
        if (file.isDirectory()) {
            for (String fileName : file.list()) {
                if (fileName.endsWith(".class")) {

                    // 끝의 .class을 잘라내어 클래스명을 가져옴
                    String className = packageName
                            + '.' + fileName
                            .substring(0, fileName.length() - 6);

                    // 클래스명으로 Class 객체 가져옴
                    Class<?> cls = null;
                    try {
                        cls = Class.forName(className);
                    } catch (ClassNotFoundException e) {
                        throw new RuntimeException(e);
                    }
                    classes.add(cls);
                }
            }
        } 
        return classes;
    }
}
```
클래스로더를 사용하는 `getClasses` 메소드를 통해 해당 디렉토리의 모든 클래스를 배열에 담을 수 있다.

클래스 배열을 스트림으로 바꾸고 윗 단계처럼 순회하며 어노테이션을 확인하며 검증 작업을 진행할 수 있다.
