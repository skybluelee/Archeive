# 메서드
## heapify
```
import heapq

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
heapq.heapify(data)

# data: [1, 1, 2, 3, 3, 9, 4, 6, 5, 5, 5]
```

## heappush
```
import heapq

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
heapq.heappush(data, 7)

# data: [1, 1, 2, 3, 3, 9, 4, 6, 5, 5, 5, 7]
```

## heappop
```
smallest = heapq.heappop(data)

# smallest: 1
# data: [1, 3, 2, 6, 3, 9, 4, 7, 5, 5, 5]
```
힙이 비어있을 경우 `IndexError`가 발생한다.

## heappushpop
```
result = heapq.heappushpop(data, 2)

# result: 1
# data: [2, 3, 4, 6, 3, 9, 5, 7, 5, 5, 5]
```
`heappush()`와 `heappop()`의 순서대로 실행하는 메서드이다.

## heapreplace
```
result = heapq.heapreplace(data, 7)

# result: 2
# data: [3, 3, 4, 6, 5, 9, 5, 7, 5, 8, 5]
```
`heappop()`과 `heappush()`의 순서대로 실행하는 메서드이다.

# 최댓값
`heapq` 모듈은 최소 힙(min heap)을 기반으로 동작하며, 최솟값을 빠르게 가져오기 위한 것으로, 기본적으로는 최댓값을 가져오는 기능은 없다.

이때 값에 -1을 곱하여 쉽게 최댓값을 가져올 수 있다.
```
heap = []

for e in data:
    heappush(heap, -e)

max_value = -1 * heapq.heappop(data)
```
