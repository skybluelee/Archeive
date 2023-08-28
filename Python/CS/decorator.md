# 데코레이터
어떤 함수가 있을 때 해당 함수를 직접 수정하지 않고 함수에 기능을 추가하고자 할 때 데코레이터를 사용한다.
```
def hello():
    print("hello")

def deco(fn):
    def deco_hello():
        print("*" * 20)    # 기능 추가
        fn()               # 기존 함수 호출
        print("*" * 20)    # 기능 추가
    return deco_hello

deco_hello = deco(hello)
deco_hello()

********************
hello
********************
```
특정 함수를 입력으로 받아서 해당 함수에 기능을 추가하는 함수를 정의하였다.
***
```
def deco(fn):
    def deco_hello():
        print("*" * 20)    # 기능 추가
        fn()               # 기존 함수 호출
        print("*" * 20)    # 기능 추가
    return deco_hello

@deco
def hello2():
    print("hello 2")
hello2()

********************
hello 2
********************
```
`@데코레이터함수이름`를 사용하여 간단하게 구현할 수 있다.
