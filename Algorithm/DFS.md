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

# 모든 경우의 수가 필요한 경우

## 문제
[이모티콘 할인행사](https://school.programmers.co.kr/learn/courses/30/lessons/150368)

### 정석 dfs
**출처: [junyeong.log](https://velog.io/@yohan11/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-Lv2.-%EC%9D%B4%EB%AA%A8%ED%8B%B0%EC%BD%98-%ED%95%A0%EC%9D%B8%ED%96%89%EC%82%AC-Python-%ED%8C%8C%EC%9D%B4%EC%8D%AC)**
```
emoticons = [1300, 1500]
data = [10, 20, 30, 40]
discount = []
def dfs(temp, depth):
    if depth == len(temp):
        discount.append(temp[:])
        return
    for d in data:
        temp[depth] += d
        dfs(temp, depth + 1)
        temp[depth] -= d

dfs([0] * len(emoticons), 0)
```
```
dfs # 1
temp = [10, 0]
-> dfs # 2-1
temp = [10, 10]
-> discount.append(temp[:])
-> dfs # 2-1번 종료(return)

-> dfs # 1
temp = [10, 0]
-> dfs # 2-2
temp = [10, 20]
-> discount.append(temp[:])
-> dfs # 2-2번 종료(return)

-> dfs # 1
temp = [10, 0]
-> dfs # 2-3
temp = [10, 30]
...
```

#### `temp[:]`
`[:]`를 사용하는 이유는 리스트를 복사하여 새로운 객체를 만들기 위해서로, 파이썬에서 리스트의 할당(`=`)은 참조를 복사하는 것이기 때문에, 원래 리스트를 변경하면 참조된 모든 변수에 영향을 미친다.
`[:]`를 사용하여 복사하면 원래 리스트와 완전히 별개의 새로운 리스트가 생성되므로 원래 리스트의 변경이 새로운 리스트에 영향을 미치지 않는다.

따라서 `discount.append(temp[:])`는 `temp` 리스트의 현재 상태를 복사하여 `discount` 리스트에 추가한다.
이로써 `discount` 리스트에는 각 할인 조합에 대한 별도의 리스트가 저장되어, 나중에 `temp` 리스트를 변경하더라도 `discount` 리스트에는 영향을 주지 않는다.

### 전체 코드
```
def solution(users, emoticons):
    answer = [0, 0]
    data = [10, 20, 30, 40]
    discount = []

    def dfs(temp, depth):
        if depth == len(temp):
            discount.append(temp[:])
            return
        for d in data:
            temp[depth] += d
            dfs(temp, depth + 1)
            temp[depth] -= d

    dfs([0] * len(emoticons), 0)

    for d in range(len(discount)):
        plus_user = 0
        profit = 0

        for user in users:
            emoticon_buy = 0
            for i in range(len(emoticons)):
                if discount[d][i] >= user[0]:
                    emoticon_buy += emoticons[i] * ((100 - discount[d][i]) / 100)
            if user[1] <= emoticon_buy:
                plus_user += 1
            else:
                profit += emoticon_buy

        if answer[0] < plus_user:
            answer = [plus_user, int(profit)]
        elif answer[0] == plus_user:
            if answer[1] < profit:
                answer = [plus_user, int(profit)]

    return answer
```

### 순열, 조합, 곱
```
data = [10, 20, 30, 40]
discount = []

# 이모티콘 할인율 구하기
def dfs(temp, depth):
    if depth == len(temp):
        discount.append(temp[:])
        return
    for d in data:
        temp[depth] += d
        dfs(temp, depth + 1)
        temp[depth] -= d
```
위 코드는 모든 순열을 dfs를 사용하여 구하는 코드이다. 이 경우
```
data = [10, 20, 30, 40]

prod = itertools.product(data, 2)
discount = list(prod)
```
permutations 혹은 combinations를 사용하는 것이 효율성 측면에서 더 좋다.

### 전체 코드
```
from itertools import product
def solution(users, emoticons):
    answer = [0, 0]
    data = [10, 20, 30, 40]

    prod = product(data, repeat=len(emoticons))    
    discount_list = list(prod)
    
    for discount in discount_list:
        service, price = 0, 0
        for user in users:   
            user_price = 0
            for idx in range(len(emoticons)):
                if discount[idx] >= user[0]:
                    user_price += emoticons[idx] * (100 - discount[idx]) / 100                
                if user_price >= user[1]:
                    service += 1
                    user_price = 0
                    break
            price += user_price

        if service > answer[0]:
            answer[0] = service
            answer[1] = price
        elif service == answer[0] and price > answer[1]:
            answer[1] = price
            
    return answer
```
