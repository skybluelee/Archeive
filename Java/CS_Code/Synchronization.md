# 동기화
특정 자원에 여러 쓰레드가 동시에 접근하는 것을 방지한다.
# synchronized
```
public class ATM {
    ...
    synchronized public void withdraw (String name, int amount) {
    if (balance < amount) return;
        try {
            Thread.sleep(new Random().nextInt(700, 1000));
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        balance -= amount;
    }
}
```
```
public class ATM {
    ...
    public void withdraw (String name, int amount) {
        synchronized (this) {              // this는 현 쓰레드를 의미함
            if (balance < amount) return;
            try {
                Thread.sleep(new Random().nextInt(700, 1000));
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            balance -= amount;
        }
    }
}
```
한번에 한 쓰레드만 접근하도록 만든다.

`synchronized`를 메소드 선언시에 붙여 메소드 전체를 동기화하거나, 메소드 내에서 `synchronized (this) {}`를 사용하여 특정 작업만 동기화하도록 설정할 수 있다.
# Cache
```
public class Cache1 {
    static boolean stop = false;
    public static void main(String[] args) {
        new Thread(() -> {
            int i = 0;
            while (!stop) {
                i++;
                System.out.println(i);
            }
            System.out.println("- - - 쓰레드 종료 - - -");
        }).start();

        try { Thread.sleep(1000);
        } catch (InterruptedException e) {}

        stop = true;

        //  💡 JVM의 캐시 방식에 따라 멈출 수도 안 멈출 수도 있음
        //  - stop으로의 접근이 동기화되지 않았을 시
        //  - 한 쓰레드가 그 값을 바꿔도 다른 쓰레드는 캐시에 저장된
        //  - 바뀌기 이전 값을 참조할 수 있음
        //    - println 메소드는 위 코드에서 캐시를 비우는 이유 제공
    }
}
```
`System.out.println(i)`가 있는 상태로 실행하면 의도한대로 10초 후에 종료된다.

하지만 `System.out.println(i)`를 주석처리한 후 실행하면 10초가 지난 후에도 계속해서 실행된다.

자바에서는 기본적으로 임시 메모리 - 캐시를 사용하는데, `println`이 있는 경우 해당 코드를 실행하기 위해 캐시에 있던 값 `i`를 강제로 옮긴다.
하지만 `println`이 없는 경우 메모리로 `i`를 옮길 이유가 없어 `i`는 임시 메모리 - 캐시에 누적되거나, JVM의 방식에 따라 실행 조차 안하는 상황일 수도 있다.
## Cache 문제 해결 - volatile
```
public class Cache2 {
    volatile static boolean stop = false;
    public static void main(String[] args) {
        new Thread(() -> {
            int i = 0;
            while (!stop) {
                i++;
            }

            System.out.println("- - - 쓰레드 종료 - - -");
        }).start();

        try { Thread.sleep(1000);
        } catch (InterruptedException e) {}

        stop = true;
    }
}
```
`volatile` 연산자는 변수의 값이 변경될 때마다 메모리에 업데이트하여 캐싱에 의한 문제를 방지할 수 있다.

단 동기화와는 다른 개념이다.
## Cache 문제 해결 - synchronization
```
public class Cache3 {
    static boolean stop = false;

    synchronized public static boolean isStop() {
        return stop;
    }
    synchronized public static void setStop(boolean stop) {
        Cache3.stop = stop;
    }

    public static void main(String[] args) {
        new Thread(() -> {
            int i = 0;
            while (!isStop()) {
                i++;
            }

            System.out.println("- - - 쓰레드 종료 - - -");
        }).start();

        try { Thread.sleep(1000);
        } catch (InterruptedException e) {}

        setStop(true);
    }
}
```
동기화를 진행하면 `i`가 증가하는 메소드와 쓰레드 종료를 결정하는 메소드가 번갈아 가며 실행되므로 캐싱에 의한 문제를 방지할 수 있다.
