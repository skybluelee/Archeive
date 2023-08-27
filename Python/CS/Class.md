# 클래스
클래스는 데이터와 데이터를 조작하는 메서드를 함께 묶어서 정의하는 것으로, 객체를 생성하기 위한 템플릿 역할을 하며, 객체는 클래스의 인스턴스(Instance)이다.

클래스를 사용하면 객체 지향 프로그래밍의 주요 개념 중 하나인 캡슐화, 상속, 다형성 등을 구현할 수 있다. 클래스를 사용하면 코드를 더 모듈화하고 재사용 가능한 구성 요소를 만들 수 있어서 코드의 가독성과 유지 보수성을 향상시키는 데 도움이 된다.

객체들은 클래스에서 정의한 성질을 그대로 이어받으나 함수와 달리 서로 독립적이기 때문에 다수의 객체를 생성한다면 클래스는 함수보다 유용하다.
## 클래스 정의
클래스는 데이터와 이를 처리하는 메서드(함수)로 구성된다.
```
class Person:
    pass

p = Person()
```
위의 경우 메모리에 2개의 객체가 생성된다. Person이라는 클래스 이름은 클래스 객체를 바인딩하고, p라는 변수는 Person 클래스 타입의 객체를 바인딩한다.

클래스와 객체는 각자 고유의 메모리 공간을 갖는다.
## 클래스와 변수
```
class Person:
    pass

p = Person()
p.data = 3
```
해당 객체에 변수를 선언하면 `p`라는 객체에 `{"data": 3}`이라고 저장된다.
***
```
class Person:
    data = 4

p = Person()
```
반면 위와 같이 클래스 내부에서 객체를 선언한다면 `Person`이라는 클래스 객체에 `{"data": 4}`라고 저장된다.
## self
self
- self는 인스턴스 메서드에서 사용되는 첫 번째 매개변수로, 해당 메서드가 호출된 인스턴스 자체를 나타낸다.
- 클래스의 모든 인스턴스 메서드에서 self를 첫 번째 매개변수로 사용해야 한다. 이를 통해 메서드 내부에서 해당 인스턴스의 속성 및 메서드에 접근할 수 있다.
- self를 사용하여 인스턴스 변수를 정의하고 접근하거나, 다른 인스턴스 메서드를 호출할 수 있다.

cls
- cls는 클래스 메서드에서 사용되는 첫 번째 매개변수로, 해당 메서드가 속한 클래스 자체를 나타낸다.
- 클래스 메서드는 클래스 수준에서 동작하며, 인스턴스와 관련이 없는 작업을 수행할 때 사용된다.
- cls를 사용하여 클래스 변수에 접근하거나, 다른 클래스 메서드를 호출할 수 있다.
## 생성자
일반적으로 함수는 사용자가 `함수이름()` 형태로 호출해야 코드가 수행된다.

클래스의 경우 특별한 이름`__init__`을 갖기만 하면 객체가 생성될 때 자동으로 호출하는 함수가 있는데, 이를 생성자라고한다.
```
class Person:
    def __init__(self):
        print("태어남..")

p = Person()

태어남..
```
클래스의 객체가 생성됨과 동시에 `__init__`이 실행되어 값이 출력된다.
## 생성자를 이용한 객체 count
```
class MyClass:
    count = 0

    def __init__(self):
        MyClass.count += 1

    def get_count(self):
        return MyClass.count

a = MyClass()
b = MyClass()
c = MyClass()

print(a.get_count())
print(MyClass.count)

3
3
```
객체 a, b, c가 생성될 때마다 생성자 조건에서 count를 + 1하였고, 최종 count 값인 3을 출력한다. 

이때 함수를 통해 출력할 수도 있고 return 값을 직접 참조하여 출력할 수 있다.
# 매직 메소드
클래스 안에 정의된 함수를 메소드라고 부른다. 이 중에서도 `__`로 시작해서 `__`로 끝나는 메소드들이 있는데, 이를 매직 메소드 또는 특별 메소드라고 부른다.

