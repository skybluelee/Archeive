# 컬렉션 종류
- 리스트(list)
  - 순서가 있는 요소들의 모임
  - 한번 선언하면 크기를 바꿀 수 없는 배열과 달리 크기가 변할 수 있음
- 셋(set)
  - 중복이 없는 컬렉션
  - 기본적으로 순서가 없음
- 맵(map)
  - 키와 값의 쌍으로 이루어진 요소들의 컬렉션
  - 키는 중복 불가능, 값은 중복 가능
  - 키마다 값이 존재함
# List
## ArrayList
가장 많이 사용되는 컬렉션 클래스로, 요소들을 들어오는 순서대로 저장한다.

초기 공간은 10으로 설정되어 있으며, 공간이 더 필요하면 동적으로 공간을 확보한다.

각 요소들로 접근이 빠르다는 장점이 있으나, 요소 추가/제거 시(append, pop 제외) 성능 부하 문제, 메모리 문제라는 단점이 있어, 변경이 드물고 빠른 접근이 필요한 곳에 적합하다.
```
public class Main {
    public static void main(String[] args) {
        ArrayList<Integer> ints1 = new ArrayList<>(); // ints1: size = 5 - 11
        ArrayList<String> strings = new ArrayList<>();                   - 22
        ArrayList<Number> numbers = new ArrayList<>();                   - ...

        ints1.add(11);
        ints1.add(22);
        ints1.add(33);
        ints1.add(44);
        ints1.add(55);

        //  for-each 문 사용 가능
        for (int i : ints1) {
            System.out.println(i);
        }
    }        
}
```
제네릭을 사용하여 타입을 지정한다. `ArrayList<Integer>`는 정수 리스트이고, 아래로 문자열, 숫자(실수)를 담는 리스트이다.
### 단순 메소드
- `size()`
    - 리스트의 개수를 구함
- `isEmpty()`
    - 빈 리스트면 true 반환
- `get(n)`
    - 리스트의 n번째 요소 반환
- `contains(<value>)`
    - 리스트에 값이 존재하면 true 반환
- `set(n, <value>)`
    - n번째 요소의 값을 value로 교체함
- `add(<value>)`
    - 리스트에 값을 추가함. `append`와 동일
- `add(n, <value>)`
    - n번째 자리에 value를 추가함. n+1 번째 자리부터는 값이 밀려남
    - [0, 1, 2] -> `add(1, 10)` -> [0, 10, 1, 2]
- `remove(n)`
    - n번째 요소를 제거
- `remove(<data_type> <value>)`
    - 리스트에서 value를 제거
    - value와 동일한 가장 앞의 요소 하나만 제거함
    - Object 클래스이므로 참조형 자료형을 추가 `ints3.remove((Integer) 55);`
- `removeAll(list)`
    - 인자로 주어진 list 내의 요소가 존재할 시 삭제
    - 차집합 개념
    - `ints1.removeAll(ints3);`
- `addAll(list)`
    - 리스트나 콜렉션을 이어 붙임
    - 파이썬의 list + list와 동일
- `clear()`
    - 리스트의 모든 요소를 제거
### 초기화 방식
```
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        ArrayList<Integer> ints2A = new ArrayList<>(
                Arrays.asList(1, 2, 3, 4, 5)
        );

        ArrayList<Integer> ints2B = new ArrayList<>(
                List.of(1, 2, 3, 4, 5)
        );

        ArrayList<Integer> ints2C = new ArrayList<>();
        Collections.addAll(ints2C, 1, 2, 3, 4, 5);
    }        
}
```
### 기존 리스트를 사용하여 새로운 리스트 생성
```
public class Main {
    public static void main(String[] args) {
        // ints1의 내용과 동일한 리스트 ints3 생성
        ArrayList<Integer> ints3 = new ArrayList<>(ints1);

        // clone을 사용하는 경우 얕은 복사임!
        ArrayList<Integer> ints4 = (ArrayList<Integer>) ints3.clone();
    }        
}
```
`clone`은 `Object` 클래스이므로 `clone`을 사용하는 경우 제네릭의 자료형을 명시해야 한다.
### 리스트 -> 배열
```
public class Main {
    public static void main(String[] args) {
        Object[] intsAry2_Obj = ints1.toArray();

        //  Integer[] ints1Ary1 = (Integer[]) ints1.toArray(); // 오류 발생

        Integer[] ints1Ary2 = ints1.toArray(Integer[]::new);
    }        
}
```
`toArray()`를 사용하여 리스트를 배열로 바꿀 수 있다.

