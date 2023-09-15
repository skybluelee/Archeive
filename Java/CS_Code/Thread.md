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
# 쓰레드 풀
많은 쓰레드 작업이 필요할 때 너무 많은 쓰레드 작업으로 인한 부하를 방지하기 위해 동시에 돌아가는 쓰레드들의 개수를 제한하는 방식이다.

쓰레드를 그때그때 생성 혹은 제거하지 않고, 주어진 개수만큼 쓰레드들을 만든 후 재사용한다.
```
public class Cave {
    private int water = 40;

    public int getWater() {
        return water;
    }
    public void pump() {
        if (getWater() > 0) water--;
    }
}
```
```
public class VolunteerRun implements Runnable {
    private static int lastNo = 0;
    private static int working = 0;

    private int no;
    private Cave cave;

    public VolunteerRun(Cave cave) {
        this.no = ++lastNo;
        this.cave = cave;

        System.out.printf("thread num: %d, water: %d%n", no, cave.getWater());
    }

    @Override
    public void run() {
        working++;
        System.out.printf("thread num: %d, thread count: %d, water: %d%n", no, working, cave.getWater());

        try { Thread.sleep(5000);
        } catch (InterruptedException e) {

            working--;
            System.out.printf("thread-%d terminated, thread count: %d, water: %d%n",no, working, cave.getWater()
            );
            return;
        }

        cave.pump();
        working--;
        System.out.printf(
                "thread-%d completed, thread count: %d, water: %d%n",
                no, working, cave.getWater()
        );
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        // ExecutorService: 쓰레드풀을 관리하는 라이브러리 클래스
        ExecutorService es = Executors.newFixedThreadPool(
                5 // 쓰레드 풀에서 동시에 일할 수 있는 최대 쓰레드 수
                  // = 스레드 풀 크기 = 풀의 최대 쓰레드 수
        );

        Cave cave = new Cave();

        while (cave.getWater() > 20) {            
            es.execute(new VolunteerRun(cave)); // execute : 쓰레드를 대기열에 추가

            try { Thread.sleep(500);
            } catch (InterruptedException e) { return; }
        }

        es.shutdown();  // 쓰레드 풀을 종료하고, 현재 실행 중인 작업을 마치고 종료
        // es.execute(new VolunteerRun(cave)); // shutdown이후에 쓰레드를 추가하면 예외 발생

        //  shutdownNow : 쓰레드 풀을 즉시 종료
        //  각 쓰레드에 InterruptedException을 발생, 즉 쓰레드 강제 종료가 아님
        //  작업 진행중인 쓰레드의 강제 종료는 InterruptedException에 대해 명령을 작성해야 함
        //List<Runnable> waitings = es.shutdownNow(); // 작업이 끝난 쓰레드 재사용 가능
                                                      // 기존 쓰레드 재사용을 확인하기 위해 list로 생성
        //System.out.println(waitings);
    }
}


```
`es.shutdown()`의 경우 작업이 전부 중지된 후 종료된다.

`es.shutdownNow()`의 경우 작업이 중간에 종료된다.
# Future
비동기적 연산의 결과로, 비동기 작업은 작업이 백그라운드에서 실행되고, 작업이 완료될 때까지 메인 스레드 또는 다른 작업을 차단하지 않고 계속 실행할 수 있도록 만든다.
```
public class Main3 {
    public static void main(String[] args) {
        ExecutorService es = Executors.newSingleThreadExecutor();
            Future<String> callAnswer = es.submit(() -> {
            Thread.sleep(2000);
            return "future answered";
        });

        // isDone : 퓨쳐의 태스크가 종료되었는지 여부 확인
        while (!callAnswer.isDone()) {
            System.out.println("Future Checking");
            try { Thread.sleep(400);
            } catch (InterruptedException e) {}
        }

        String result = null;
        try { result = callAnswer.get();
        } catch (InterruptedException | ExecutionException e) {}

        System.out.println("Status: " + result);
        System.out.println("Main Method");

        es.shutdown();
    }
}

Future Checking
Future Checking
Future Checking
Future Checking
Future Checking
Status: future answered
Main Method
```
Future는 Callable로 제네릭에 반환하는 값의 자료형을 명시한다.

