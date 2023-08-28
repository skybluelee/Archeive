# 이터레이터
파이썬에서 리스트, 튜플, 딕셔너리와 같은 기본 자료 구조는 `for, while`을 사용하여 반복 가능한데, 이러한 객체를 **이터러블**하다고 한다.

파이썬의 어떤 객체가 `__iter__` 메소드를 포함하고 있다면 해당 객체를 이터러블 객체라고 부르고, `__next__` 메소드를 포함하고 있다면 해당 객체를 이터레이터 객체라고 부른다.
## 이터레이터 객체 생성
```
class Season:
    def __init__(self):
        self.data = ["봄", "여름", "가을", "겨울"]
        self.index = 0

    def __iter__(self):
        return self # 자기 자신을 리턴

    def __next__(self):
        if self.index < len(self.data):
            cur_season = self.data[self.index]
            self.index += 1
            return cur_season
        else:
            raise StopIteration
            
s = Season()      # 클래스 객체 생성
for i in s:
    print(i)
    
봄
여름
가을
겨울 
```
이터레이터 객체를 만들 때 `__iter__, __next__` 메소드를 구현해야 한다. `__iter__` 메소드는 이터레이터 객체를 리턴해야 하는데, 현재 클래스 자기 자신이 이터레이터 객체이므로 자기 자신을 리턴한다.

Season 클래스의 객체를 생성한 후 `iter` 내장 함수를 호출하여 이터레이터 객체를 얻는다. 그 다음 이터레이터 객체에 대해 `next` 내장 함수를 호출하여 반복적으로 값을 얻는다.