`toArray()`를 사용하는 경우 특정 타입의 배열로 반환하기 위해서는 생성자를 추가해야 한다.
## LinkedList
queue를 구현하는 용도로 사용한다.

각 요소들이 이전, 다음 요소들과의 링크(주소)를 가지고 있어 요소를 추가하거나 제거할 때 공간을 옮길 필요가 없다.

요소의 추가와 제거가 빠르다는 장점이 있으나, 요소 접근이 느리다는 단점이 있어, 요소들의 추가와 제거가 잦은 곳에 적합하다.

`ArrayList`와 `LinkedList`는 대부분의 메소드를 공유한다.
### ArrayList에만 있는 메소드
- `ensureCapacity(n)`
    - n개의 자리수를 미리 확보
    - ArrayList는 공간이 필요하기 때문
- `trimToSize()`
    - 남는 공간 제거(메모리 회수)
### LinkedList에만 있는 메소드
- `addFirst(<value>)`
    - 리스트의 왼쪽에 값을 추가함
    - 파이썬의 appendleft와 동일
- `addLast(<value>)`
    - 리스트의 오른쪽에 값을 추가함
- `peekFirst()`
    - 첫번째 요소를 꺼내지 않고 값만 확인하여 리턴함
    - 비어있는 경우 null 반환
- `peekLast()`
    - 마지막 요소를 꺼내지 않고 값만 확인하여 리턴함
    - 비어있는 경우 null 반환
- `getFirst()`
    - 첫번째 요소를 꺼내지 않고 값만 확인하여 리턴함
    - 비어있는 경우 오류 발생
- `getLast()`
    - 마지막 요소를 꺼내지 않고 값만 확인하여 리턴함
    - 비어있는 경우 오류 발생
- `pollFirst()`
    - 첫번째 요소를 꺼내서 리턴함
    - 비어있는 경우 null 반환
- `pollLast()`
    - 마지막 요소를 꺼내서 리턴함
    - 비어있는 경우 null 반환
- `removeFirst()`
    - 첫번째 요소를 꺼내서 리턴함
    - 비어있는 경우 오류 발생
- `removeLast()`
    - 마지막 요소를 꺼내서 리턴함
    - 비어있는 경우 오류 발생
***
**스택 구현**
```
LinkedList<Character> charLList = new LinkedList<>();

charLList.push('A');
charLList.push('B');
charLList.push('C');
charLList.push('D');
charLList.push('E');

char pop1 = charLList.pop();
char pop2 = charLList.pop();
char pop3 = charLList.pop();
```
리스트에 `push()`를 사용하여 A, B, C, D, E 순으로 넣고 `pop()`을 사용하여 E, D, C를 제거하는 스택을 구현할 수 있다.
## ArrayDeque
`LinkedList`의 메소드와 거의 동일하며, 성능이 중요할 때(넣고 꺼내기가 잦을 때) 스택, 큐로의 활용에 보다 적합하다.
# Set
Set은 중복되지 않는 요소들의 집합이다.

|주요 클래스|장점|단점|
|---------|----|----|
|HashSet|성능이 빠르고 메모리 적게 사용|순서 관련 기능 없음|
|LinkedHashSet|요소들을 입력 순서대로 정렬|HashSet보다 성능이 떨어짐|
|TreeSet|요소들을 특정 기준대로 정렬(기본 오름차순)|데이터 추가/삭제에 시간 소모 많음|

## HashSet
```
public class Main {
    public static void main(String[] args) {
        Set<Integer> intHSet1 = new HashSet<>();
        intHSet1.add(1);
        intHSet1.add(1);
        intHSet1.add(2);
        intHSet1.add(3); // intHSet1: [1, 2, 3]

        List<Integer> ints1 = new ArrayList(
                Arrays.asList(1, 1, 2, 2, 3, 3, 4, 5, 6, 7)
        );
        Set<Integer> intHSet2 = new HashSet<>(ints1); // intHSet2: [1, 2, 3]
    }
}
```
HashSet으로 초기화하고 `add()`메소드를 사용하여 값을 추가할 수 있고,

리스트를 생성하고 해당 리스트를 셋으로 만들 수 있다.

결과값으로 중복 요소가 존재하지 않는 것을 확인할 수 있다.
```
ints1.clear();
ints1.addAll(intHSet2);
```
위의 방식으로 list의 unique 값을 set으로 넣고, 해당 리스트를 지우고 set을 add하여 unique값의 리스트를 얻을 수 있다.
### 메소드
- `contains(<value>)`
    - 값과 동일한 요소가 있다면 true 반환
