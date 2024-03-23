# sort와 sorted의 차이
`sort`는 원본 리스트를 정렬하며, 반환값은 `None`이다.
```
my_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
my_list.sort()
```

<br>

`sorted`는 새로운 리스트를 반환하며, 원본은 유지된다.
```
my_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_list = sorted(my_list)
```

# Params
## key
특정 행에 대하여 key를 사용해 오름차순, 내림차순으로 정렬할 수 있다.
```
data = [[2,2,6],[1,5,10],[4,2,9],[3,8,3]]

sorted_list = sorted(data, key=lambda x: (x[1], -x[0]))
# 1번 인덱스에 대해 오름차순, 0번 인덱스에 대해 내림차순으로 정렬
```

## reverse
boolean값으로 default값은 false. true로 설정시 반대로 정렬한다.

# dictionary sort
## value 기준으로 정렬
```
my_dict = {'a': 4, 'b': 3, 'c': 2, 'd': 1}

sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))

# sorted_dict: {'d': 1, 'c': 2, 'b': 3, 'a': 4}
```
