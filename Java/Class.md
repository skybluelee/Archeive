# Class
java의 클래스는 참조형으로 값을 변경하면 원래 객체의 값이 변경된다.
# 생성자, this
```
public class Market {
    int price;
    String type;

    // 생성자(constructor) : 인스턴스를 만드는 메소드
    // this : 생성될 인스턴스를 가리킴
    Market (int price, String type) {
        this.price = price;
        this.type = type;
    }

    String intro () {
        return "%s: %d원".formatted(this.type, this.price);
    }
}
```
Market 클래스: Market.java
```
public class Main {
    public static void main(String[] args) {
        Market musinsa = new Market(100000, "Hoodie");
        Market twoninecm = new Market(50000, "shirt");

        String[] intros = {musinsa.intro(), twoninecm.intro()};

        for (String info : intros) {
            System.out.println(info);
        }
    }
}
```
Main문
## 생성자
**생성자**의 경우 해당 Class와 동일한 이름으로 인스턴스를 생성하는 것을 말한다.

`Market` 클래스의 `Market (int price, String type)`이하를 생성자라고 한다.

생성자를 사용하는 경우 Main문에서 인스턴스 생성과 변수 전달을 동시에 진행할 수 있다.

생성자가 없는 경우 인스턴스를 생성하고 변수를 각각 전달해야 한다.
`musinsa.type = "Hoodie"; musinsa.price = 100000;`
생성자를 만들지 않은채 실행하더라도 java 내에서 생성자를 생성한다.
## this
**this**는 생성한 객체를 의미한다.
```
Market (int price, String type) {
        this.price = price;
        this.type = type;
    }
```
위 코드는 해당 인스턴스의 변수 `price, type`에 값을 넣는다.

사용 변수가 겹치는 경우 원하는 값이 제대로 들어가지 않는 경우가 있는데, `this`를 사용하여 해결할 수 있다.
# 다중 생성자
```
public class Main {
    public static void main(String[] args) {
        ChickenMenu[] menus = {
                new ChickenMenu("후라이드", 10000),
                new ChickenMenu("양념치킨", 12000),
                new ChickenMenu("화덕구이", 15000, "bake")
        };
        Chicken store1 = new Chicken(3, "판교", menus);

        ChickenMenu order1 = store1.orderMenu("양념치킨");
        ChickenMenu order2 = store1.orderMenu("오븐구이");
    }
}
```
```
public class ChickenMenu {                                    public class Chicken {
    String name;                                                  int no;
    int price;                                                    String name;
    String cook = "fry";                                          ChickenMenu[] menus;

    ChickenMenu (String name, int price) {
        this.name = name;                                         Chicken (int no, String name, ChickenMenu[] menus) {
        this.price = price;                                           this.no = no;
    }                                                                 this.name = name;
                                                                      this.menus = menus;
    ChickenMenu (String name, int price, String cook) {           }
        this.name = name;
        this.price = price;                                       ChickenMenu orderMenu (String name) {
        this.cook = cook;                                             for (ChickenMenu menu : menus) {
    }                                                                      if (menu.name.equals(name)) {
}                                                                              return menu;
                                                                           }
                                                                      }
                                                                      return null;
                                                              }
```
ChickenMenu 클래스의 경우 입력을 2개 받는 경우와 3개 받는 경우를 나누어 각각 생성자를 정의하였다. 동일한 클래스를 사용하는 각각의 객체가 생성된다.
# static
```
public class Chicken {                                        
    static String brand = "Min's Chicken";                        
    static String contact() {                                         
        return "%s에 오신걸 환영합니다.".formatted(brand);              
    }                                                                 
                                                                      
    String name;
    int price;                                                        
                                                                      
    Chicken(int price, String name){
        this.price = price;                                           
        this.name = name;                                             
    }                                                             
                                                             
    String menu() {
        return "%s에 오신걸 환영합니다. %s는 %d원 입니다.".formatted(brand, name, price);
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        String brand = Chicken.brand; // brand: Min's Chicken
        String contact = Chicken.contact(); // contact: Min's Chicken에 오신걸 환영합니다.
        
        // String main_name = Chicken.name; 오류 발생
        
        Chicken store = new Chicken(18000, "후라이드");
        String menu_intro = store.menu(); // menu_intro: Min's Chicken에 오신걸 환영합니다. 후라이드는 18000원 입니다.
        
        String store_brand = store.brand; // 자동 생성이 안됨
        String store_contact = store.contact(); // store_contact: Min's Chicken에 오신걸 환영합니다.
    }
}
```
`static`으로 생성한 변수는 메모리에 저장되어, 클래스로 생성된 객체가 해당 변수를 가져올 수 있다.

