# 길찾기
## 문제
[리코쳇 로봇](https://school.programmers.co.kr/learn/courses/30/lessons/169199)
### 1. 주어진 크기 만큼의 list 생성 -> 동작 check
```
graph = [[0]*세로 for i in range(가로)]
graph[시작][위치] = 1
```
### 2. queue 생성, 상하좌우 설정
```
from collections import deque
queue = deque()
queue.append((0, 6, 0)) # 시작 위치의 좌표와 움직인 횟수를 추가하기 위한 값

dx = [-1, 1, 0, 0] # up, down
dy = [0, 0, -1, 1] # left, right
```
### 3. queue가 존재할 때까지 반복

```
while queue:
	code
	return answer
return -1
```
### 4. queue에서 원하는 값이 나오도록 설정
```
px, py, cnt = queue.popleft() # 현재 위치와 움직인 횟수
if board[px][py] == 'G': # 목표 지점에 도달
	return cnt
    
# 현재 위치에서 4가지 방향으로 위치 확인
for i in range(4):
	nx, ny = px, py
	while True: # 끝까지 움직여야 하므로 while 추가. 한칸씩 움직이는 경우 필요하지 않음
		nx += dx[i]
        ny += dy[i]   
        
        # 범위를 이탈하거나 장애물을 만난 경우 
		if nx < 0 or nx >= R or ny < 0 or ny >= C or board[nx][ny] == 'D':
			nx -= dx[i]
			ny -= dy[i] # 한 칸씩 뒤로
			break
	if graph[nx][ny] == 0: # 한번도 방문한 적이 없다면
		graph[nx][ny] = 1
		queue.append((nx, ny, cnt + 1))
```
### 전체 코드
```
from collections import deque

def solution(board):
    answer = 0
    row = len(board)
    col = len(board[0])
    start_x, start_y = 0, 0
    for i in range(row):
        for j in range(col):
            if board[i][j]=='R':
                start_x, start_y = i, j
                
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    queue = deque()
    queue.append((start_x, start_y, 0))
    
    graph = [[0]*col for _ in range(row)]
    graph[start_x][start_y] = 1
        
    while queue:
        px, py, cnt = queue.popleft()
        if board[px][py] == 'G':
            return cnt
        for i in range(4):
            nx, ny = px, py
            while True:
                nx += dx[i]
                ny += dy[i]
                if nx < 0 or nx >= row or ny < 0 or ny >= col or board[nx][ny] == 'D':
                    nx -= dx[i]
                    ny -= dy[i]
                    break
            if not graph[nx][ny]:
                graph[nx][ny] = 1
                queue.append((nx, ny, cnt+1))
    return -1
```
# 구역 찾기
## 문제
[석유 시추](https://school.programmers.co.kr/learn/courses/30/lessons/250136)
### 전체 코드
```
from collections import deque

def solution(land):
    row = len(land)
    col = len(land[0])
    col_num = [0] * col

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for i in range(row):
        for j in range(col):
            if land[i][j] == 1:
                start_x, start_y = i, j
                land[i][j] = 0

                queue = deque()
                queue.append((start_x, start_y))

                cnt = 1
                line = []

                while queue:
                    px, py = queue.popleft()
                    if py not in line:
                        line.append(py)
                    for k in range(4):
                        nx, ny = px, py 
                        nx += dx[k]
                        ny += dy[k]      
                        if not (nx < 0 or nx >= row or ny < 0 or ny >= col):
                            if land[nx][ny] == 1:
                                land[nx][ny] = 0
                                queue.append((nx, ny))
                                cnt += 1                    

                for line_num in line:
                    col_num[line_num] += cnt

                cnt = 1
                line = []
    answer = max(col_num) 
    return answer
```
## 구역 찾기 - 2
## 문제
[무인도 여행](https://school.programmers.co.kr/learn/courses/30/lessons/154540)
### 문자열 변환
```
# maps = ["X591X","X1X5X","X231X", "1XXX1"]
new_maps = []
for map_str in maps:
    new_maps.append(list(map_str))
```
사용하기 편하게 미리 list로 변형
### 전체 코드
```
from collections import deque

def solution(maps):
    answer = []
    row = len(maps)
    col = len(maps[0])

    new_maps = []
    for map_str in maps:
        new_maps.append(list(map_str))

    queue = deque()

    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    for i in range(row):
        for j in range(col):
            if new_maps[i][j] != "X":
                start_x, start_y = i, j
                cnt = int(new_maps[i][j])
                queue.append((start_x, start_y))
                new_maps[i][j] = "X"

                while(queue):
                    cx, cy = queue.popleft()
                    for k in range(4):
                        nx = cx + dx[k]
                        ny = cy + dy[k]

                        if not (nx < 0 or nx >= row or ny < 0 or ny >= col):
                            if new_maps[nx][ny] != "X":
                                cnt += int(new_maps[nx][ny])
                                queue.append((nx, ny))
                                new_maps[nx][ny] = "X"

                answer.append(cnt)
                queue = deque()
    
    return sorted(answer) if answer else [-1]
```
