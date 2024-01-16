# **`combinations(iterable, r)` - 조합 생성:**
```
from itertools import combinations

data = [1, 2, 3]

nCr = combinations(data, r=2)
# (1, 2), (1, 3), (2, 3)
```
첫번째 인자에 대한 r가지 조합을 반환한다.

`combinations`를 포함한 모든 객체는 itertools 객체이다. 값 자체를 for문을 사용하여 순회할 수는 있지만, 직접 확인하기 위해서는
`list()`를 사용해야 한다.

# **`permutations(iterable, r=None)` - 순열 생성:**
```
from itertools import permutations

data = [1, 2, 3]

nPr = permutations(data, r=2)
# (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)
```

# **`product(*iterables, repeat=1)` - 카르테시안 곱 생성:**
## 두개의 iterable 객체를 생성하는 경우
```
from itertools import product

numbers = [1, 2, 3]
colors = ['red', 'green']
cartesian_product = product(numbers, colors)
# (1, 'red'), (1, 'green'), (2, 'red'), (2, 'green'), (3, 'red'), (3, 'green')
```
## 하나의 iterable에 대해 생성하는 경우
```
from itertools import product

numbers = [1, 2]
cartesian_product = product(numbers, repeat=2)
# (1, 1), (1, 2), (2, 1), (2, 2)
```
조합과 순열과 다르게 가변인자가 존재하므로 `repeat=n`으로 지정해야 한다.

product를 사용하여 모든 경우의 수를 얻을 수 있다.

# **`count(start=0, step=1)` - 무한한 수열 생성:**
```
from itertools import count

for num in count(start=1, step=2):
   print(num)

# 1, 3, 5, ...
```
이 코드는 1부터 시작해서 2씩 증가하는 무한한 홀수 수열을 생성한다.

# **`cycle(iterable)` - 반복 가능한 객체 무한히 반복:**
```
from itertools import cycle

colors = ['red', 'green', 'blue']
color_cycle = cycle(colors)

for _ in range(10):
   print(next(color_cycle))

# red, green, blue, red, green, blue, red, green, blue, red
```

# **`repeat(element, times=None)` - 원소를 반복:**
```
from itertools import repeat

for num in repeat(2, times=3):
   print(num)

# 2, 2, 2
```

# **`chain(*iterables)` - 여러 iterable 합치기:**
```
from itertools import chain

list1 = [1, 2, 3]
tuple1 = (4, 5, 6)
set1 = {7, 8, 9}

combined = chain(list1, tuple1, set1)
print(list(combined))

# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```