`static`으로 생성한 변수는 메인 메소드에서 가져올 수 있지만, 인스턴스 메소드 내의 변수는 가져올 수 없다.

`static`으로 생성한 변수를 객체를 통해서 가져올 수 있으나 권장되지는 않는다.
## static을 사용한 변수 이용
```
public class Chicken {

    static String brand = "Min's Chicken";
    static String contact () {
        return "%s입니다. 무엇을 도와드릴까요?".formatted(brand);
    }
    static int lastNo = 0;

    int no;
    //int no = ++lastNo; // 이렇게 해도 됨

    String name;

    YalcoChicken(String name) {
        no = ++lastNo;
        this.name = name;
    }

    String intro () {
        return "안녕하세요, %s %d호 %s호점입니다.".formatted(brand, no, name);
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        YalcoChicken store1 = new YalcoChicken("판교"); // store1: no = 1, name = "판교"
        YalcoChicken store2 = new YalcoChicken("강남"); // store2: no = 2, name = "강남"
        YalcoChicken store3 = new YalcoChicken("제주"); // store3: no = 3, name = "제주"
    }
}
```
`static`으로 생성한 변수를 디버깅되는 동안 모든 객체가 공유하는 점을 이용하여 각 객체에 다른 값을 넣을 수 있다.
# 접근 제어자
클래스 내에 많은 필드와 메소드가 존재하는데, 이를 전부 공개하는 것은 비효율적이다.

접근 제어자는 사용중 오용이나 혼란을 방지하기 위해 사용하며 이를 **캡슐화(encapsulation)** 라 한다.

이는 필드나 메소드를 감추기 위한 것이 아니라(코드로 확인 가능) 혼란을 방지하여 편의성을 제공하기 위해 사용한다.

|접근 권한|public|protected|default|private|
|------|------|-----|-----|----|
|해당 클래스 내부|O|O|O|O|
|동일 패키지 내부|O|O|O|X|
|동일 패키지 또는 <br> 자손 클래스 내부|O|O|X|X|
|다른 패키지 포함 <br> 모든 장소|O|X|X|X|

```
package sec05.chap03.ex02; // 동일 패키지 안에 존재

public class Button {
    private static String mode = "LIGHT";
    public static void switchMode () {
        mode = mode.equals("LIGHT") ? "DARK" : "LIGHT";
    }

    private char print;
    private int space = 1;

    public Button (char print, int space) {
        this.print = print;
        this.space = space;
    }

    public void setSpace (int space) {
        if (space < 1 || space > 4) return;
        this.space = space;
    }
    public String getButtonInfo () {
        return "%c 버튼, %d픽셀 차지"
                .formatted(print, space * 4096);
    }
}
```
```
package sec05.chap03.ex02; // 동일 패키지 안에 존재

public class Main {
    public static void main(String[] args) {
        Button button1 = new Button('1', 1);

        //Button.mode = "OCEAN"; // 오류 발생
        Button.switchMode();

        //button1.space = 3; // 오류 발생
        button1.setSpace(3);
        button1.setSpace(-1); // 걸러짐

        //char button1Print = button1.print; // 오류 발생
        String button1Info = button1.getButtonInfo();
    }
}
```
`Button.mode = "OCEAN";`: private으로 생성한 필드의 경우 접근이 불가능하다.

위의 경우와 같이 private한 필드에는 접근이 불가능하므로, 해당 필드를 수정하기 위해서는 private 필드를 변경하는 함수를 사용한다.

`setSpace` 메소드의 경우 `space`를 입력받아 해당 객체의 `space`를 수정한다.
## getter, setter
private한 필드를 변경하기 위해서는 해당 클래스에 필드를 변경하는 메소드를 생성해야 한다.

