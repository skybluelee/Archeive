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
        super("ShutDown"); // 💡 부모의 생성자 호출
    }                                                                      public ToggleButton(String print, boolean on) {
                                                                               super(print);
	@Override                                                                  this.on = on;
    public void func () {                                                  }
        System.out.println("프로그램 종료");
    }                                                                      @Override
}                                                                          public void func () {

```
