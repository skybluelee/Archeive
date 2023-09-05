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

**생성자**의 경우 해당 Class와 동일한 이름으로 인스턴스를 생성하는 것을 말한다.

`Market` 클래스의 `Market (int price, String type)`이하를 생성자라고 한다.

생성자를 사용하는 경우 Main문에서 인스턴스 생성과 변수 전달을 동시에 진행할 수 있다.

생성자가 없는 경우 인스턴스를 생성하고 변수를 각각 전달해야 한다.
`musinsa.type = "Hoodie"; musinsa.price = 100000;`
생성자를 만들지 않은채 실행하더라도 java 내에서 생성자를 생성한다.

**this**는 생성한 객체를 의미한다.
`Market (int price, String type) {
        this.price = price;
        this.type = type;
    }`
    
위 코드는 해당 인스턴스의 변수 `price, type`에 값을 넣는다.

사용 변수가 겹치는 경우 원하는 값이 제대로 들어가지 않는 경우가 있는데, `this`를 사용하여 해결할 수 있다.
