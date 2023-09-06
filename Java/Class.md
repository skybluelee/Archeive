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