작동 방식은 아래와 같다.
1. `get()` 메소드를 호출하기 전까지 백그라운드에서 실행된다.
2. future 쓰레드의 종료를 확인한다. 위에서는 `isDone` 메소드를 사용했다.
3. `get()` 메소드를 사용하여 결과를 받아온다. 이 작업이 끝나기 전까지 이외의 작업은 전부 막힌다(블로킹).
4. future 쓰레드가 종료되고 메인 쓰레드에서 막혔던 작업이 시작된다.
# CompletableFuture
Future보다 편리한 기능을 제공한다.
- 연속되는 작업들을 비동기적으로 함수형으로 작성
- 여러 비동기 작업들을 조합하고, 병렬적으로 실행 가능
- 예외 처리를 위한 기능들 제공
## 생성
```
package sec11.chap07;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class Main {
    public static void main(String[] args) {
        try {
            supplyAsyncEx();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void takeTime (boolean error) {
        try {
            int randMilliSec = new Random().nextInt(1000, 1500);
            Thread.sleep(randMilliSec);
            System.out.printf("... %f 초 경과 ...%n", randMilliSec / 1000.0);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        if (error) throw new RuntimeException("오류 발생");
    }

    public static void supplyAsyncEx () throws ExecutionException, InterruptedException {
        CompletableFuture<String> getHello = CompletableFuture.supplyAsync(() -> {
            takeTime(false);
            return "Hello";
        });

        System.out.println("- - - get 사용 전 - - -");

        String hello = getHello.get();

        System.out.println("- - - get 사용 후 - - -");
        System.out.println(hello);
    }
}

- - - get 사용 전 - - -
... 1.343000 초 경과 ...
- - - get 사용 후 - - -
Hello
```
`CompletableFuture`를 생성하는 메소드 `supplyAsync`는 Supplier를 받아 비동기 작업 실행한다. Supplier는 인자는 없고, 반환값은 있어 제네릭에 명시한다.

Future와 동일하게 `get` 메소드를 사용하면 블로킹이 발생하고, 해당 값을 받기 전까지 다음 코드의 진행을 막는다(이 순간은 비동기가 아님). 값을 받은 후 메인 쓰레드가 진행된다.
## thenAccept
```
public class Main {
    public static void main(String[] args) {
        thenAcceptEx1();
    }

    public static void takeTime (boolean error) {
        try {
            int randMilliSec = new Random().nextInt(1000, 1500);
            Thread.sleep(randMilliSec);
            System.out.printf("... %f 초 경과 ...%n", randMilliSec / 1000.0);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        if (error) throw new RuntimeException("오류 발생");
    }

    public static void thenAcceptEx1 () throws ExecutionException, InterruptedException {
        CompletableFuture<String> getHello = CompletableFuture.supplyAsync(() -> {
            System.out.println("값 받아오기 시작");
            takeTime(false);
            return "Hello";
        });

        CompletableFuture<Void> printHello = getHello.thenAccept(s -> {
            System.out.println("받아온 값 처리 시작");
            takeTime(false);
            System.out.println(s);
        });

        System.out.println("- - - 중간에 다른 코드들 진행 - - -");

        printHello.get();
}

값 받아오기 시작
- - - 중간에 다른 코드들 진행 - - -
... 1.434000 초 경과 ...
받아온 값 처리 시작
... 1.296000 초 경과 ...
Hello
```
`thenAccept` 메소드는 Consumer로 인자를 사용하고, 반환값은 없다. 위의 경우 인자 `s`는 `getHello`의 반환값 `"Hello"`이다.

`get` 메소드를 호출한 후에 `thenAccept` 이하의 작업이 실행된다(동기). 호출하기 전까지는 실행할 일을 지정했을 뿐이다(비동기).
***
```
public static void thenAcceptEx2 () throws ExecutionException, InterruptedException {
    CompletableFuture<Void> print5nums = CompletableFuture.supplyAsync(() -> {
            List<Integer> ints = new ArrayList<>();
            IntStream.range(0, 5).forEach(i -> {
                takeTime(false);
                ints.add(i);
            });
            return ints;
        }).thenAccept(list -> {
            takeTime(false);
            list.stream().forEach(System.out::println);
        });

        System.out.println("- - - 중간에 다른 코드들 진행 - - -");

        print5nums.get();
    }
```
`CompletableFuture`의 제니릭 자료형이 `Void`인 이유는 최종 결과인 `thenAccept`에서의 반환값이 없기 때문이다.