이 경우 IntelliJ 상태창 -> Code -> Generator -> Getter and Setter로 들어가면 private 필드에 대한 메소드를 자동으로 생성하는 기능이 있다.
# 상속
자손 클래스는 부모 클래스의 모든 필드와 메소드를 상속받는다.
```
public class Button {
    private String print;

    public Button(String print) {
        this.print = print;
    }

    public void func () {
        System.out.println(print);
    }
}
```
```
public class ShutDownButton extends Button { // Button 클래스를 상속함  public class ToggleButton extends Button {
    public ShutDownButton () {                                             private boolean on;
        super("ShutDown"); // 부모의 생성자 호출
    }                                                                      public ToggleButton(String print, boolean on) {
                                                                               super(print);
	@Override                                                                  this.on = on;
    public void func () {                                                  }
        System.out.println("프로그램 종료");
    }                                                                      @Override
}																		   public void func () {
																		   	   super.func();
																	       	   this.on = !this.on;
																		       System.out.println(
																		            "대문자입력: " + (this.on ? "ON" : "OFF"));
																		       }
																		  }
```
```
public class Main {
    public static void main(String[] args) {
		Button entrButton = new Button("Enter");
        ShutDownButton stdnButton = new ShutDownButton();
        ToggleButton tglButton = new ToggleButton("CapsLock", false);

        entrButton.func();

        System.out.println("\n- - - - -\n");

        stdnButton.func();

        System.out.println("\n- - - - -\n");

        tglButton.func();
        tglButton.func();
        tglButton.func();
    }
}
```
`extends Button`를 사용하여 부모 클래스의 모든 필드와 메소드를 상속받는다.

## `super`의 역할
- 생성자의 경우
	- 부모 클래스에 생성자가 존재하는 경우
 		- `super()`을 사용하여 작성한다.
   		- `super("ShutDown")`의 경우 `Button("ShutDown")`과 동일하다.
     - 부모 클래스에 생성자가 존재하지 않는 경우
     	- 자손 클래스에 `super`를 포함한 생성자를 정의할 필요 없다.
- 메소드의 경우
	- `super.`을 사용하여 부모 클래스의 메소드를 호출한다.
 	- `super.func()`의 경우 부모 클래스의 `func()`를 호출한다.
 
## `@Override`
부모 클래스의 메소드를 가져와서 덮어 쓴다.

부모 클래스의 메소드와 동일한 이름이어야 한다. 이름이 다른 경우 오류가 발생한다.

`@Override`로 정의한 메소드를 호출하면 부모 클래스의 메소드는 무시되고 Override한 메소드만 호출된다.
## 생성자
부모 클래스에 생성자를 정의했다면, 반드시 자손 클래스에도 `super`을 사용하여 생성자를 정의해야 한다.

만약 자손 클래스에 정의할 생성자가 존재하지 않더라도
```
public ShutDownButton(String print) {
	super(print);
}
```
와 같이 빈 생성자라도 만들어야 한다. 그렇지 않으면 오류가 발생한다.
# 다형성(Polymorphism)
**상속** 파트의 코드 참조
```
Button button1 = new Button("Enter");
Button button2 = new ShutDownButton();
Button button3 = new ToggleButton("CapsLock", true);

ShutDownButton button4 = new Button("Enter");
ToggleButton button5 = new ShutDownButton();
```
자식 클래스는 모두 부모 클래스에 속한다. 따라서 위의 3개의 코드는 부모 클래스 객체를 자손 클래스를 통해 생성한다.

반면 아래의 2개의 코드는 자손 클래스 객체를 부모 클래스를 통해 생성하거나, 상속 관계가 아닌 클래스를 통해 객체를 생성할 수 없다.

이처럼 특정 자료형의 자리에 여러 종류가 들어올 수 있는 것을 **다형성**이라고 한다.
## `instanceof`
`instanceof`는 뒤에 오는 클래스의 인스턴스인지를 확인한다.
```
Button button = new Button("버튼");
ToggleButton toggleButton = new ToggleButton("토글", true);
ShutDownButton shutDownButton = new ShutDownButton();

// true
boolean typeCheck1 = button instanceof Button;
boolean typeCheck2 = toggleButton instanceof Button;
boolean typeCheck3 = shutDownButton instanceof Button;

// false
boolean typeCheck4 = button instanceof ShutDownButton;
boolean typeCheck5 = button instanceof ToggleButton;

// 오류 발생
boolean typeCheck6 = toggleButton instanceof ShutDownButton;
boolean typeCheck7 = shutDownButton instanceof ToggleButton;
```
Button과 그 자손 클래스에서 생성한 객체를 Button과 비교하면 true를 반환하고, 반대의 경우 false를 반환한다.

