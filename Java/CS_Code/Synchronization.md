# 동기화(Synchronization)
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
# Synchronization Method
## wait, notify, notifyAll
`wait`은 동기화 메소드 사용 중에 자기가 하는 일을 멈추고 다른 쓰레드가 사용하도록 양보한다.

`notify`는 일을 멈춘 상태의 쓰레드에게 자리가 비었음을 통보한다. 대기열의 쓰레드 중 하나에만 통보하므로 상황에 따라 무한대기상태에 빠질 수 있다.

`notifyAll`은 대기중인 모든 쓰레드에 통보한다. `notify`보다 자주 사용된다.
***
```
public class PhoneBooth {
    synchronized public void phoneCall (SoldierRun soldier) {
        System.out.println("☎️ %s 전화 사용중...".formatted(soldier.title));

        try { Thread.sleep(500);
        } catch (InterruptedException e) {}

        System.out.println("👍 %s 전화 사용 완료".formatted(soldier.title));

        notifyAll();
        try {
            //  💡 현 사용자를 폰부스에서 내보냄
            //  - sleep처럼 아래의 예외 반환 확인
            wait();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
```
`notifyAll ~` 부분을 주석처리하면 하나의 쓰레드만 동작하게 된다. 이러한 원인은 아래와 같다.
1. 동기화 부재: `wait`와 `notifyAll`을 사용하지 않으면 쓰레드들은 동기화 메커니즘을 갖지 않는다. 따라서 다수의 쓰레드가 공유 자원에 동시에 액세스할 수 있으며 경합 조건 (Race Condition)이 발생할 수 있다. 이는 여러 쓰레드가 동시에 PhoneBooth의 리소스에 접근하려고 할 때 하나의 쓰레드만 자원을 사용하게 될 수 있는 원인 중 하나이다.
2. 공유 자원 점유: PhoneBooth 클래스의 인스턴스는 여러 쓰레드가 공유하는 자원이다. `wait`와 `notifyAll`을 사용하지 않으면 쓰레드가 이 자원을 점유하고 있을 때, 다른 쓰레드는 그 자원에 접근할 수 없다. 이로 인해 다른 쓰레드들은 자원을 기다리며 실행을 멈추게 된다.
3. 경합 조건: 경합 조건은 여러 쓰레드가 공유 자원에 동시에 접근하여 자원의 일관성을 해치는 상황을 의미한다. `wait`와 `notifyAll`을 사용하지 않으면 쓰레드 간에 경합 조건이 발생할 수 있으며, 이로 인해 예상치 못한 결과가 발생할 수 있다.

`wait`와 `notifyAll`을 사용하여 쓰레드 간에 동기화를 관리하면 쓰레드 간의 순서와 상호 작용을 조절할 수 있으며, 공유 자원에 대한 안전한 액세스를 보장할 수 있다. 이를 통해 여러 쓰레드가 동시에 자원을 사용하거나 경합 조건을 피할 수 있다.
