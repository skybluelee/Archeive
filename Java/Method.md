# 메소드
메소드는 다른 언어의 함수와 동일한 개념이나, 자바의 경우 모든 것이 클래스 요소이므로 메소드라고 부른다.

```
public class Ex01 {
    public static void main(String[] args) {
        int int1 = add(2, 3);
        System.out.println(int1);
    }

    static int add (int num1, int num2) {
        return num1 + num2;
    }
}

5
```
메소드의 경우 main 메소드 바깥에 작성하고, 실행문을 메인 메소드 내부에 작성한다.
# 형식
```
static int add (int num1, int num2) {
    return num1 + num2
}
```
- static: 정적 메소드에서 호출하기 위해 사용한다. 해당 값을 사용하지 않으면 메인 메소드에서 사용 불가능하다.
- int: 반환값의 자료형이다. 반환값의 자료형과 일치하지 않을 경우 오류가 발생한다. 반환값이 없을 시 void를 사용한다.
- add: 메소드 이름
# 외부 변수 사용
```
public class Ex01 {
    public static void main(String[] args) {
        int count1 = getCount(); // count1: 1
        int count2 = getCount(); // count2: 2
        int count3 = getCount(); // count3: 3
        int count4 = getCount(); // count4: 4
    }

    static int count = 0;

    static int getCount () {
        System.out.println("카운트 증가");
        return ++count;
    }
}
```
메인 메소드 외부에서 `static`을 사용하여 변수를 생성하는 경우 외부에서도 값을 참조 가능하다.

단, 이러한 방법은 사용하지 않는 것이 좋다.
# 배열 입력과 반환
```
public class Ex01 {
    public static void main(String[] args) {
        int[] numbers = {3, 5, 9, 2, 8, 1, 4};

        int maxOfNumbers = getMaxAndMin(numbers)[0];
        int minOfNumbers = getMaxAndMin(new int[] {3, 5, 9, 2, 8, 1, 4})[1];
    }

    static int[] getMaxAndMin (int[] nums) {
        int max = nums[0];
        int min = nums[0];
        for (int num : nums) {
            max = max > num ? max : num;
            min = min < num ? min : num;
        }
        return new int[] {max, min};
    }
}
```
배열을 입력으로 하는 경우 위와 같이 배열을 생성하고 `int[] number = {}` 생성한 배열을 입력으로 넣거나, 배열 자체를 입력할 수 있다. 두번째 경우 무조건 `new <자료형> [] {}` 형식이어야 한다.

자바에서는 여러 값을 리턴할 수 없으므로, 여러 값을 리턴하는 경우에는 배열이나 객체를 사용한다.
# 입력이 정해지지 않는 경우
```
public class Ex01 {
    public static void main(String[] args) {
        double avg = getAverage(3, 91, 14, 27, 4);
    }

    static double getAverage(int... nums) { // nums: {3, 91, 14, 27, 4}
        double result = 0.0;
        for (int num : nums) {
            result += num;
        }
        return result / nums.length;
    }
}
```
`int...`의 경우 int 자료형의 값의 개수를 알 수 없는 경우 사용한다.

`int[]`와 다르므로 해당 메소드를 사용할 때 입력으로 값을 여러개를 사용한다.

위 경우 `nums`로 3, 91, 14, 27, 4의 값을 입력하였고, 실행하는 메소드에서는 배열로 간주하여 실행한다.

단, `static String descClass (int classNo, String teacher, String... kids)`와 같이 정해진 인자들과 사용시 맨 마지막에 놓아야 한다. 
# 메소드 오버로딩
```
static int add(int a, int b) { return a + b; }
static int add(int a, int b, int c) { return a + b + c; }
static double add(double a, double b) { return a + b; }

static String add(String a, char b) { return a + b; }
static String add(char a, String b) { return a + b; }

static double add(int a, int b) { return (double) (a + b); } // 오류 발생
```
1. 매개변수의 개수가 다르고,
2. 매개변수의 자료형이 다르고,
3. 매개변수의 자료형의 순서가 다른 경우
메소드 이름이 같아도 다른 함수로 인식해서 사용할 수 있는데, 이를 메소드 오버로딩이라 한다.

단 매개변수는 갖지만 반환하는 자료형이 다른 경우는 오버로딩이 불가능하다.
# 원시형과 참조형
```
public class Ex01 {
    public static void main(String[] args) {
        int intNum = 3;        // intNum: 3
        modifyIntArg(intNum);

        int[] intNums = {1, 2, 3};

        //  배열은 참조형이지만 그 안의 값들은 원시형
        modifyIntArg(intNums[0]);

        //  참조형인 배열 자체를 인자로 사용
        modifyAryElem(intNums); // intNums: {1, 3, 3}
    }

    static void modifyIntArg (int num) {
        System.out.printf("수정 전: %d%n", num++);
        System.out.printf("수정 후: %d%n", num);
    }
    static  void modifyAryElem (int[] ary) {
        System.out.printf("수정 전: %d%n", ary[1]++);
        System.out.printf("수정 후: %d%n", ary[1]);
    }
}
```
원시형의 경우 값을 복사하여 사용하므로 메소드 내에서 값을 수정하더라도 원본 값은 변하지 않는다.

참조형의 경우 값 자체를 사용하므로 메소드 내에서 값을 수정하면 해당 값도 변한다.