상속 관계가 아닌 경우 오류가 발생한다.
***
```
Button[] buttons = {
		new Button("Space"),
		new ToggleButton("NumLock", false),
		new ShutDownButton()
};

for (Button btn : buttons) {
	if (btn instanceof ShutDownButton) continue; 
	btn.func();
}
```
다음과 같이 종속 여부를 파악하여 진행할 수 있다.
## object
모든 클래스의 부모 클래스이다.
```
Object obj1 = new Object();

Object obj2 = new YalcoChicken(3, "판교");
Object obj3 = new ShutDownButton();
```
우리가 생성한 클래스를 아무런 제약 없이 Object 클래스를 사용하여 생성할 수 있다.

Object가 아니고, 동일한 패키지 안에 없다면 해당 클래스가 있는 파일을 import해야 사용할 수 있다.
# final
`final`은 변경하지 못하게 만들어준다.
**필드**의 경우 변수를 선언과 동시에 초기화하거나 생성자에서 초기화한다.
```
private final int no;
또는
public Final_Class(int no) {
	this.no = no;
}
```
```
// 오류 발생
public void changeFinalFields () {
	this.no++;
}
```
이 경우 위와 같이 `final`로 생성한 변수를 바꾸려 하면 오류가 발생한다.
***
**메소드**의 경우 override가 불가능하게 된다.
```
public final void Final_Check () {
	System.out.println("This is final");
}
```
메소드를 부모 클래스가 가지고 있고
```
// 오류 발생
@override
public void Final_Check () {
	System.out.println("Not final");
}
```
자식 클래스가 위와 같이 부모 클래스의 메소드를 override하는 경우 오류가 발생한다.
***
**인스턴스**의 경우 다른 값을 넣지는 못하지만, 필드는 변경할 수 있다.
```
final Final_Class instance = new Final_Class(3, "aaa");

// 오류 발생
instance = new Final_Class(17, "bbb");
// 변경 가능
instance.name = "ccc";
```
***
**클래스**의 경우 자손 클래스를 만들 수 없다.
```
public final class Final_Class{
	...
}

// 오류 발생
public class add_class extends Final_Class {
}
```
`extends <final_class>` 과정에서 오류가 발생한다.
# 추상 클래스
스스로는 인스턴스를 만들 수 없으며, 관련 클래스의 공통 분모를 정의하기 위한 클래스이다.
**인스턴스**
```
public abstract class Kakao {
}

public class Main {
    public static void main(String[] args) {
        Kakao yalcoGroup = new Kakao(1, "서울"); // 오류 발생
}
```
추상 클래스로 객체를 생성하는 것은 불가능하다.
***
**메소드**
```
public abstract class Kakao {
	abstract static String getCreed (); // 오류 발생

    public abstract void takeOrder();
}

public class Cafe extends Kakao {
    @Override
    public void takeOrder () {
        System.out.printf("얄코카페 %s 음료를 주문해주세요.%n", super.intro());
        if (!isTakeout) System.out.println("매장에서 드시겠어요?");
    }
}
```
추상 클래스에서 클래스 메소드(`static`을 사용한 메소드)는 사용할 수 없다.

추상 클래스에서 정의한 메소드는 자식 클래스에서 정의해야 한다.

위와 같이 `takeOrder()` 메소드를 자식 클래스에서 정의해야 하며, 정의하지 않는 경우 오류가 발생한다. 
IntelliJ 상태창 -> Code -> Generator -> Implement Method를 클릭하면 부모 클래스로 부터 정의해야 하는 메소드를 알려준다.

추상 클래스에서의 메소드는 이미 역할이 지정되어 있어 접근 제어자(`public`)을 사용하지 않아도 정상적으로 작동한다.
***
**다형성**
추상 클래스의 자식들로 만든 객체를 추상 클래스를 통해 메소드 제어가 가능하다.
# 인터페이스
추상 클래스와 달리 종속되지 않고, 원하는 객체에 제한 없이 사용할 수 있다.
`public interface <interface_name>`형식으로 작성하며, interface를 class로 바꾸면 기존 class 파일로 변경된다.