위와 다르게 객체를 생성해서 각각 메소드를 실행하지 않고 하나로 묶어서 실행했다.
## thenApply
```
public class Main {
    public static void main(String[] args) {
        thenApplyEx1();
    }

    public static void thenApplyEx1 () throws ExecutionException, InterruptedException {
        CompletableFuture.supplyAsync(() -> {
            takeTime(false);   // ... 1.175000 초 경과 ...
            return new Random().nextInt(0, 6) + 1;

        }).thenApply(
                //  💡 thenApply : 얻어온 값을 Function에 넣어 다른 값 반환
                //  - 스트림의 map과 비슷
                i -> {
                    takeTime(false);   // ... 1.277000 초 경과 ...
                    return "이번 숫자: " + i;
                }
        ).thenAccept(
                System.out::println
        ).get();
    }

        System.out.println("- - - 중간에 다른 코드들 진행 - - -");

        printHello.get();
}

... 1.175000 초 경과 ...
... 1.277000 초 경과 ...
이번 숫자: 2
```
`thenApply`는 Function으로 인자를 받고, 반환값이 존재한다. 위의 경우 `i`는 `new Random().nextInt(0, 6) + 1`의 값이다.

`thenAccept`의 람다식은 `thenAccept(s -> System.out.println(s))`로 `"이번 숫자: " + i`이 인자이다.
## exceptionally
```
public class Main {
    public static void main(String[] args) {
        exceptionallyEx(true); // 오류 발생
    }

    public static void exceptionallyEx (Boolean error) throws ExecutionException, InterruptedException {
        CompletableFuture.supplyAsync(() -> {
            takeTime(error);
            return "ㅇㅇ 안녕";

        }).exceptionally(e -> {
            e.printStackTrace();
            return "안녕 못해.";
        }).thenApply(s -> {
            takeTime(false);
            return "대답: " + s;
        }).thenAccept(
                System.out::println
        ).get();
    }
}

... 1.105000 초 경과 ...
대답: 안녕 못해.
```
`exceptionally`는 `Optional`의 `OrElse`와 유사하게 오류가 발생하면 해당 값을 반환한다.

단 `OrElse`나 `try catch`처럼 오류 발생을 해결하는 것이 아닌 오류가 발생과 값 리턴이 둘 다 발생한다.
## thenCompose, thenCombine
```
public class Main {
    public static void main(String[] args) {
        thenComposeEx();
        thenCombineEx();  // 동일한 결과
    }

    public static void thenComposeEx () throws ExecutionException, InterruptedException {

        CompletableFuture<Swordman> getBlueChamp = getChamp(Side.BLUE);
        CompletableFuture<Swordman> getRedChamp = getChamp(Side.RED);

        System.out.println("\n===== 양 진영 검사 훈련중 =====\n");

        //  💡 thenCompose : 두 CompleteFuture의 결과를 조합
        //  -  ⭐️ 두 작업이 동시에 진행됨 주목
        getBlueChamp.thenCompose(
                        b -> getRedChamp.thenApply(
                                r -> {
                                    if (b.hp == r.hp) throw new RuntimeException();
                                    return b.hp >= r.hp ? b : r;
                                })
                )
                .thenApply(Swordman::toString)
                .thenApply(s -> "🏆 승자 : " + s)
                .exceptionally(e -> "⚔ 무승부")
                .thenAccept(System.out::println)
                .get();
    }

    public static void thenCombineEx () {
        CompletableFuture<Swordman> getBlueChamp = getChamp(Side.BLUE);
        CompletableFuture<Swordman> getRedChamp = getChamp(Side.RED);

        System.out.println("\n===== 양 진영 검사 훈련중 =====\n");

        try {
            getBlueChamp.thenCombine(
                            getRedChamp,
                            (b, r) -> {
                                if (b.hp == r.hp) throw new RuntimeException();
                                return b.hp >= r.hp ? b : r;
                            })
                    .thenApply(Swordman::toString)
                    .thenApply(s -> "🏆 승자 : " + s)
                    .exceptionally(e -> "⚔ 무승부")
                    .thenAccept(System.out::println)
                    .get();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } catch (ExecutionException e) {
            throw new RuntimeException(e);
        }
    }
}
```
`thenCompose, thenCombine` 두 메소드 모두 2개의 비동기 쓰레드를 하나의 쓰레드로 합치는 역할을 한다. 다만 문법에서 차이를 보이낟.

