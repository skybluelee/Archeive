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