- `remove(<value>)`
    - 값과 동일한 요소가 있다면 지우고 true를 반환, 요소가 없다면 false 반환
    - boolean 메소드임
- `removeAll(Set)`
    - 인자로 주어진 Set의 요소와 동일한 요소를 제거함
    - 차집합 개념
### 클래스
```
public class Main {
    public static void main(String[] args) {
        Set<Swordman> swordmenSet = new HashSet<>();
        Swordman swordman = new Swordman(Side.RED);

        swordmenSet.add(swordman);
        swordmenSet.add(swordman);
        swordmenSet.add(new Swordman(Side.RED));
        swordmenSet.add(new Swordman(Side.RED)); // swordmenSet: size = 3
    }
}
```
set은 인스턴스를 기준으로 중복 요소를 확인한다. 따라서 객체가 동일한 값이더라도 다른 객체라면 중복으로 판단하지 않는다.
### 정렬
정수에 대해 HashSet을 사용한 결과가 마치 값을 정렬한 것처럼 보이는데, 이는 정수를 고유 해시값으로 저장하는 내부적 특성일 뿐, 실제로 정렬되는 것이 아니다.

문자열의 경우 정렬 효과를 볼 수 없다.

일정 개수까지는 정렬 효과가 보이나, 특정 수를 넘으면 정렬이 되지 않으므로 HashSet을 정렬의 목적으로 사용해서는 안된다.
## TreeSet
TreeSet은 요소를 정렬하므로 TreeSet만의 메소드가 존재한다.
### 메소드
```
public class Main {
    public static void main(String[] args) {
        for (int i : new int[] { 5, 1, 9, 3, 7, 2, 6, 10, 4}) {
            intHashSet.add(i);
            intLinkedHashSet.add(i);
            intTreeSet.add(i);
        }
        for (var s : new Set[] intTreeSet) {
            System.out.println(s);
        }

        int firstInt = intTreeSet.first(); // firstInt: 1
        int lastInt = intTreeSet.last();   // lastInt: 10

    }
}
```
- `first()`
    - 최솟값 반환
- `last()`
    - 최댓값 반환
- `pollFirst()`
    - 최솟값 제거
- `pollLast()`
    - 최댓값 제거
- 문자열의 경우
    - `ceiling(<value>)`: 같은 것이 없다면 트리구조상 바로 위의 것 (바로 더 큰 것) 반환
    - `floor(<value>)`: 같은 것이 없다면 트리구조상 바로 아래의 것 (바로 더 작은 것) 반환
- `descendingSet()`
    - 순서가 뒤집힌 Set 반환
### 반드시 필요한 순서
숫자와 문자의 경우 크기를 비교할 수 있기 때문에 TreeSet을 바로 사용할 수 있다.

반면 객체의 경우 크기 비교가 불가능하여 TreeSet을 사용할 수 없는데, 이때 `Comparable` 또는 `Comparator`를 사용하여 비교가 가능하게 만들어 TreeSet을 사용할 수 있다.
# map
key - value 쌍으로 구성되며, 키와 값의 자료형은 제한이 없다. 

키값은 중복될 수 없다. 키가 중복되는 경우 새로운 값이 기존의 값을 대체한다.
```
public class Main {
    public static void main(String[] args) {
        Map<Integer, String> numNameHMap = new HashMap<>();
        numNameHMap.put(1, "spark"); // numNameHMap: 1 -> "spark"
        numNameHMap.put(2, "kafak");                 2 -> "kafka"
        numNameHMap.put(3, "linux");                 3 -> "linux"

        Map<Side, ArrayList<Unit>> sideUnitsHMap = new HashMap<>();
        sideUnitsHMap.put(
                Side.BLUE,
                new ArrayList<>(
                        Arrays.asList(
                                new Swordman(Side.BLUE),
                                new Knight(Side.BLUE),
                                new MagicKnight(Side.BLUE))
                )
        );
    }
}
```
`Map<<key_type>, <value_type>> <map_name> = new <map_type><>();` 형식으로 초기화한다.

numNameHMap의 경우 key를 int로 value를 string인 map이고

sideUnitsHMap의 경우 key로 class 값을, value로 list를 받는다.
## 메소드
- `put(<key>, <value>)`
    - 키와 값을 map에 입력
- `putAll(map)`
    - 인자로 주어진 map의 모든 값을 해당 map에 입력
- `get(<key>)`
    - key를 받아 value를 반환
    - map에 해당 key가 없다면 `null`을 반환