`thenCompose`의 경우 `thenCompose(<instance1>.thenApply(<instance2>; <실행문>))` 형식이고,

`thenCombine`의 경우 `<instance1>.thenCombine(<instance2>; <실행문>)` 형식이다.
## allOf
```
public class Main {
    public static void main(String[] args) {
        allOfEx1();
    }

    public static CompletableFuture<Integer> rollDiceFuture () {
        return CompletableFuture.supplyAsync(() -> {
                    System.out.println("주사위 굴림");

                    takeTime(new Random().nextBoolean());
                    var result = new Random().nextInt(0, 6) + 1;
                    System.out.println("🎲 : " + result);
                    return result;
                }
        ).exceptionally(e -> -1); // 예외 대비
    }

    public static void allOfEx1 () throws ExecutionException, InterruptedException {
        var roll1 = rollDiceFuture();
        var roll2 = rollDiceFuture();
        var roll3 = rollDiceFuture();
        var roll4 = rollDiceFuture();
        var roll5 = rollDiceFuture();

        CompletableFuture.allOf(
                roll1, roll2, roll3, roll4, roll5
        ).thenRun(() -> {
            // 프린트 순서 확인
            System.out.println("결과 모두 나옴");

            var int1 = roll1.join();
            var int2 = roll2.join();
            var int3 = roll3.join();
            var int4 = roll4.join();
            var int5 = roll5.join();

            String result = IntStream.of(int1, int2, int3, int4, int5)
                    .boxed()
                    .map(i -> i == -1 ? "(무효)" : String.valueOf(i))
                    .collect(Collectors.joining(", "));
            System.out.println("최종 결과 : " + result);
        }).get();
    }
}
```
`allOf`는 `thenCompose, thenCombine`와 달리 여러개의 CompletableFuture 쓰레드를 동시에 진행할 수 있다.

`thenRun` 메소드는 결과들을 동기적으로 종합한다.
## anyOf
```
public class Main {
    public static void main(String[] args) {
        allOfEx1();
    }

    public static CompletableFuture<Integer> rollDiceFuture () {
        return CompletableFuture.supplyAsync(() -> {
                    System.out.println("주사위 굴림");

                    takeTime(new Random().nextBoolean());
                    var result = new Random().nextInt(0, 6) + 1;
                    System.out.println("🎲 : " + result);
                    return result;
                }
        ).exceptionally(e -> -1); // 예외 대비
    }

    public static void anyOfEx () throws ExecutionException, InterruptedException {
        ArrayList<CompletableFuture<String>> runners = new ArrayList<>();

        String[] names = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U"
                         .split(",");

        ForkJoinPool forkJoinPool = new ForkJoinPool(names.length);

        Arrays.stream(names)
              .forEach(r -> runners.add(raceRunner(r, forkJoinPool)));

        //  💡 anyOf : 가장 먼저 완료된 결과물을 받아옴
        CompletableFuture.anyOf(
                        runners.stream()
                                .toArray(CompletableFuture[]::new)
                )
                .thenAccept(w -> {
                    System.out.println(
                            w != null
                                    ? ("🏆 1등: " + w)
                                    : "💣 지뢰 폭발"
                    );
                })
                .get();
    }
}
```
`allOf`가 CompletableFuture의 모든 쓰레드의 값을 가져온다면 `anyOf`는 가장 먼저 완료된 결과물을 받아온다.
# 병렬 스트림
일반적으로 직렬보다 성능이 좋다. 하지만 데이터 크기가 작은 경우나 순차적으로 처리해야 하는 작업등은 병렬 스트림이 더 느리므로 작업의 특성을 고려해야 한다.
## 병렬 스트림 생성
```
public class Main {
    public static void main(String[] args) {
        Stream<Character> stream1 = Stream.of('A', 'B', 'C');
        var bool1 = stream1.isParallel(); // bool1: false

        stream1.parallel();
        var bool2 = stream1.isParallel(); // bool2: true

        stream1.sequential();
        var bool3 = stream1.isParallel(); // bool3: false
    }
}
```
`parallel()` 메소드를 사용하여 직렬 스트림을 병렬 스트림으로 변경할 수 있고,

