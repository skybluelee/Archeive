# collections.deque

## 초기화
```
from collections import deque

deque_example = deque([1, 2, 3])
```

## append
```
deque_example.append(4)      # [1, 2, 3, 4]
deque_example.appendleft(0)  # [0, 1, 2, 3, 4]
```

## pop
```
popped_element = deque_example.pop()        # popped_element = 4, deque_example = [0, 1, 2, 3]
leftmost_element = deque_example.popleft()  # leftmost_element = 0, deque_example = [1, 2, 3]
```

## extend
```
deque_example.extend([5, 6, 7])           # deque_example = [1, 2, 3, 5, 6, 7]
deque_example.extendleft([-1, 0])          # deque_example = [0, -1, 1, 2, 3, 5, 6, 7]
```

## rotate
```
deque_example.rotate(2)    # deque_example = [6, 7, 0, -1, 1, 2, 3, 5]
deque_example.rotate(-3)   # deque_example = [1, 2, 3, 5, 6, 7, 0, -1]
```

# defaultdict

## type 초기화
```
from collections import defaultdict

default_dict = defaultdict(int)
default_dict2 = defaultdict(list)

default_dict[0] += 1          # {0: 1}
default_dict2[0].append(1)    # {0: [1]}
```

## lambda를 통한 초기화
```
from collections import defaultdict

default_dict_lambda = defaultdict(lambda: -1)
default_dict_lambda2 = defaultdict(lambda: [1])

default_dict_lambda[0] += 1          # {0: 0}
default_dict_lambda2[0].append(1)    # {0: [1, 1]}
```

# Counter

## 초기화
```
from collections import Counter

my_list = [1, 2, 3, 1, 2, 3, 4, 5]
my_counter = Counter(my_list)         # Counter({1: 2, 2: 2, 3: 2, 4: 1, 5: 1})
```

## most_common
```
common_elements = my_counter.most_common(2)      # [(1, 2), (2, 2)]
```

## 합, 차
```
another_list = [1, 2, 3, 1, 2]
another_counter = Counter(another_list)

combined_counter = my_counter + another_counter
subtracted_counter = my_counter - another_counter

print(combined_counter)
# Counter({1: 3, 2: 3, 3: 3, 4: 1, 5: 1})

print(subtracted_counter)
# Counter({3: 2, 4: 1, 5: 1})
```

## dict 메서드
Counter는 dictionary는 아니지만, 형태가 유사하며 동일한 메서드를 사용한다.

## 값 확인
```
from collections import Counter

my_list = [1, 2, 3, 1, 2, 3, 4, 5]
my_counter = Counter(my_list)         # Counter({1: 2, 2: 2, 3: 2, 4: 1, 5: 1})

count_of_2 = my_counter[2]            # count_of_2: 2
```

## keys, values, items
```
from collections import Counter

my_list = [1, 2, 3, 1, 2, 3, 4, 5]
my_counter = Counter(my_list)        # Counter({1: 2, 2: 2, 3: 2, 4: 1, 5: 1})

keys = my_counter.keys()             # dict_keys([1, 2, 3, 4, 5])

values = my_counter.values()         # dict_values([2, 2, 2, 1, 1])

items = my_counter.items()           # dict_items([(1, 2), (2, 2), (3, 2), (4, 1), (5, 1)])
```
