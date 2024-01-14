# 중복 값 제거
queue 내부에 기존의 중복값이 존재하는 경우 queue를 사용하더라도 효율성 문제가 발생할 수 있다.

## 문제
[숫자 변환하기](https://school.programmers.co.kr/learn/courses/30/lessons/154538)

## set을 사용한 중복값 제거
```
num_set = set()

if value not in num_set:
    num_set.add(value)
else:
    pass
```
set 이외에도 딕셔너리나 리스트를 사용할 수도 있다.

## 전체 코드
```
from collections import deque
def solution(x, y, n):
    num_set = set()
    answer = -1
    
    if x == y:
        return 0
    
    queue = deque()
    queue.append([x,0])
    
    while queue:
        temp = queue.popleft()
        num, cnt = temp[0], temp[1]
        cnt += 1
        
        num1 = num + n
        num2 = num * 2
        num3 = num * 3        
        
        if y in [num1, num2, num3]:
            answer = cnt
            break
        else:
            if num1 < y and num1 not in num_set:
                num_set.add(num1)
                queue.append([num1, cnt])
            if num2 < y and num2 not in num_set:
                num_set.add(num2)
                queue.append([num2, cnt])
            if num3 < y and num3 not in num_set:
                num_set.add(num3)
                queue.append([num3, cnt])
    return answer
```
