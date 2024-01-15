# 리스트의 끝까지 확인하는 경우

## 문제
[택배 배달과 수거하기](https://school.programmers.co.kr/learn/courses/30/lessons/150369)

### 1. 리스트 위치 확인
반드시 리스트의 처음부터 시작해야 하는지 확인한다.
```
deliveries = deliveries[::-1]
pickups = pickups[::-1]
```
리스트의 마지막부터 확인해도 된다면 순서를 뒤집는 것이 간편할 수도 있다.

### 2. 리스트 순회
```
    for i in range(n):
        have_to_deli += deliveries[i]
        have_to_pick += pickups[i]
        ...
        answer += (n - i) * 2
```
해당 코드는 len(list)의 길이 n이 주어졌다.

for문을 사용하여 전체 리스트를 순회하고, 해당 인덱스의 위치는 `n - i`이다.

### 전체 코드
```
def solution(cap, n, deliveries, pickups):
    deliveries = deliveries[::-1]
    pickups = pickups[::-1]
    answer = 0

    have_to_deli = 0
    have_to_pick = 0

    for i in range(n):
        have_to_deli += deliveries[i]
        have_to_pick += pickups[i]

        while have_to_deli > 0 or have_to_pick > 0:
            have_to_deli -= cap
            have_to_pick -= cap
            answer += (n - i) * 2

    return answer
```