```
public interface Hunter {
    String position = "hunter"; // 반드시 초기화
    void hunt (); // Hunter 인터페이스를 사용하는 경우 정의해야 함
}
```
인터페이스의 필드는 `public static final`이 디폴트로 정해져 있다. 또한 생성자가 존재하지 않아,
필드를 선언하는 동시에 반드시 초기화를 진행해야 한다.

메소드의 경우 `public abstract`가 디폴트로 정해져 있어 해당 인터페이스를 사용하는 경우 반드시 정의해야 한다.
***
```
public class PolarBear extends Mamal implements Hunter, Swimmer {
    public PolarBear() {
        super(false);
    }

    @Override
    public void hunt() {
        System.out.println(position + ": Coca Cola");
    }

    @Override
    public void swim() {
        System.out.println("swimming");
    }
}
```
`implements`를 사용하여 인터페이스를 사용하고, 여러 개의 인터페이스를 적용할 수 있다.

해당 인터페이스에서 메소드를 선언한 경우, 위와 같이 정의하지 않으면 오류가 발생한다.
## default
```
public interface food {
    static void announcement() {
        System.out.println("식품안전 관련 공지");
    }

    default void regularInspection () {
        System.out.println("정기 체크");
    }

    void cleanKitchen ();
}
```
`static`으로 생성한 메소드는 메인 메소드에서 바로 사용할 수 있다. 위의 경우 `food.announcement();`로 호출할 수 있다.

`default`를 사용하는 경우 일반적인 메소드와 달리 해당 인터페이스를 사용하는 클래스에서 `default` 메소드를 작성하지 않아도 된다.
# 싱글턴
객체지향언어에서 많이 사용하는 활용 방식 중 하나이다.

프로그램 상에서 특정 인스턴스가 하나만 있어야 할 때 사용한다.
```
public class Setting {
	private static Setting setting; // 클래스 필드로 설정

    private Setting () {} // 생성자를 private으로 설정

    public static Setting getInstance() {
        if (setting == null) {        // 객체가 존재하지 않는다면 
            setting = new Setting();  // 객체를 생성함
        }
        return setting;
    }
}
```
위와 같이 클래스(정적) 필드로 정의한다면 프로그램에서 메모리 하나만 존재하게 된다. 즉 모든 객체가 동일한 필드를 공유한다.
```
public class Tab {
    // 공유되는 유일한 인스턴스를 받아옴
    private Setting setting = Setting.getInstance();

    public Setting getSetting() {
        return setting;
    }
}

public class Main {
    public static void main(String[] args) {
		Tab tab1 = new Tab();
        Tab tab2 = new Tab();
        Tab tab3 = new Tab();
    }
}
```
Tab 클래스의 모든 독립된 객체는 동일한 필드를 사용한다.
# 패키지
자바 프로젝트의 디렉토리 역할을 수행한다.

클래스 명의 중복을 방지하기 위해 사용한다. 해당 클래스를 입력하면 동일한 클래스 이름이더라도 intelliJ에서 패키지 디렉토리를 알려주기 때문에
클래스를 정확하게 선택할 수 있다.

```
package sec06.chap02.pkg1;

public class Parent {   // 부모 클래스
    private int a = 1;
    int b = 2; // default
    protected int c = 3;
    public int d = 4;
}
```
```
package sec06.chap02.pkg1;				package sec06.chap02.pkg1;

// 자식 클래스							// 친구 클래스
public class Child extends Parent {     public class Friend {
    //  int aa = a; // 오류 발생				Parent parent = new Parent();	
    int bb = b;								//  int aa = new Parent().a; // ⚠️ 불가
    int cc = c;								int bb = parent.b;
    int dd = d;								int cc = parent.c;
}											int dd = parent.d;
										}
```
동일한 패키지의 자식 클래스의 경우 `private`을 제외한 접근 제어자로 선언된 필드는 바로 가져올 수 있다. 
단 `private`으로 선언된 필드를 상속받지 못하는 것이 아닌 변수로 가져오지 못하는 것을 의미한다.

