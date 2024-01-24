# 원을 그리고 해당 범위 내의 값을 찾는 경우

## 문제
[점 찍기](https://school.programmers.co.kr/learn/courses/30/lessons/140107)

### 간단 설명
특정 거리에 있는 좌표의 개수 구하기

### stack 사용
각 좌표에 대해 for를 사용하지 않고 최댓값까지 있는 stack을 만들고, 해당 stack에서 pop하며 거리와 비교
```
for i in range(0, d+1, k):
    l = (float(d)**2 - float(i)**2) ** (1/2)
    temp = pos[-1]
    
    if temp > l:
        while temp > l:
            temp = pos.pop()
            len_pos -= 1
```

### type 변경
문제에 대해 int 범위에 대해 overflow가 발생하는지 확인

### 전체 코드
```
def solution(k, d):
    answer = 0
    pos = []
    
    len_pos = 0
    while(len_pos*k <= d):
        pos.append(len_pos*k)
        len_pos += 1
    
    for i in range(0, d+1, k):
        l = (float(d)**2 - float(i)**2) ** (1/2)
        temp = pos[-1]
        
        if temp > l:
            while temp > l:
                temp = pos.pop()
                len_pos -= 1
            pos.append(temp)
            len_pos += 1
        
        answer += len_pos        

    return answer
```
