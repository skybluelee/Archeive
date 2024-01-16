# 각 자릿수의 정보가 필요한 경우
## 문제
[마법의 엘리베이터](https://school.programmers.co.kr/learn/courses/30/lessons/148653)

### `/=` 사용
기존 자릿수가 필요하지 않은 경우 `/=` 혹은 `//=`을 사용하여 크기를 줄이고 `num % 10`으로 새로운 자릿수를 구할 수 있다.

### 전체 코드
```
from collections import deque
def solution(storey):
    answer = []
    queue = deque([[storey, 0]])

    while queue:
        temp = queue.popleft()
        num, cnt = temp[0], temp[1]
        
        if num / 10 < 1:
            if num <= 5:
                cnt += num
            else: # 앞자리가 6 이상인 경우 자리를 올리고 빼는게 빠름
                cnt += 1 + 10 - num
            answer.append(cnt)
            
        else:
            if num % 10 < 5:
                cnt += num % 10
                num -= num % 10
                num /= 10
                queue.append([num, cnt])
            elif num % 10 > 5:
                cnt += 10 - (num % 10)
                num += 10 - (num % 10)
                num /= 10
                queue.append([num, cnt])
            else:
                cnt += 5
                num1 = num + 5
                num1 /= 10
                num2 = num - 5
                num2 /= 10
                queue.append([num1, cnt])
                queue.append([num2, cnt])
        
    return min(answer)
```