- `containsKey(<key>)`
    - map에 해당 key가 있다면 true
- `containsValue(<value>)`
    - map에 해당 value가 있다면 true
- `getOrDefault(<key>, <defaultValue>)`
    - key가 있다면 value를 반환하고 없다면 defaultValue를 반환
- `remove(<key>)`
    - map에 key가 있다면 해당 요소를 삭제
- `remove(<key>, <value>)`
    - map에 해당 key, value가 있다면 해당 요소를 삭제
- `isEmpty()`
    - map이 비어있다면 true 반환
- `clear()`
    - map의 모든 요소 제거
## key는 중복 불가
```
public class Main {
    public static void main(String[] args) {
        Map<Integer, String> numNameHMap = new HashMap<>();
        numNameHMap.put(1, "spark"); // numNameHMap: 1 -> "spark"
        numNameHMap.put(2, "kafak");                 2 -> "kafka"
        numNameHMap.put(3, "linux");                 3 -> "linux"

       var key_check = numNameHMap.keySet();
        //  keySet을 활용한 for-each
        for (var n : numNameHMap.keySet()) {
            System.out.println(numNameHMap.get(n));
        }
    }
}
```
key의 중복 불가 특성을 사용하여 value를 얻을 수 있다.
`keySet()` 메소드를 사용하여 해당 map의 모든 key를 얻고, key를 for each문의 인자로 사용하여 모든 value를 얻을 수 있다.
## Entry 인터페이스
```
public class Main {
    public static void main(String[] args) {
        Map<Integer, String> numNameHMap = new HashMap<>();
        numNameHMap.put(1, "spark"); // numNameHMap: 1 -> "spark"
        numNameHMap.put(2, "kafak");                 2 -> "kafka"
        numNameHMap.put(3, "linux");                 3 -> "linux"

       Set<Map.Entry<Integer, String>> numNameES = numNameHMap.entrySet();
        for (var entry : numNameES) {
            int key = entry.getKey();
            String value = entry.getValue();
            System.out.printf("k: %d, v: %s%n", key, value);
            System.out.println(entry);
        }
    }
}

k: 1, v: spark
1=spark
k: 2, v: kafak
2=kafak
k: 3, v: linux
3=linux
```
entry 인터페이스는 맵의 각 요소를 갖는다.

map을 entry로 이어 받는 경우 `getKey()`와 `getValue()`를 사용하여 key와 value를 얻을 수 있다.
## TreeMap
TreeMap은 key를 트리 형태로 저장한다.

정렬이 필요없고 빠른 접근이 필요한 경우 HashMap을, key 순으로 정렬이 필요한 경우는 TreeMap을 사용한다.
```
public class Main {
    public static void main(String[] args) {
        TreeMap<Integer, String[]> classKidsTMap = new TreeMap<>();
        classKidsTMap.put(3, new String[] {"q", "w", "e"}); // classKidsTMap: 1 -> ["z", "x", "c"]
        classKidsTMap.put(9, new String[] {"a", "s", "d"});                   3 -> ["q", "w", "e"]
        classKidsTMap.put(1, new String[] {"z", "x", "c"});                   9 -> ["a", "s", "d"]

        int firstKey = classKidsTMap.firstKey(); // firstKey: 1
        int lastKey = classKidsTMap.lastKey();   // lastKey: 9

        int ceil = classKidsTMap.ceilingKey(4);  // ceil: 3
    }
}
```
key의 순서대로 정렬되므로 `firstKey()`와 `lastKey()` 메소드를 통해 첫번째와 마지막 key를 확인할 수 있다.
### 메소드
- `ceilingKey(<key>)`
    - 주어진 key가 없다면 트리구조상 바로 위의 key를 반환
- `floorKey(<key>)`
    - 주어진 key가 없다면 트리구조상 바로 아래의 key를 반환
- `firstEntry()`
    - map의 첫번째 요소를 반환
    - Map.Entry<Integer, String[]> firstEntry = classKidsTMap.firstEntry(); // classKidsTMap: size = 3,
- `lastEntry()`                                                                firstEntry: 1 -> ["z", "x", "c"]
    - map의 마지막 요소를 반환
- `pollFirstEntry()`
    - map의 첫번째 요소를 꺼내서 반환
    - Map.Entry<Integer, String[]> pollF1 = classKidsTMap.pollFirstEntry(); // classKidsTMap: size = 2, 
- `pollLastEntry()`                                                            pollF1: 1 -> ["z", "x", "c"]
    - map의 마지막 요소를 꺼내서 반환
