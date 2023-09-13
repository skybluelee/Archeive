# 생성 및 동작 방식
```
public class Thread1 extends Thread {
    @Override
    public void run() {

        for (var i = 0; i < 20; i++) {
            System.out.print(1);
        }
    }
}
```
```
public class MyRunnable implements Runnable {
    @Override
    public void run() {

        for (var i = 0; i < 20; i++) {
            System.out.print(2);
        }
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        Thread thread1 = new Thread1();                // Thread 상속시
        Thread thread2 = new Thread(new MyRunnable()); // Runnable 구현시

        // run은 메인 스레드에서 동작
//        thread1.run();
//        thread2.run();

        thread1.start();
        thread2.start();

        for (var i = 0; i < 20; i++) {
            System.out.print('M');
        }
    }
}
```
쓰레드를 만드는 방법으로는 `Thread` 클래스를 상속하거나, `Runnable`인터페이스를 구현하는 방법이 있다.

각 방식의 차이가 다른 것을 확인할 수 있다.

`run()`을 사용하는 경우 메인 쓰레드에서 동작하기 때문에 병렬 처리가 불가능해 사실상 쓰레드를 사용하지 못한다.

쓰레드를 사용하기 위해서는 `start()` 메소드를 사용한다.
## sleep
```
public class MyRunnable implements Runnable {
    @Override
    public void run() {

        for (var i = 0; i < 20; i++) {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

            System.out.print(2);
        }
    }
}
```
sleep을 사용하는 경우 InterruptedException가 발생하기 때문에 `try catch`로 감싸주어야 한다.
# 쓰레드 이름
```
Thread thread = new Thread(new TarzanRun(100));

thread.setName("new thread");

thread.start();
```
쓰레드의 이름은 자바에서 임의로 정해진 정수를 붙여 진행된다. `Thread-0: ...`

`setName` 메소드를 사용하면 쓰레드의 이름을 붙일 수 있다. `new thread: ...`
# 우선 순위
```
public class Main {
    public static void main(String[] args) {
        Thread thr0 = new Thread(new PrintThrNoRun(0));
        Thread thr1 = new Thread(new PrintThrNoRun(1));
        Thread thr2 = new Thread(new PrintThrNoRun(2));

        thr0.setPriority(Thread.MIN_PRIORITY);
        thr1.setPriority(Thread.NORM_PRIORITY);
        thr2.setPriority(Thread.MAX_PRIORITY);

        thr0.start();
        thr1.start();
        thr2.start();    
```
`setPriority`는 우선 순위를 매기는 메소드로 MIN_PRIORITY: 1, NORM_PRIORITY: 5, MAX_PRIORITY: 10의 값을 갖는다.

코드대로라면 thr0, thr1, thr2 순으로 실행된다.
***
```
public class Main {
    public static void main(String[] args) {
        new Thread(() -> {
            for (var i = 0; i < 20; i++) {
                System.out.print(3);
                for (var j = 0; j < Integer.MAX_VALUE; j++) {}
                Thread.yield(); // 양보
            }
        }).start();

        for (var i = 0; i < 20; i++) {
            System.out.print('M');
            for (var j = 0; j < Integer.MAX_VALUE; j++) {}
        }
    }
}
```
`yield`는 해당 쓰레드의 우선 순위를 양보하는 메소드이다.

코드대로라면 두번째 쓰레드가 끝나고 첫번째 쓰레드가 실행된다.
***
쓰레드 우선 순위 설정은 OS가 판단한다. 따라서 우선 순위를 지정하더라도 항상 동작하지 않는다.
# 멀티태스킹
```
public class TarzanRun implements Runnable {
    int max;
    public TarzanRun(int max) { this.max = max; }

    @Override
    public void run() {
        var lyric = "%s : Update Loading %d%%";

        for (var i = 0; i < max; i++) {

            try {
                Thread.sleep(2000);
                System.out.printf(
                        (lyric) + "%n", Thread.currentThread().getName(),
                        i * 10
                );
            } catch (InterruptedException e) {           // 메인 쓰레드에서 인터럽트를 발생시킬 때 발생하는 오류
                System.out.println("Terminate Thread");
                return;
            }
        }
    }
}
```
```
public class Main2 {
    public static void main(String[] args) {
        Thread tarzanSong = new Thread(new TarzanRun(10));
        tarzanSong.start();
                //.run();   // 메인 쓰레드에서만 동작. 멀티태스킹 불가

        try (Scanner sc = new Scanner(System.in)) {
            while (sc.hasNext()) {
                var line = sc.nextLine();
                if (line.equalsIgnoreCase("check")) {
                    // isAlive : 해당 쓰레드가 진행중인지 여부
                    System.out.println(tarzanSong.isAlive() ? "Proceeding." : "Terminated.");
                }

                if (line.equalsIgnoreCase("enjoy")) {
                    System.out.println("감상할 가치가 있는 노래다.");
                    // join의 경우 try catch가 필요
                    try {
                        tarzanSong.join();       // join에 인자가 없는 경우 쓰레드가 종료될 때까지 입력 문자열을 모아둔 후 종료후에 한번에 반환함
                      //tarzanSong.join(5000);   // join에 인자가 있는 경우 (인자)ms만큼 입력 문자열을 모아둔 후 명시한 시간이 지나면 문자열을 반환함
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }

                if (line.equalsIgnoreCase("stop")) {
                    System.out.println("아 제발 좀 닥쳐봐!");
                    // 해당 쓰레드의 run에 InterruptedException 발생시킴
                    tarzanSong.interrupt();
                }

                if (line.equalsIgnoreCase("quit")) break;
                System.out.println(line);
            }
        }
    }
}
```
# 쓰레드 그룹
쓰레드 그룹은 연관된 쓰레드를 그룹으로 묶어 일괄적으로 다루거나 보안상 분리하기 위해 사용한다.

