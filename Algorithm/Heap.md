# 리스트를 순회하면서 리스트의 최댓값과 최솟값을 확인해야 하는 경우

## 문제
[디펜스 게임](https://school.programmers.co.kr/learn/courses/30/lessons/142085)

enemy 리스트를 순회하며 각 값을 n에서 빼거나, k를 사용하여 생략할 수 있다.
해당 과정을 가장 오래 수행한 값을 리턴한다.

**출처: [isayaksh@gmail.com](https://velog.io/@isayaksh/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-Programmers-%EB%94%94%ED%8E%9C%EC%8A%A4-%EA%B2%8C%EC%9E%84-Python)**

### 설명
최대한 숫자가 큰 값을 k를 사용하여 스킵해야 한다.

heap을 사용하는 경우 최솟값을 쉽게 확인할 수 있다. 이 특성을 사용하여 heap에 값 * -1하여 push하고, 최솟값을 제거한다(결과적으로는 최댓값을 제거).

### 1. heap push
heap은 기본적으로 최솟값만을 제거하도록 설계된 알고리즘이다. 인자를 설정하여 최댓값으로 동작하게 만들 수 없다.

따라서 기존 값에 -1을 곱하여 push한다.
```
for e in enemy:
    heappush(heap, -e)
    sumEnemy += e
```

### 2. 최댓값 제거
리스트 순회하며 값을 더하고, 특정 값이 n을 넘는다면, 최댓값을 제거한다.
```
heap: [-4, -2, -5] -> [-4, -2]
total -= 5
```
heap에서의 최솟값은 리스트의 최댓값으로 이를 제거하고, 전체 합에서 해당 값을 빼면 처음부터 k를 사용하지 않다고, 최댓값에 대해서만 k를 사용한 것과 같다.

### 전체 코드
```
from heapq import heappop, heappush

def solution(n, k, enemy):
    answer, sumEnemy = 0, 0
    heap = []
    
    for e in enemy:
        heappush(heap, -e)
        sumEnemy += e
        if sumEnemy > n:
            if k == 0: break
            sumEnemy += heappop(heap) 
            k -= 1
        answer += 1
    return answer
```