위에서 설명한 `__init__` 또한 생성자라고 부르는 매직 메소드 중 하나이다.
## `__call__`
```
class MyFunc:
    def __call__(self, *args, **kwargs):
        print("call")


f = MyFunc()
f()

call
```
클래스의 객체에 `()`를 붙이면 `__call__`이 실행된다.
## `__getattribute__`
```
class Stock:
    def __getattribute__(self, item):
        print("data is", item)


s = Stock()
s.apple

data is apple
```
객체에 `.`을 사용하여 접근하는 경우 `__getattribute__` 메직 메소드를 호출한다.
## `__new__`
```
class MyClass:
    def __new__(cls):
        instance = object.__new__(cls)
        print("Creating a new instance")
        return instance
    
    def __init__(self):
        print("Initializing the instance")
        
Creating a new instance
Initializing the instance
```
`__new__` 메소드는 객체를 생성하는데 사용되는 매직 메소드이다. 이 메서드는 클래스의 인스턴스를 생성하고 초기화하기 전에 호출된다. 즉, 객체가 실제로 생성되기 전에 호출되므로 `__init__` 메서드보다 먼저 실행된다.

일반적으로 `instance = super(MyClass, cls).__new__(cls)`를 사용하여 슈퍼 클래스(부모 클래스)에 대한 클래스 객체를 얻는데, 슈퍼 클래스가 존재하지 않는 경우 `object`를 사용할 수 있다.

`object` 클래스는 파이썬의 모든 클래스의 기본 슈퍼 클래스이다. 파이썬에서 새로운 클래스를 정의할 때 명시적으로 다른 클래스를 상속하지 않는다면, 그 클래스는 자동으로 `object` 클래스를 상속받는다.
## `__del__`
```
class MyClass:
    def __init__(self, value):
        self.value = value

    def __del__(self):
        print(f"Object with value {self.value} is being destroyed")

obj1 = MyClass(42)
del obj1

Object with value 42 is being destroyed
```
obj1 객체가 제거되었다.

`__del__` 메소드는 객체가 메모리에서 소멸될 때 호출되는 메소드이다.

객체가 더 이상 참조되지 않을 때(즉, 객체를 가리키는 변수나 참조가 없을 때) 이 메서드가 호출되며, 객체를 메모리에서 제거하기 직전에 실행된다.

객체 소멸 시에 메모리 누수(memory leak)나 예기치 않은 동작을 유발할 수 있으므로, 신중하게 사용해야한다.
## `__str__`
```
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

person = Person("Alice", 30)

str_representation = str(person) # __str__ 메소드 사용
print(str_representation)

Person(name=Alice, age=30)
```
`__str__` 메소드는 객체를 문자열로 표현하는데 사용된다.

person이라는 객체에 name, age 변수가 선언되었고, `str` 함수를 통해 `__str__` 메소드를 사용하여 `f"Person(name={self.name}, age={self.age})"` 값을 리턴하였다.

이후 `print(str_representation)`를 통해 `__str__` 메소드가 사용된 것을 확인할 수 있다.
***
추가로 `print`는 내부적으로 `__str__` 메소드를 호출한다.
```
a = 1
b = 'person'
c = ['a', 1]
print(a,b,c)

1 person ['a', 1]
```
`__str__` 메소드의 경우 서로 다른 타입을 가진 데이터도 동일하게 문자열로 변환시키는 특징이 있다.
## `__repr__`
```
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

point = Point(2, 3)
print(repr(point))  # 출력: Point(x=2, y=3)

Point(x=2, y=3)
```
`__repr__`와 `__str__` 사용 방식과 문자열로 변환한다는 점은 동일하다.

차이점으로는
- `__repr__` 메소드는 객체의 "공식적인(representational)" 문자열 표현을 제공하는 데 사용된다.
- 주로 디버깅 및 객체의 상태 확인을 위한 목적으로 사용된다.