쓰레드 그룹은 다른 쓰레드 그룹에 포함될 수 있다.
## 쓰레드 그룹 생성
```
public class Main {
    public static void main(String[] args) {
        Thread thr1 = new Thread(() -> {});
        ThreadGroup mainThrGroup = thr1.getThreadGroup();
        String mainThrGroupName = mainThrGroup.getName(); // mainThrGroupName: main

        // 쓰레드 그룹 생성하기
        ThreadGroup threadGroup1 = new ThreadGroup("TG_1");
        String thrGroup1Name = threadGroup1.getName();       // thrGroup1Name: TG_1

        // 그룹에 속한 쓰레드 생성
        Thread thr2 = new Thread(threadGroup1, () -> {});
        String thr2GroupName = thr2.getThreadGroup().getName(); // thr2GroupName:TG_1

        // 쓰레드 그룹에 속한 쓰레드 그룹 만들기
        ThreadGroup threadGroup2 = new ThreadGroup(threadGroup1, "TG_2");
        String thrGroup2ParentName = threadGroup2.getParent().getName(); // thrGroup2ParentName: TG_1
    }
}
```
`new Thread(() -> {})` -> 인자가 존재하지 않는다.
쓰레드 그룹을 생성하지 않은채로 쓰레드를 생성한다면 기본 쓰레드 그룹인 main 쓰레드에 배치된다.

`ThreadGroup`클래스를 사용하여 쓰레드 그룹을 생성하고, `new Thread(threadGroup1, () -> {})` 해당 그룹을 인자로하여 쓰레드를 생성한다면
`.getThreadGroup().getName()` 메소드를 통해 쓰레드 그룹의 이름을 얻을 수 있고, 해당하는 쓰레드 그룹의 이름을 얻을 수 있다.

그룹안에 그룹을 만들고자 한다면 `ThreadGroup(threadGroup1, "TG_2")` 메소드에 첫번째 인자로 부모 그룹의 이름, 두번째 인자로 생성할 그룹의 인자를 입력한다.

그룹 내에 그룹이 존재하고, 부모 그룹에 쓰레드를 파악하는 경우 **부모 그룹과 모든 자손 그룹의 쓰레드의 수를 확인**(`activeCount()` 메소드 사용)할 수 있고,
**부모 그룹에 쓰레드 종료를 요청하면 자손 그룹의 쓰레드도 종료된다.**
# 데몬 쓰레드
메인 쓰레드의 작업을 보조하는 역할을 하며, 메인 쓰레드의 작업이 끝나면 자동 종료된다.
```
public class Main3 {
    public static void main(String[] args) {
        // 데몬 쓰레드로 사용할 쓰레드를 정의
        Runnable rythmRun = () -> {
            while (true) {
                System.out.print("deamon working");

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        };

        // 메인 쓰레드 정의
        Thread SingThread = new Thread(() -> {
            var lines = new String[] {
                    "10%", "20%", "30%", "40%", "50%",
                    "60%", "70%", "80%", "90%", "100%"
            };

            Thread rythmThread = new Thread(rythmRun); // 쓰레드 내에서 쓰레드 정의

            rythmThread.setDaemon(true);   // 데몬 쓰레드로 설정

            rythmThread.start();

            for (var i = 0; i < lines.length; i++) {
                System.out.println("\n" + lines[i]);
                try {
                    Thread.sleep(1200);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });

        SingThread.start();
    }
}

10%
deamon working
20%
deamon working
...
100%
deamon working
```
데몬 쓰레드 사용 방식은 아래와 같다.
1. 데몬 쓰레드로 사용할 쓰레드와 메인 쓰레드를 생성한다.
2. 메인 쓰레드 내에서 데몬 쓰레드로 사용할 쓰레드를 객체로 생성한다. `Thread rythmThread = new Thread(rythmRun)`
3. 데몬 쓰레드 객체를 `setDaemon(true)` 메소드를 사용하여 데몬 쓰레드로 정의한다.
4. 메인 쓰레드 내에서 데몬 쓰레드를 `start()`한다.
5. 메인 메소드에서 메인 쓰레드를 `start()`한다.
