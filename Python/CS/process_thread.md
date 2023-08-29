# 프로세스와 스레드
**프로세스(Process)**
- 프로세스는 운영 체제에서 실행 중인 프로그램의 인스턴스이다.
- 각 프로세스는 독립된 메모리 공간을 가지며, 서로 영향을 미치지 않는다. 즉, 한 프로세스의 오류가 다른 프로세스에 영향을 미치지 않는다.
- 프로세스는 자체적인 자원(메모리, 파일 핸들, CPU 시간 등)을 할당받아 실행된다.
- 프로세스 간 통신은 비용이 높고 복잡한데, 이는 운영 체제에서 제공하는 메커니즘을 사용해야 하기 때문이다.
- 파이썬에서 multiprocessing 모듈을 사용하여 멀티프로세싱을 구현할 수 있다.

**스레드(Thread):**
- 스레드는 프로세스 내에서 실행되는 작은 실행 단위이다.
- 스레드는 같은 프로세스 내의 다른 스레드와 메모리를 공유한다. 따라서 데이터 공유와 통신이 간단하다.
- 스레드는 프로세스 내의 자원을 공유하므로 프로세스에 비해 가볍고 빠르게 생성 및 종료할 수 있다.
- 하나의 스레드에서 오류가 발생하면 프로세스 전체에 영향을 줄 수 있으므로 스레드 간 동기화가 필요하다.
- 파이썬에서 threading 모듈을 사용하여 멀티스레딩을 구현할 수 있다.
## 파이썬에서 threading 모듈 사용하기
파이썬 기본 모듈로는 `thread`와 `threading` 모듈이 있는데 보통 `threading` 모듈을 더 자주 사용한다. 이외에도 GUI 라이브러리인 PyQt의 `QThread`를 사용하기도 한다.
```
import threading
import time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        time.sleep(3)
        print("sub thread end   ", threading.currentThread().getName())


print("main thread start")
for i in range(5):
    name = "thread {}".format(i)
    t = Worker(name)              
    t.start()                       # sub thread의 run 메서드를 호출

print("main thread end")

main thread start
sub thread start  thread 0
sub thread start  thread 1
sub thread start  thread 2
sub thread start  thread 3
sub thread start  thread 4
main thread end
sub thread end    thread 4
sub thread end    thread 0
sub thread end    thread 3
sub thread end    thread 1
sub thread end    thread 2
```
메인 스레드가 5개의 서브 스레드를 생성하고 `start` 메소드를 호출하여 `Worker` 클래스에 정의된 `run()` 메소드를 호출한다. 메인 스레드와 5개의 서브 스레드는 운영체제의 스케줄러에 의해 스케줄링되면서 실행된다.
## 데몬 스레드
`threading` 모듈을 사용하여 메인 스레드가 서브 스레드를 생성하는 경우 메인 스레드는 서브 스레드가 모두 종료될 때까지 기다렸다고 종료한다. 반면 데몬(daemon) 스레드는 메인 스레드가 종료될 때 자신의 실행 상태와 상관없이 종료되는 서브 스레드를 의미한다.
```
import threading
import time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        time.sleep(3)
        print("sub thread end   ", threading.currentThread().getName())

print("main thread start")
for i in range(5):
    name = "thread {}".format(i)
    t = Worker(name)
    t.daemon = True
    t.start()

print("main thread end")

main thread start
sub thread start  thread 0
sub thread start  thread 1
sub thread start  thread 2
sub thread start  thread 3
sub thread start  thread 4
main thread end
sub thread end    thread 3
sub thread end    thread 0
sub thread end    thread 4
sub thread end    thread 2
sub thread end    thread 1
```
`t.daemon = True`를 통해 데몬 스레드로 만들 수 있고 `threading`과 달리 메인 스레드가 서브 스레드보다 빨리 종료되는 것을 확인할 수 있다.
## Fork, Join
메인 스레드가 서브 스레드를 생성하는 것을 fork라고 하고, 모든 스레드가 작업을 마칠 때까지 기다리는 것을 join이라 한다. 보통 데이터를 여러 스레드를 통해서 병렬로 처리한 후 그 값들을 다시 모아서 순차적으로 처리해야할 필요가 있을 때 분할한 데이터가 모든 스레드에서 처리될 때까지 기다렸다가 메인 스레드가 다시 추후 작업을 하는 경우에 사용한다.
```
import threading
import time


class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name    

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        time.sleep(5)
        print("sub thread end   ", threading.currentThread().getName())


print("main thread start")

t1 = Worker("1") 
t1.start()         

t2 = Worker("2")   
t2.start()          

t1.join()
t2.join()

print("main thread post job")
print("main thread end")

main thread start
sub thread start  1
sub thread start  2
sub thread end    1 
sub thread end    2
main thread post job
main thread end
```
가장 처음 예시에서는 메인 스레드가 모든 실행을 완료한 후 서브 스레드가 종료될 때까지 기다렸고, `join`을 사용하는 경우 메인 스레드가 서브 스레드가 종료될 때까지 기다린다는 차이가 있다.
## 결론
파이썬의 Global Interpreter Lock (GIL)은 CPython (파이썬의 표준 구현)에서 스레드 간 병렬 처리를 제한하는데 사용되며, 이로 인해 CPython에서 멀티스레딩이 CPU 바운드 작업에는 효과적이지 않을 수 있다. 그러나 I/O 바운드 작업에는 여전히 유용할 수 있다.

요약하면, 프로세스와 스레드는 다중 작업을 관리하고 병렬성을 활용하는 데 사용되는 중요한 개념이며, 파이썬에서 이러한 개념을 구현할 때 multiprocessing 및 threading 모듈을 사용할 수 있다.