동일한 패키지의 친구 클래스의 경우 필드를 상속받지 못하지만, 객체를 생성하여 `private`을 제외한 접근 제어자로 선언된 필드를 가져올 수 있다.
***
```
package sec06.chap02.pkg1;

public class Parent {   // 부모 클래스
    private int a = 1;
    int b = 2; // default
    protected int c = 3;
    public int d = 4;
}
```
```
package sec06.chap02.pkg2;				package sec06.chap02.pkg1;
import sec06.chap02.pkg1.Parent;
// 자식 클래스							// 친구 클래스
public class Child extends Parent {     public class Friend {
    //  int aa = a; // 오류 발생				Parent parent = new Parent();	
    int bb = b;								//  int aa = new Parent().a; // ⚠️ 불가
    int cc = c;								int bb = parent.b;
    int dd = d;								int cc = parent.c;
}											int dd = parent.d;
										}
```
자식 클래스가 패키지가 다른 부모로부터 상속받기 위해서는 `import`를 사용해야 한다.
***
```
import sec06.chap02.pkg3.*; // 와일드카드

public class Main {
    public static void main(String[] args) {
        Cls1 cls1 = new Cls1();
        Cls2 cls2 = new Cls2();
        Cls3 cls3 = new Cls3(); // pkg3의 클래스들

		
		// 패키지의 이름이 동일한 경우 
        sec06.chap02.pkg1.Child child1 = new sec06.chap02.pkg1.Child();
        sec06.chap02.pkg2.Child child2 = new sec06.chap02.pkg2.Child();

		System.out.println(child1.b); // sec06.chap02.pkg1의 Child 클래스의 변수를 받음
    }
}
```
특정 패키지에서 여러 클래스를 사용하기 위해서 `.*`을 사용할 수 있다. 이 방식을 와일드 카드라고 한다.

패키지의 이름이 동일한 경우 위와 같이 패키지 이름을 임의로 변경하여 사용할 수 있다.
# 내부 클래스
내부 클래스는 외부/내부 클래스간의 관계가 긴밀할 때 사용한다.

적절히 사용시 가독성을 높여주나, 과하게 사용하면 클래스가 비대화 되는 단점이 있다.
***
```
public class Outer {
    private String inst = "field";
    private static String sttc = "sttatic_field";
```
## 멤버 인스턴스
```
    // 멤버 인스턴스
	class InnerInstMember {
        private String name = inst + sttc;
        private InnerSttcMember innerSttcMember = new InnerSttcMember(); // static class

        public void func () {
            System.out.println(name);
        }
    }
```
멤버 인스턴스(일반적인 내부 클래스)의 경우 Outer 클래스의 일반 필드와 static 필드 모두 사용할 수 있다.

또한 정적 내부 클래스에 접근할 수 있다.
***
```
public class Main {
    public static void main(String[] args) {
        Outer.InnerInstMember innerInstMember = outer.getInnerInstMember();
        innerInstMember.func();
    }
}
```
멤버 인스턴스 클래스는 위와 같은 방식으로 객체를 생성할 수 있다.
## 정적 내부 클래스
```
	// static 클래스
	public static class InnerSttcMember {
        // private String name1 = inst; // 오류 발생
		private String name2 = sttc;

        // private InnerInstMember innerInstMember = new InnerInstMember(); // 오류 발생

        public void func () {
            // ⚠️ 인스턴스 메소드지만 클래스가 정적(클래스의)이므로 인스턴스 필드 접근 불가
            //  name += inst;
            System.out.println(name);
        }
    }
```
정적 내부 클래스의 경우 클래스에서 static으로 선언되지 않은 필드는 사용할 수 없다.

또한 멤버 인스턴스 클래스에 접근할 수 없다.
***
```
public class Main {
    public static void main(String[] args) {
        Outer.InnerSttcMember staticMember = new Outer.InnerSttcMember();
        staticMember.func();
    }
}
```
정적 내부 클래스는 위와 같은 방식으로 객체를 생성할 수 있다.
## 메소드 안에 정의된 클래스
```
	public void memberFunc () {
        class MethodMember {
            String instSttc = inst + " " + sttc;
            InnerInstMember innerInstMember = new InnerInstMember();
            InnerSttcMember innerSttcMember = new InnerSttcMember();

            public void func () {
                innerInstMember.func();
                innerSttcMember.func();
                System.out.println("메소드 안의 클래스");
            }
        }
    }
```
outer 클래스에서 생성된 모든 필드와 클래스에 접근이 가능하다.
## 익명 클래스
따로 이름을 부여받지 않고 다른 클래스나 인터페이스로부터 상속 받아 만들어진다.