`sequential()` 메소드를 사용하여 병렬 스트림을 직렬 스트림으로 변경할 수 있다.
***
```
public class Main {
    public static void main(String[] args) {
        Stream<Integer> stream2 = Arrays.asList(1, 2, 3, 4, 5)
                .parallelStream();

        List<Double> dblList = new ArrayList<>(
                Arrays.asList(1.23, 2.34, 3.45)
        );
        Stream<Double> stream3 = dblList.parallelStream();
    }
}
```
`parallelStream()` 메소드를 사용하여 처음부터 병렬 스트림으로 생성할 수 있다.
## 직렬 vs 병렬
`map`과 `filter`의 경우 병렬이 직렬보다 성능이 더 좋고,

`reduce`의 경우 순차 실행이므로 직렬이 병렬보다 성능이 더 좋다.

`sum`의 경우 양이 많으면 병렬의 성능이 더 좋지만, 양이 적으면 직렬의 성능이 더 좋다.

작업에 따라 직렬과 병렬을 적절히 선택해야 하고 아래와 같이 직렬과 병렬을 동시에 사용할 수도 있다.
```
package sec11.chap08;

import java.util.stream.IntStream;

public class Main2 {
    public static void main(String[] args) {
        final int RANGE = 10000000;

        measureTime("mixed", () -> {
            var tri = IntStream.range(0, TRI_RANGE)
                    .parallel()
                    .filter(i -> i % 2 == 0)
                    .map(i -> i + 1)          // filter, map 작업은 병렬로
                    .sequential() 
                    .reduce(Integer::sum);    // reduce 작업은 직렬로 수행
        });
    }
```
# Thread 관련 클래스
쓰레드 중복을 해결하는 클래스
## ConcurrentHashMap
```
public class Main {
    public static void main(String[] args) {
        Map<String, Integer> concurrentHashMap = new ConcurrentHashMap<>();

        Runnable toConcurrHashMap = () -> {
            for (int i = 0; i < 10000; i++) {
                concurrentHashMap.put("key" + i, i);
            }
        };

        measureTime("Concurrent 해시맵", () -> {
            Thread t1 = new Thread(toConcurrHashMap);
            Thread t2 = new Thread(toConcurrHashMap);
            Thread t3 = new Thread(toConcurrHashMap);

            t1.start(); t2.start(); t3.start();
            try {
                t1.join(); t2.join(); t3.join();
            } catch (InterruptedException e) {}
        });
    }
}
```
`ConcurrentHashMap`은 맵을 구획으로 분할하여 각 구획에 대해 동기화를 적용한다. 즉 쓰레드가 서로 다른 구획에 접근하여 작업한다.
## Atomic
```
public class Main3 {

    static int count = 0;
    static AtomicInteger atomicCount = new AtomicInteger(0);

    public static void main(String[] args) {
        Runnable incCount = () -> {
            for (int i = 0; i < 10000; i++) {
                count++;
                atomicCount.getAndIncrement();
            }
        };

        Thread t1 = new Thread(incCount);
        Thread t2 = new Thread(incCount);
        Thread t3 = new Thread(incCount);

        t1.start(); t2.start(); t3.start();

        try {
            t1.join(); t2.join(); t3.join();
        } catch (InterruptedException e) {}

        int result = count;
        int atomicResult = atomicCount.get();
    }
}
```
`Atomic` 클래스는 한 번에 하나의 쓰레드만 접근이 가능하므로 특정 변수에 대해 쓰레드로부터의 안전을 제공한다.
