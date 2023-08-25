# 함수
## 가변 인자
**Positional variable argument** `(*args)`
- 위치 가변 인자, 인자 값을 그대로 전달

**Keyword variable argument** `(**kwargs)`
- 키워드 가변 인자, 키워드와 키워드 값을 전달
```
def foo(*args, **kwargs):
    print(args)
    print(kwargs)

foo(1, 2, 3, a=1, b=1, c=2)

(1, 2, 3)
{'a': 1, 'b': 1, 'c': 2}
```
kwargs의 경우 변수가 딕셔너리 형태로 바인딩함.
## lambda 함수
익명 함수라고도 함.
```
a = lambda x: x + 2

print(a(2))

4
```
`lambda` 옆의 `x`는 입력을 의미하고 `:` 이후의 값이 리턴된다.
***
```
print((lambda x: x + 2)(2))

4
```
lambda 표현식 자체를 호출할 수 있다.
***
```
(lambda : print('nothing'))()

nothing
```
매개변수 없이 생성할 수 있다.
## 내장 함수
**`hasattr`**
`hasattr(객체, 이름)` 내장 함수의 인자로 넘겨주는 문자열 타입의 이름이 객체에 존재하면 True, 그렇지 않으면 False를 반환함.
```
class Car:
    def __init__(self):
        self.wheels = 4

    def drive(self):
        print("drive")

mycar = Car()
```
```
hasattr(mycar, "wheels")
hasattr(mycar, "drive")
hasattr(mycar, "drives")

True
True
False
```
***
**`getattr`**
내부의 객체를 리턴하거나 함수를 실행한 결과를 리턴한다.
```
num_wheel = getattr(mycar, "wheels")
print(num_wheel, type(num_wheel))

4 <class 'int'>
---------------------------------------
method = getattr(mycar, "drive")
type(method)
method()

method
drive
```
변수의 경우 해당 변수를 가져오고 함수의 경우 리턴 값을 가져온다.
## LEGB
변수를 참조하는 경우 LEGB 순으로 탐색함
- L: Local, 함수 안
- E: Enclosed Functions Locals, 내부 함수에서 자신의 외부 함수의 범위
- G: Global, 전역
- B: Built-in, open, range와 같은 파이썬 내장 함수를 의미
```
a = 10       # global
def test():
    a = 20   # local
    print(a)
test()

20
```
local이 우선이므로 20이 출력한다.
```
a = 10
def test():
    a = 20
    print(a)
test()
print(a)

20
10
```
함수 내의 local 영역에서 생성된 변수는 함수 호출이 끝나면 소멸된다. 따라서 전역 변수 값인 10이 이후에 출력된다.
```
a = 10
def test():
    global a
    a = 20

test()
print(a)

20
```
함수내의 변수가 소멸되지 않기 위해서는 global로 선언하면 해결된다.
```
def outer(num):
    def inner():
        print(num)
    return inner
f1 = outer(3)
f1()

3
```
내부 함수가 존재하는 경우 자신 외부 함수에서 변수를 참조한다.
outer함수 호출 -> inner 함수 객체 생성시 num 값을 내부 함수 객체에 저장 -> inner 함수 객체의 주소가 리턴 -> f1 변수가 바인딩

이때 num값은 `__closure__` 속성에 저장된다.