한 번만 사용되므로 클래스로 정의할 필요없이 간단하게 구축하고, 사용후 버려진다.
```
import sec05.chap08.*;

public class Main {
    public static void main(String[] args) {
        Kakao store1 = new Chicken("울산");
        Kakao store2 = new Cafe("창원", true);

        Kakao store3 = new Kakao (1, "포항") {
            @Override
            public void takeOrder() {
                System.out.printf(
                        "super.intro() // super: Kakao
                );
            }

            public void dryFish () {
                System.out.println("anonymous");
            }
        };

        // store3.dryFish // 오류 발생
    }
}
```
익명 클래스의 인스턴스는 상속받거나 오버라이드 된 메소드만 호출 가능하다. 위에서는 Kakao 인스턴스를 상속받아 사용하였다.

익명 클래스 내부에서 생성한 메소드는 익명 클래스 밖에서는 사용 불가능하다.
# 메인 메소드
```
javac <class_name>.java

java <class_name> <args>
```
위의 방식으로 메인 메소드에 인자를 입력할 수 있다.
# 열거형
지정된 값을 반복하여 사용하는 경우 발생할 수 있는 오류를 없애기 위해 사용한다.
```
public class Button {
    enum Mode { LIGHT, DARK }
    enum Space { SINGLE, DOUBLE, TRIPLE }

    private Mode mode = Mode.LIGHT;
    private Space space = Space.SINGLE; // 메소드 사용을 위해 디폴트 값을 넣는 형식으로 초기화

    public void setMode(Mode mode) {
        this.mode = mode;
    }

    public void setSpace(Space space) {
        this.space = space;
    }
}

public class Main1 {
    public static void main(String[] args) {
        Button button1 = new Button();

        button1.setMode(Button.Mode.LIGHT);
        button1.setSpace(Button.Space.DOUBLE);
    }
}
```
`Mode, Space`를 `enum`형식으로 생성하였다. 그 결과 `Mode.` 혹은 `Space.`을 입력하면 자동으로 해당 하는 자료인 `{ LIGHT, DARK }, { SINGLE, DOUBLE, TRIPLE }`이 나오게 된다.
***
```
public enum Clothes {
    HD("후드티", 100000, 1),
    MM("맨투맨", 80000, 3),
    JS("청바지", 90000, 2),

    private String type;
    private int price;
    private int rank;

    Clothes(String type, int price, int rank) {
        this.type = type;
        this.price = price;
        this.rank = rank;
    }

    public String getName() { return name; }
    public int getPrice() { return price; }
}
```
`enum`을 사용하는 경우 `Clothes(String type, int price, int rank)`에서 설정한 순서대로 해당 배열이 설정된다.
```
HD(type: "후드티", price: 100000, rank: 1)
```
위와 같이 표기된다.
```
public class Main2 {
    public static void main(String[] args) {
        Clothes cloth1 = Clothes.HD;
        Clothes cloth2 = Clothes.MM;
        Clothes cloth3 = Clothes.JS;

        var cloth1Name = cloth1.getName();
        var cloth2Price = cloth2.getPrice();

        var byNames = new YalcoChickenMenu[] { // byNames: 0 = "HD"
                Clothes.valueOf("HD"),						    - name = "후드티", price = 100000, rank = 1
                Clothes.valueOf("MM"),					   1 = "MM"
                Clothes.valueOf("JS"),                     2 = "JS"
                // Clothes.valueOf("NN"), // 오류 발생
        };

        var names = new String[] { // names: ["HD", "MM", "JS"]
                cloth1.name(), cloth2.name(), cloth3.name()
        };

        var orders = new int[] { // orders: [1, 2, 3]
                cloth1.ordinal(), cloth2.ordinal(), cloth3.ordinal()
        };

        var menus = YalcoChickenMenu.values(); // menus: "HD"
    }													 - name = "후드티", price = 100000, rank = 1
}														 "MM" ...
```
`valueOf()`는 해당 이름의 가진 값 내부의 모든 데이터를 가지고온다. `enum` 내부에 요청한 값이 없다면 오류가 발생한다.

`name()`은 enum의 각 항목의 이름을 반환한다.

`ordinal()`는 enum 값의 순서를 반환한다.

`values()`는 enum의 전체 배열을 반환한다.