단순 문자열이 아니라 주로 사용되는 변수를 확인하는 용도로 사용된다고 해석하면 될 듯 하다.
## `__iter__`
```
class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        return self  # 자기 자신을 이터레이터로 반환

    def __next__(self):
        if self.start >= self.end:
            raise StopIteration  # 이터레이션 종료 예외
        current = self.start
        self.start += 1
        return current

my_range = MyRange(1, 5)
for num in my_range:
    print(num)

1
2
3
4
```
`__iter__`는 객체를 반복 가능한(iterable) 객체로 만들기 위해 정의된다. `__iter__`메서드는 주로 컬렉션 형태의 객체에서 사용되며, 객체가 반복 가능한 요소를 제공할 때 호출된다.

`__iter__` 메소드는 일반적으로 `self`를 직접 반환하지 않고 `self` 객체에 대한 이터레이터(iterator)를 생성하여 반환하는 것이 일반적인데, 이는 `self`를 직접 반환하는 경우 객체가 무한루프에 빠지는 것을 방지하기 위함이다.
### `__next__`
`__iter__` 를 사용할 때 같이 사용되며, 이터레이션을 통해 다음 값을 반환하는 역할을 한다.

`__next__` 메소드는 이터레이터(iterator) 객체에서 호출되며, 다음 요소를 반환하거나 이터레이션을 종료하기 위한 StopIteration 예외를 발생시킨다.
## `__len__`
```
class MyList:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def append(self, value):
        self.data.append(value)

my_list = MyList()
my_list.append(1)
my_list.append(2)
my_list.append(3)

length = len(my_list)
print(length)

3
```
`__len__` 메소드는 객체의 길이(크기)를 반환하는 역할을 한다.
## `__bool__`
```
class NonEmptyList:
    def __init__(self, data):
        self.data = data

    def __bool__(self):
        return len(self.data) > 0

my_list = NonEmptyList([1, 2, 3])

if my_list:
    print("my_list is not empty")
else:
    print("my_list is empty")

my_list is not empty    
```
`__bool__` 메소드는 객체를 불리언 값(True 또는 False)으로 평가할 때 호출되는 메서드이다.

`__bool__` 메소드는 True 또는 False를 반환한다. `__bool__` 메소드는 선택적으로 정의가 가능하며 `__bool__` 메소드가 정의되지 않았다면`__len__` 메소드를 사용하여 객체의 길이가 0인지 아닌지를 판단하여 불리언 값을 결정한다. `__bool__` 메소드가 정의되어 있다면 `__len__` 메소드는 무시된다.
## `__add__`, `__sub__`, `__mul__`, `__truediv__`
각각 `+, -, *, /` 연산을 수행하는 메소드이다.
```
class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        real_part = self.real + other.real
        imag_part = self.imag + other.imag
        return ComplexNumber(real_part, imag_part)

    def __str__(self):
        return f"{self.real} + {self.imag}i"

num1 = ComplexNumber(1, 2)
num2 = ComplexNumber(3, 4)

result = num1 + num2
print(result)

4 + 6i
```
클래스로 생성한 객체끼리 연산이 가능하도록 만들어 준다.
# 추상 클래스
객체 지향 프로그래밍에서 추상 클래스(abstract class)란 메소드 구현 없이 메소드의 이름만 존재하는 클래스이다. 보통 객체 지향 설계에서 부모클래스에 메소드만 정의하고 이를 상속받은 클래스가 해당 메소드를 반드시 구현하도록 강제하기 위해 사용한다.
```
from abc import *


class Car(metaclass=ABCMeta):
    @abstractmethod
    def drive(self):
        pass


class K5(Car):
    pass

k5 = K5()
```
위의 경우 `@abstractmethod`를 사용하여 Car 클래스를 상속받은 모든 클래스가 drive() 메소드를 정의하는 것을 강제한다. 따라서 위 코드를 실행하면 객체 생성시 오류가 발생한다.
```
from abc import *


class Car(metaclass=ABCMeta):
    @abstractmethod
    def drive(self):
        pass


class K5(Car):
    def drive(self):
        print("k5 drive")

k5 = K5()
```
drive() 메소드를 구현하면 정상적으로 객체가 생성되고 메소드도 호출된다.
