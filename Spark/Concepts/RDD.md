해당 문서는 [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)를 바탕으로 작성하였다.
# RDD
Spark는 RDD(Resilient Distributed Dataset)라는 개념을 중심으로 동작한다. 
RDD는 Spark에서 데이터를 나타내는 기본 추상화 방식으로, 병렬로 작동할 수 있는 요소들의 장애 허용(fault-tolerant) 컬렉션이다. 
RDD를 생성하는 방법으로는
기존의 컬렉션을 드라이버 프로그램에서 병렬화하는 방법 또는 공유 파일 시스템, HDFS, HBase 또는 Hadoop InputFormat을 제공하는 기타 데이터 소스와 같은 외부 저장 시스템에서 데이터셋을 참조하는 방법 2가지가 존재한다.

## 병렬 컬렉션(Parallelized Collections)
병렬 컬렉션은 드라이버 프로그램 내의 기존 반복 가능한(iterable) 객체나 컬렉션에 SparkContext의 `parallelize`  메서드를 호출하여 생성된다.
컬렉션의 요소들은 병렬로 작동할 수 있는 분산 데이터셋을 형성하기 위해 복사된다.
예를 들어, 숫자 1부터 5까지를 포함하는 병렬 컬렉션을 생성하는 방법은 다음과 같다.
```
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
```
생성된 분산 데이터셋(distData)은 병렬로 작동할 수 있다.
예를 들어, `distData.reduce(lambda a, b: a + b)`를 호출하여 리스트의 요소들을 합할 수 있다.
분산 데이터셋에 대한 연산에 대해서는 이후에 설명한다.

병렬 컬렉션에 대한 중요한 매개변수 중 하나는 데이터셋을 나눌 파티션의 개수이다.
Spark는 클러스터의 각 파티션에 대해 하나의 task를 실행한다.
일반적으로 클러스터의 각 CPU당 2-4개의 파티션을 사용한다.
보통, Spark는 클러스터에 기반하여 자동으로 파티션의 수를 설정하려고 시도한다.
그러나, `parallelize`의 두 번째 파라미터로 전달하여 수동으로 설정할 수 있다 (예: `sc.parallelize(data, 10)`). 
참고: 코드의 일부 위치에서는 역호환성을 유지하기 위해 파티션의 동의어인 slices라는 용어를 사용함.

## 외부 데이터셋
PySpark는 Hadoop에서 지원하는 모든 저장소 소스(로컬 파일 시스템, HDFS, Cassandra, HBase, Amazon S3)에서 분산 데이터셋을 생성할 수 있다.
Spark는 텍스트 파일, SequenceFiles 및 Hadoop InputFormat의 다른 파일 형식을 지원한다.

SparkContext의 `textFile` 메서드를 사용하여 텍스트 파일 RDD를 생성할 수 있다.
이 메서드는 파일에 대한 URI(머신 내의 로컬 경로 또는 hdfs://, s3a:// 등의 URI)를 가져와 그것을 라인의 컬렉션으로 읽는다. 아래는 해당 예시이다.

```
>>> distFile = sc.textFile("data.txt")
```
생성된 후에 distFile은 데이터셋 연산으로 처리할 수 있다. 
예를 들어, `distFile.map(lambda s: len(s)).reduce(lambda a, b: a + b)`를 사용하여 `map`과 `reduce`를 사용하는 모든 라인의 크기를 사용하여 합할 수 있다.

Spark에서 파일을 읽는 데 대한 몇 가지 주의점.
- 로컬 파일 시스템의 경로를 사용하는 경우, 해당 파일은 워커 노드의 동일한 경로에서도 접근 가능해야 한다. 그렇지 않으면 모든 워커에 파일을 복사하거나 네트워크로 마운트된 공유 파일 시스템을 사용해야 한다.
- textFile을 포함한 Spark의 모든 파일 기반 입력 메서드는 디렉터리, 압축된 파일, 와일드카드도 지원한다. 예를 들면, `textFile("/my/directory")`, `textFile("/my/directory/*.txt")`, `textFile("/my/directory/*.gz")` 등을 사용할 수 있다.
- textFile 메서드는 파일의 파티션 수를 제어하기 위한 선택적(optional) 두 번째 인자를 사용합니다. 기본적으로 Spark는 파일의 각 블록(기본적으로 HDFS에서는 128MB)에 대해 하나의 파티션을 생성합니다. 그러나 더 큰 값으로 전달하여 더 많은 파티션을 요청할 수도 있다. 블록보다 적은 파티션을 가질 수는 없다.

텍스트 파일 외에도 Spark의 Python API는 여러 다른 데이터 형식을 지원한다.
- `SparkContext.wholeTextFiles`는 여러 작은 텍스트 파일을 포함하는 디렉터리를 읽고, 각각을 (파일 이름, 내용) 쌍으로 반환한다. 이것은 각 파일의 1줄당 1개의 레코드를 반환하는 `textFile`과 대조적이다.
- `RDD.saveAsPickleFile` 및 `SparkContext.pickleFile`은 pickle Python 객체로 구성된 간단한 형식으로 RDD를 저장하는 것을 지원한다. pickle 직렬화에서는 배치(batching)가 사용되고, 기본 배치 크기는 10이다.
- SequenceFile 및 Hadoop Input/Output Formats

주의 - 이 기능은 현재 실험적으로 표시되어 있으며, 고급 사용자를 위해 설계되었다. 해당 기능은 Spark SQL이 선호되는 접근 방식인 Spark SQL을 기반으로 한 읽기/쓰기 지원으로 대체될 수 있다.

### Writable Support
PySpark의 SequenceFile 지원은 Java 내에서 키-값 쌍의 RDD를 로드하고, Writables를 기본 Java 타입으로 변환하며, 그 결과로 나온 Java 객체들을 pickle을 사용하여 pickle한다.
키-값 쌍의 RDD를 SequenceFile에 저장할 때, PySpark는 반대로 동작합니다. 
Python 객체를 Java 객체로 unpickle하고, 그 다음에 이를 Writables로 변환한다.
다음과 같은 Writables는 자동으로 변환된다.

|Writable Type|Python Type|
|-------------|-----------|
|Text|str|
|IntWritable|int|
|FloatWritable|float|
|DoubleWritable|float|
|BooleanWritable|bool|
|BytesWritable|bytearray|
|NullWritable|None|
|MapWritable|dict|

> pickle: Python에서 제공하는 직렬화 프로토콜이다. 직렬화(serialization)는 객체의 상태나 데이터를 저장하거나 전송 가능한 형식으로 변환하는 프로세스를 의미하며, pickle은 Python 객체를 바이트 스트림으로 변환하는 데 사용되고, 이 바이트 스트림은 나중에 원래의 객체로 복원될 수 있다.

배열은 기본적으로 처리되지 않는다.
사용자들은 읽기 또는 쓰기 시 사용자 정의 `ArrayWritable` 하위 타입을 명시적으로 지정해야 한다.
쓰기 시에는 배열을 사용자 정의 `ArrayWritable` 하위 타입으로 변환하는 사용자 정의 변환기(converter)도 명시해야 한다.
읽기 시에는 기본 변환기가 사용자 정의 `ArrayWritable` 하위 타입을 `Java Object[]`로 변환하며, 이 후에 Python 튜플로 pickle된다.
원시 타입의 배열에 대한 Python `array.array`를 얻으려면 사용자들은 사용자 정의 변환기를 명시적으로 지정해야 한다.

### Saving and Loading SequenceFiles
```
>>> rdd = sc.parallelize(range(1, 4)).map(lambda x: (x, "a" * x))
>>> rdd.saveAsSequenceFile("path/to/file")
>>> sorted(sc.sequenceFile("path/to/file").collect())
[(1, u'a'), (2, u'aa'), (3, u'aaa')]
```
텍스트 파일과 마찬가지로, SequenceFiles는 경로를 지정하여 저장하고 로드할 수 있다. 
키와 값 클래스는 지정할 수 있지만, 표준 Writables의 경우 이는 필수가 아니다.

### Saving and Loading Other Hadoop Input/Output Formats
PySpark는 'new' 그리고 'old' Hadoop MapReduce API 모두에 대해 어떤 Hadoop InputFormat을 읽거나 어떤 Hadoop OutputFormat을 작성할 수 있다.
필요한 경우, Hadoop 구성을 Python 딕셔너리로 전달할 수 있다.
Elasticsearch ESInputFormat을 사용한 예시는 다음과 같다.
```
$ ./bin/pyspark --jars /path/to/elasticsearch-hadoop.jar
>>> conf = {"es.resource" : "index/type"}  # assume Elasticsearch is running on localhost defaults
>>> rdd = sc.newAPIHadoopRDD("org.elasticsearch.hadoop.mr.EsInputFormat",
                             "org.apache.hadoop.io.NullWritable",
                             "org.elasticsearch.hadoop.mr.LinkedMapWritable",
                             conf=conf)
>>> rdd.first()  # the result is a MapWritable that is converted to a Python dict
(u'Elasticsearch ID',
 {u'field1': True,
  u'field2': u'Some Text',
  u'field3': 12345})
```
InputFormat이 Hadoop 구성과/또는 입력 경로에만 의존하고 키와 값 클래스가 위의 표에 따라 쉽게 변환될 수 있다면, 위의 접근 방식은 해당 경우에 잘 작동할 것이다.

Cassandra나 HBase에서 데이터를 로드하는 경우와 같이 사용자 정의 직렬화된 2진 데이터를 가지고 있다면, 먼저 Scala/Java 쪽에서 pickle의 pickler가 처리할 수 있는 형식으로 해당 데이터를 변환해야 한다.
이를 위해 [Converter](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/api/python/Converter.html) 특성이 제공된다.
이 특성을 확장하고 변환 메서드에서 변환 코드를 구현하면 된다.
`InputFormat`에 접근하는데 필요한 종속성을 갖고 있는 해당 클래스는 Spark job jar에 패키지로 포함되고, PySpark 클래스 경로에 포함되어야 한다.

Cassandra / HBase `InputFormat` 및 `OutputFormat`을 사용하는 사용자 정의 변환기와 관련한 예제를 보려면 [Python 예제](https://github.com/apache/spark/tree/master/examples/src/main/python)와 [Converter 예제](https://github.com/apache/spark/tree/master/examples/src/main/scala/org/apache/spark/examples/pythonconverters)를 참조하라.

## RDD 연산
RDDs는 2가지 종류의 연산을 지원한다 - transformation 연산은 기존의 데이터셋에서 새로운 데이터셋을 생성하는 연산이며, action 연산은 데이터셋에 대한 계산을 실행한 후 드라이버 프로그램에 값을 반환한다.
예를 들면, `map`은 각 데이터셋 요소를 함수를 통해 전달하고 결과를 나타내는 새로운 RDD를 반환하는 transformation 연산이다.
반면에, `reduce`는 RDD의 모든 요소를 특정 함수를 사용하여 집계하고 최종 결과를 드라이버 프로그램에 반환하는 action 연산이다(물론 분산 데이터셋을 반환하는 parallel `reduceByKey`도 있다).

Spark의 모든 transformation 연산은 lazy하다. 
이는 transformation 연산이 즉시 결과를 계산하지 않는다는 것을 의미한다.
대신, 기본 데이터셋에 적용된 변환을 기억만 한다.
action 연산에서 결과를 드라이버 프로그램에 반환해야 할 때만 transformation 연산이 계산된다.
이 설계 방식은 Spark가 더 효율적으로 실행되도록 만든다.
예를 들어, `map`을 통해 생성된 데이터셋이 `reduce`에서 사용될 것임을 알고, 매핑된 큰 데이터셋이 아닌 `reduce`의 결과만을 드라이버에 반환할 수 있다.

기본적으로 각 transform된 RDD는 action을 실행할 때마다 다시 계산될 수 있다. 
그러나 persist(또는 cache) 메서드를 사용하여 RDD를 메모리에 유지할 수도 있으며, 이 경우 Spark는 다음 번에 쿼리할 때 빠른 액세스를 위해 클러스터의 요소를 유지한다. 
RDD를 디스크에 지속적으로 저장하거나 여러 노드에 복제하는 기능도 지원된다.

### 기초
```
lines = sc.textFile("data.txt")
lineLengths = lines.map(lambda s: len(s))
totalLength = lineLengths.reduce(lambda a, b: a + b)
```
첫 번째 줄은 외부 파일에서 기본 RDD를 정의한다.
이 데이터셋은 메모리에 로드되거나 다른 방식으로 처리되지 않는다: lines는 단순히 파일을 가리키는 포인터일 뿐이다.
두 번째 줄에서는 map 변환의 결과로 `lineLengths`를 정의한다.
여기서도 laziness 때문에 `lineLengths`는 즉시 계산되지 않는다.
마지막으로 우리는 action인 reduce를 실행한다.
이 시점에서 Spark는 계산을 별도의 머신에서 실행할 작업으로 분할하고, 각 머신은 map과 reduce를 모두 실행하여, 답변만을 드라이버 프로그램에 반환한다.
```
lineLengths.persist()
```
`lineLengths`를 나중에 다시 사용하길 원한다면 위 코드를 reduce 이전에 추가하면 된다.
그렇게 하면 `lineLengths`는 처음 계산된 이후 메모리에 저장된다.

### Passing Functions to Spark
Spark의 API는 클러스터에서 실행되기 위해 드라이버 프로그램에서 함수를 전달하는 것을 매우 의존한다.
이를 수행하는 세 가지 권장 방법이 있다.
1. 간단한 함수로서 식으로 작성할 수 있는 경우에는 람다 표현식을 사용한다. (람다는 여러 문장 또는 값을 반환하지 않는 문장을 지원하지 않는다.)
2. 더 긴 코드의 경우, Spark에 호출되는 함수 내부에 local로 정의한다.
3. 모듈 내의 최상위 함수(top-level functions)를 사용한다.

```
"""MyScript.py"""
if __name__ == "__main__":
    def myFunc(s):
        words = s.split(" ")
        return len(words)

    sc = SparkContext(...)
    sc.textFile("file.txt").map(myFunc)
```
예를 들어, 람다를 사용하기에 긴 코드는 위와 같이 사용한다.
***
```
class MyClass(object):
    def func(self, s):
        return s
    def doStuff(self, rdd):
        return rdd.map(self.func)
```
참고로 클래스 인스턴스의 메서드 참조를 전달하는 것도 가능하다(싱글턴 객체와는 반대로). 
그러나 이는 해당 클래스를 포함하는 객체를 메서드와 함께 전송해야 하는 것을 의미한다.

> 싱글턴 객체: 싱글턴 객체(Singleton object)는 오직 하나의 인스턴스만을 가지는 객체를 의미한다. 즉, 클래스로부터 생성된 객체 중에서 오직 한 번만 생성되어 프로그램 전체에서 공유되는 객체를 말한다.

***
```
class MyClass(object):
    def __init__(self):
        self.field = "Hello"
    def doStuff(self, rdd):
        return rdd.map(lambda s: self.field + s)
```
새로운 `MyClass`를 생성하고 그 위에 `doStuff`를 호출하면, 그 내부의 map은 그 MyClass 인스턴스의 func 메서드를 참조하므로 전체 객체가 클러스터로 전송되어야 한다.

비슷한 방식으로, 외부 객체의 필드에 접근하면 전체 객체가 참조된다.
***
```
def doStuff(self, rdd):
    field = self.field
    return rdd.map(lambda s: field + s)
```
이 문제를 피하기 위한 가장 간단한 방법은 외부적으로 접근하는 대신 필드를 로컬 변수로 복사하는 것이다.

### Understanding closures
Spark에서 어려운 부분 중 하나는 클러스터 전체에서 코드를 실행할 때 변수와 메서드의 범위와 생명 주기를 이해하는 것이다.
범위 밖의 변수를 수정하는 RDD 작업은 종종 혼란의 원인이 될 수 있다. 
아래 예제에서는 `foreach()`를 사용하여 카운터를 증가시키는 코드로, 위에서 언급한 문제가 발생할 수 있다.

#### Example
```
counter = 0
rdd = sc.parallelize(data)

# Wrong: Don't do this!!
def increment_counter(x):
    global counter
    counter += x
rdd.foreach(increment_counter)

print("Counter value: ", counter)
```
단순한 RDD 요소의 합을 구하는 것을 생각해보라. 이는 실행이 동일한 JVM 내에서 이루어지는지 여부에 따라 다르게 작동할 수 있다. 
이러한 일반적인 예는 Spark를 `local mode (--master = local[n])`에서 실행할 때와 Spark 애플리케이션을 클러스터에 배포할 때 (예: spark-submit을 통해 YARN으로 배포)의 경우이다.

#### Local vs. cluster modes
위의 코드의 동작은 정의되어 있지 않으며, 의도한 대로 작동하지 않을 수 있다.
job을 실행하기 위해, Spark는 RDD 작업의 처리를 task로 분할하여 실행하는데, 각 task는 executor에 의해 실행된다.
실행 전에 Spark는 task의 closure를 계산한다.
closure는 executor가 RDD에서 (이 경우 `foreach()`에서) 계산을 수행하기 위해 볼 수 있어야 하는 변수와 메서드이다.
이 클로저는 직렬화되어 각 executor에게 전송된다.

각 executor에 전송된 closure 내의 변수는 이제 복사본이므로, `foreach` 함수 내에서 counter가 참조될 때 드라이버 노드의 counter가 아니다.
드라이버 노드의 메모리에는 여전히 counter가 있지만, 이것은 더 이상 executor에게 보이지 않는다!
익스큐터는 직렬화된 closure에서의 복사본만 볼 수 있다. 
따라서 counter의 최종 값은 counter에 대한 모든 작업은 직렬화된 closure 내의 값에 대한 참조를 했기 때문에 여전히 0이 된다.

로컬 모드에서는 일부 상황에서 `foreach` 함수가 실제로 드라이버와 동일한 JVM 내에서 실행되어 원래의 counter를 참조하고 실제로 업데이트할 수 있다.

이러한 시나리오에서 명확하게 정의된 동작을 보장하기 위해 Accumulator를 사용해야 한다.
Spark의 Accumulator는 클러스터의 워커 노드 간에 실행이 분할될 때 변수를 안전하게 업데이트하는 메커니즘을 제공하기 위해 특별히 사용된다.
이 가이드의 Accumulators 섹션에서 이에 대해 더 자세히 다룬다.

일반적으로 클로저 - 루프나 로컬로 정의된 메서드와 같은 consturct(생성자)는 전역 상태를 변경하는 데 사용되어서는 안 된다.
Spark는 closures 외부에서 참조된 객체의 변이 동작을 정의하거나 보장하지 않는다.
이렇게 하는 코드는 로컬 모드에서 작동할 수 있지만, 그것은 우연에 불과하며, 이러한 코드는 분산 모드에서 예상대로 동작하지 않을 것이다.
전역 집계가 필요한 경우 Accumulator를 사용하라.

#### Printing elements of an RDD
또 다른 흔한 사용법은 `rdd.foreach(println)` 또는 `rdd.map(println)`을 사용하여 RDD의 요소를 출력하는 것이다.
단일 머신에서는 이를 통해 예상된 출력이 생성되며 RDD의 모든 요소가 출력된다.
그러나 클러스터 모드에서는 executor에 의해 호출되는 stdout 출력이 이제 드라이버가 아닌 executor의 stdout에 작성되므로, 드라이버의 stdout에는 이러한 출력이 표시되지 않는다!
드라이버에서 모든 요소를 출력하려면 RDD를 먼저 드라이버 노드로 가져오기 위해 collect() 메서드를 사용해야 한다.
따라서 다음과 같이 작성할 수 있다: `rdd.collect().foreach(println)`.
그러나 `collect()`는 RDD 전체를 단일 머신으로 가져오기 때문에 드라이버의 메모리가 부족할 수 있다. 
RDD의 몇몇 요소만 출력해야 하는 경우 take()를 사용하는 것이 더 안전한 접근 방식입니다: `rdd.take(100).foreach(println)`.

### Working with Key-Value Pairs
대부분의 Spark 작업은 어떤 유형의 객체를 포함하는 RDD에서 작동하지만, 특정 특별한 작업은 키-값 쌍의 RDD에서만 사용할 수 있다. 
가장 일반적인 것은 키를 기준으로 요소를 그룹화하거나 집계하는 것과 같은 분산 "셔플" 작업이다.

Python에서는 이러한 작업이 (1, 2)와 같은 내장 Python 튜플을 포함하는 RDD에서 작동한다.
간단히 이러한 튜플을 생성한 후 원하는 작업을 호출하면 된다.

```
lines = sc.textFile("data.txt")
pairs = lines.map(lambda s: (s, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)
```
예를 들어, 위 코드는 키-값 쌍에서 `reduceByKey` 작업을 사용하여 파일의 각 텍스트 라인이 발생하는 빈도를 카운트한다.

우리는 또한 `counts.sortByKey()`와 같이 키를 기준으로 쌍을 알파벳순으로 정렬하고, 마지막으로 `counts.collect()`를 사용하여 그들을 객체의 목록으로 드라이버 프로그램으로 다시 가져올 수 있다.

### Transformations
다음 표는 Spark에서 지원하는 일반적인 transformation 연산 몇 가지를 나열한다. 자세한 내용은 RDD API 문서 ([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/rdd/RDD.html), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/api/java/JavaRDD.html), [Python](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html#pyspark.RDD), [R](https://spark.apache.org/docs/latest/api/R/reference/index.html))와 페어 RDD 함수 문서 ([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/rdd/PairRDDFunctions.html), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/api/java/JavaPairRDD.html))를 참조하라.

|Transformation|Meaning|
|------------|-----------|
|map(_func_)|소스의 각 요소를 함수 func를 통과시켜 생성한 새로운 분산 데이터셋을 반환한다.|
|filter(_func_)|원본 데이터셋에서 func 함수가 true를 반환하는 요소들만 선택하여 생성한 새로운 데이터셋을 반환한다.|
|flatMap(_func_)|map과 유사하지만 각 입력 항목은 0개 또는 그 이상의 출력 항목으로 매핑될 수 있다 (따라서 func는 단일 항목 대신에 Seq(시퀀스)를 반환해야 한다).|
|mapPartitions(_func_)|map과 유사하지만, 각 파티션(블록)에 독립적으로 실행된다. 따라서 func는  Iterator<T> => Iterator<U> 유형이어야 한다.|
|mapPartitionsWithIndex(_func_)|mapPartitions와 유사하지만, 파티션의 인덱스 정보도 제공된다. func는 T 타입의 RDD를 실행할 때 (Int, Iterator<T>) => Iterator<U> 유형이어야 한다.|
|sample(_withReplacement, fraction, seed_)|주어진 난수 생성기의 시드를 사용하여 데이터의 일정한 비율만큼 복원 또는 비복원(with replacement, w/o replacement) 방식으로 샘플링한다.|
|union(_otherDataset_)|원본 데이터셋과 인자의 요소들의 합집합을 포함하는 새로운 데이터셋을 반환한다.|
|intersection(_otherDataset_)|원본 데이터셋과 인자의 요소들의 교집합을 포함하는 새로운 RDD를 반환한다.|
|distinct([_numPartitions_]))|원본 데이터셋의 중복되지 않는 요소만 포함하는 새로운 데이터셋을 반환한다.|
|groupByKey([_numPartitions_])|데이터셋이 (K, V) 쌍으로 구성된 경우, (K, Iterable<V>) 쌍의 데이터셋을 반환한다.<br><br>참고: 키별로 집계(합계 또는 평균을 구하는 경우)를 수행하기 위해 그룹화하려는 경우, `reduceByKey` 또는 `aggregateByKey`를 사용하면 훨씬 더 나은 성능을 얻을 수 있다.<br><br>참고: 출력의 병렬성 수준은 기본적으로 부모 RDD의 파티션 수에 따라 결정된다. 사용자는 다른 작업(task) 수를 설정하기 위해 선택적으로 `numPartitions` 인자를 전달할 수 있다.|
|reduceByKey(_func_, [_numPartitions_])|데이터셋이 (K, V) 쌍으로 구성된 경우, 주어진 reduce 함수 func를 사용하여 각 키의 값이 집계된 (K, V) 쌍의 데이터셋을 반환한다. 이 reduce 함수 func는 (V,V) => V 타입이어야 합니다. `groupByKey`와 마찬가지로, reduce 작업의 수는 선택적인 두 번째 인자를 통해 구성할 수 있다.|
|aggregateByKey(zeroValue)(_seqOp_, _combOp_, [_numPartitions_])|데이터셋이 (K, V) 쌍으로 구성된 경우, 주어진 combine 함수와 중립적인 "zero" 값 사용하여 각 키의 값이 집계된 (K, U) 쌍의 데이터셋을 반환한다. 입력 값 타입과 다른 집계 값 타입을 허용하면서 불필요한 할당을 피한다. `groupByKey`와 마찬가지로, reduce 작업의 수는 선택적인 두 번째 인자를 통해 구성할 수 있다.|
|sortByKey([_ascending_], [_numPartitions_])|데이터셋이 (K, V) 쌍으로 구성되며 K가 Ordered를 구현한 경우, boolean 타입의 ascending 인자에 지정된 대로 키를 오름차순 또는 내림차순으로 정렬된 (K, V) 쌍의 데이터셋을 반환한다.|
|join(otherDataset, [_numPartitions_])|(K, V)와 (K, W) 타입의 데이터셋을 대상으로 호출되면, 각 키에 대한 모든 요소의 쌍을 포함하는 (K, (V, W)) 쌍의 데이터셋을 반환한다. Outer 조인은 leftOuterJoin, rightOuterJoin, fullOuterJoin을 통해 사용할 수 있다.|
|cogroup(_otherDataset_, [_numPartitions_])|(K, V)와 (K, W) 타입의 데이터셋을 대상으로 호출되면, (K, (Iterable<V>, Iterable<W>)) 튜플의 데이터셋을 반환한다. 이 연산은 `groupWith`라고도 한다.|
|cartesian(_otherDataset_)|T와 U 타입의 데이터셋을 대상으로 호출되면, (T, U) 쌍의 데이터셋을 반환한다(모든 요소의 쌍).|
|pipe(command, [_envVars_])|RDD의 각 파티션을 쉘 명령어, 예를 들면 Perl 또는 bash 스크립트로 전달한다. RDD 요소들은 프로세스의 stdin으로 작성되며, 프로세스의 stdout으로 출력된 줄들은 문자열의 RDD로 반환된다.|
|coalesce(_numPartitions_)|RDD의 파티션 수를 numPartitions으로 줄인다. 큰 데이터셋을 필터링한 후에 작업을 더 효율적으로 실행하는 데 유용하다.|
|repartition(_numPartitions_)|RDD의 데이터를 무작위로 다시 배열하여 더 많거나 더 적은 파티션을 생성하고, 그들 사이에서 균형을 맞춘다. 이는 항상 모든 데이터를 네트워크를 통해 재배열한다.|
|repartitionAndSortWithinPartitions(_partitioner_)|주어진 파티셔너에 따라 RDD를 다시 파티셔닝하고, 각 결과 파티션 내에서 레코드를 키별로 정렬한다. 이는 각 파티션 내에서 repartition을 호출한 후에 정렬하는 것보다 효율적인데, 왜냐하면 이 방식은 정렬 작업을 셔플 기계(machinery)로 넣을 수 있기 때문이다.|

### Actions
다음 표는 Spark에서 지원하는 일반적인 action 연산 목록을 나열하고 있다. 자세한 내용은 RDD API 문서([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/rdd/RDD.html), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/api/java/JavaRDD.html), [Python](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html#pyspark.RDD), [R](https://spark.apache.org/docs/latest/api/R/reference/index.html)) 및 pair RDD 함수 문서([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/rdd/PairRDDFunctions.html), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/api/java/JavaPairRDD.html))를 참조하라.

|Action|Meaning|
|------------|-----------|
|reduce(_func_)|두 개의 인자를 받아 하나의 결과를 반환하는 함수 func를 사용하여 데이터셋의 요소를 집계한다. 함수는 병렬로 올바르게 계산될 수 있도록 교환 법칙과 결합 법칙을 가져야 한다.|
|collect()|드라이버 프로그램에서 데이터셋의 모든 요소를 배열로 반환한다. 이는 일반적으로 데이터의 충분히 작은 하위 집합을 반환하는 필터 또는 다른 연산 후에 유용하다.|
|count()|데이터셋의 요소 수를 반환한다.|
|first()|데이터셋의 첫 번째 요소를 반환한다 (`take(1)`과 유사).|
|take(_n_)|데이터셋의 처음 n개의 요소를 배열로 반환한다.|
|takeSample(_withReplacement_, _num_, [_seed_])|데이터셋의 num 요소를 랜덤 샘플로 반환한다. 복원 유무와 선택적으로 난수 생성기 시드를 지정할 수 있다.|
|takeOrdered(_n_, [_ordering_])|첫 번째 n개의 RDD 요소를 자연 순서나 사용자 지정 비교자를 사용하여 반환한다.|
|saveAsTextFile(_path_)|데이터셋의 요소를 지정된 디렉토리(HDFS나 Hadoop 지원 파일 시스템)에 텍스트 파일(또는 여러 텍스트 파일)로 저장한다. Spark는 `toString` 메서드를 호출하여 각 요소를 파일의 텍스트 줄로 변환한다.|
|saveAsSequenceFile(_path_)(Java and Scala)|데이터셋의 요소를 지정된 경로의 로컬 파일 시스템, HDFS 또는 기타 Hadoop 지원 파일 시스템에 Hadoop SequenceFile 형식으로 저장한다. 이 기능은 Hadoop의 Writable 인터페이스를 구현한 키-값 쌍의 RDD에 사용할 수 있다. Scala에서는 Writable로 암시적으로 변환 가능한 타입에 대해서도 사용할 수 있다 (Spark는 Int, Double, String 등의 기본 타입에 대한 변환을 포함하고 있다).|
|saveAsObjectFile(_path_)(Java and Scala)|데이터셋의 요소를 Java 직렬화를 사용하여 간단한 형식으로 저장한다. 이후에는 `SparkContext.objectFile()`을 사용하여 로드할 수 있다.|
|countByKey()|(K, V) 타입의 RDD에만 사용 가능하며, 각 키의 수를 반환하는 (K, Int) 쌍의 해시맵을 반환한다.|
|foreach(_func_)|데이터셋의 각 요소에 함수 func를 실행한다. 이는 일반적으로 [Accumulator](https://spark.apache.org/docs/latest/rdd-programming-guide.html#accumulators)를 업데이트하거나 외부 저장 시스템과 상호 작용하는 등의 부수 효과를 위해 수행된다.<br><br>참고: `foreach()` 외부에서 Accumulators 외의 변수를 수정하는 것은 정의되지 않은 동작을 초래할 수 있다. 자세한 내용은 [Understanding closures](https://spark.apache.org/docs/latest/rdd-programming-guide.html#understanding-closures-a-nameclosureslinka)를 참조하라.|

Spark RDD API는 일부 액션의 비동기 버전도 제공한다. 예를 들면, `foreach`의 비동기 버전인 `foreachAsync`가 있다. `foreachAsync`는 액션의 완료를 기다리는 대신 즉시 호출자에게 `FutureAction`을 반환합니다. 
이를 사용하여 액션의 비동기 실행을 관리하거나 대기할 수 있다.

### Shuffle operations
Spark에서 특정 연산은 셔플(shuffle)이라는 이벤트를 발생시킨다.
셔플은 데이터를 재분배하여 다른 파티션으로 그룹화하는 Spark의 메커니즘이다.
이는 일반적으로 데이터를 executor와 머신 간에 복사하는 것을 포함하여 복잡하고 비용이 많이 드는 작업이다.

#### Background
셔플 동안 어떤 일이 발생하는지 이해하기 위해, `reduceByKey` 연산의 예를 살펴볼 수 있다.
`reduceByKey` 연산은 하나의 키에 대한 모든 값을 튜플로 결합되는 새로운 RDD를 생성한다 - 키와 해당 키에 연결된 모든 값을 사용하여 실행되는 reduce 함수의 결과이다.
문제는 하나의 키에 대한 모든 값이 동일한 파티션에, 심지어 같은 머신에 있지 않을수도 있으나 결과를 계산하기 위해 값들은 동일한 위치에 있어야 한다는 점이다.

Spark에서는 일반적으로 데이터가 특정 연산에 필요한 위치에 위치에 존재하도록 파티션 간에 분산되어 있지 않는다. 
계산 중에 단일 작업은 단일 파티션에서 작동합니다. 따라서 `reduceByKey` reduce 작업을 실행하기 위해 모든 데이터를 조직화하려면 Spark는 all-to-all 연산을 수행해야 한다. 
Spark는 모든 키에 대한 모든 값들을 찾기 위해 모든 파티션에서 읽어야 하며, 그런 다음 각 키에 대한 최종 결과를 계산하기 위해 파티션 간의 값들을 모으는 작업을 수행해야 한다 - 이것이 셔플이라고 한다.

새로 셔플된 데이터의 각 파티션에 있는 요소 집합은 결정론적(과정은 알 수도, 설정할 수도 없음)이며, 파티션 자체의 순서도 결정론적이다. 
그러나 이러한 요소들의 순서는 그렇지 않다. 
셔플 후 예측 가능한 순서의 데이터를 원하는 경우 아래 방법을 사용하라.

- 각 파티션을 정렬하기 위해 `mapPartitions`를 사용.
- 동시에 다시 파티셔닝(repartitioning)하면서 파티션을 효율적으로 정렬하기 위해 `repartitionAndSortWithinPartitions`를 사용.
- 전역적으로 정렬된 RDD를 만들기 위해 `sortBy`를 사용.

셔플을 유발할 수 있는 연산에는 [`repartition`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#RepartitionLink) 및 [`coalesce`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#RepartitionLink)와 같은 **repartition** 연산, [`groupByKey`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#GroupByLink) 및 [`reduceByKey`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#ReduceByLink)와 같은 **ByKey** 연산(카운팅은 제외), [`cogroup`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#CogroupLink) 및 [`join`](https://spark.apache.org/docs/latest/rdd-programming-guide.html#JoinLink)과 같은 **join** 연산이 포함된다.

#### Performance Impact
셔플은 디스크 I/O, 데이터 직렬화, 네트워크 I/O를 포함하기 때문에 비용이 많이 드는 작업이다.
셔플을 위해 Spark는 데이터를 조직하기 위한 map 작업 세트와 데이터를 집계하기 위한 reduce 작업 세트를 생성한다. 
이 용어는 MapReduce에서 비롯되었으며 Spark의 map과 reduce 연산과 직접적으로 관련되어 있지는 않다.

내부적으로, 개별 map 작업에서의 결과는 메모리에 보관되며 더 이상 저장할 수 없을 때까지 유지된다. 그런 다음, 이러한 결과는 대상 파티션을 기준으로 정렬되어 단일 파일로 쓰여진다. reduce 측에서 작업은 관련된 정렬된 블록을 읽는다.

특정 셔플 작업은 레코드를 조직하기 위해 레코드 전송 전/후에 메모리 내 데이터 구조를 사용하므로 큰 양의 힙 메모리를 소비할 수 있다. 
구체적으로, `reduceByKey` 및 `aggregateByKey`는 map 측에서 이러한 구조를 생성하며, ByKey 작업은 reduce 측에서 이를 생성한다. 
데이터가 메모리에 맞지 않으면 Spark는 이러한 테이블을 디스크에 스피릴링(spilling)하여 디스크 I/O의 추가 오버헤드와 증가된 가비지 컬렉션 비용을 발생시킨다.

> 스피릴링(spilling)은 메모리 내의 데이터나 작업 결과가 메모리에 모두 저장될 수 없을 때, 초과된 데이터를 임시로 디스크에 저장하는 프로세스를 의미한다. Spark와 같은 분산 컴퓨팅 프레임워크에서는 메모리 제한이나 대규모 데이터 처리 작업 때문에 이러한 스피릴링 메커니즘을 사용하여 성능을 유지하고 데이터 손실 없이 처리할 수 있게 한다. 스피릴링은 일반적으로 비용이 더 많이 들기 때문에, 가능하면 메모리에 데이터를 보관하는 것이 더 효율적이지만, 제한된 메모리 용량 내에서는 스피릴링이 필요할 수 있다.

셔플은 또한 디스크에 많은 수의 중간 파일을 생성한다.
Spark 1.3부터는 이러한 파일들은 해당 RDD가 더 이상 사용되지 않고 가비지 컬렉트(garbage collected)될 때까지 보존된다. 이는 라인지(lineage)가 다시 계산될 경우 셔플 파일을 다시 생성할 필요가 없도록 하기 위해 수행된다. 
가비지 컬렉션은 애플리케이션이 이러한 RDD에 대한 참조를 유지하거나 GC가 빈번하게 발생하지 않는 경우 장기간 이후에 발생할 수 있다. 
이는 장기 실행되는 Spark 작업이 많은 양의 디스크 공간을 사용할 수 있음을 의미한다. 임시 저장 디렉토리는 Spark 컨텍스트를 구성할 때 `spark.local.dir` 구성 매개변수로 지정된다.

셔플 동작은 다양한 구성 매개변수를 조정하여 조정할 수 있다. [Spark Configuration Guide](https://spark.apache.org/docs/latest/configuration.html) 내의 'Shuffle Behavior' 섹션을 참조하라.

## RDD Persistence
Spark에서 가장 중요한 기능 중 하나는 연산 간에 메모리에 데이터셋을 지속적으로 저장(또는 캐싱)하는 것이다.
RDD를 지속적으로 저장하면 각 노드는 해당 RDD의 파티션을 메모리에 저장하고 그 데이터셋(또는 그것을 기반으로 한 데이터셋)의 다른 작업에서 재사용한다. 
이 방식을 사용하여 미래의 작업이 훨씬 빠르게(주로 10배 이상) 실행될 수 있다. 캐싱은 반복 알고리즘과 빠른 대화형 사용을 위한 핵심 도구이다.

RDD를 지속적으로 저장하려면 해당 RDD에 대해 `persist()` 또는 `cache()` 메서드를 사용하면 된다.
첫 번째로 action에서 계산될 때 해당 RDD는 노드의 메모리에 보관된다. 
Spark의 캐시는 고장 허용성(fault-tolerant)을 갖추고 있어, RDD의 어떤 파티션이 손실되더라도 원래 생성한 transformation을 사용하여 자동으로 재계산된다.

또한, 각 저장된 RDD는 다른 저장 수준을 사용하여 저장될 수 있다.
예를 들어, 데이터셋을 디스크에 저장하거나 메모리에 직렬화된 Java 객체로 저장(공간을 절약하기 위해)하거나 노드 간에 복제하는 등의 방법이 있다.
이러한 수준은 `persist()`에 StorageLevel 객체([Scala](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/storage/StorageLevel.html), [Java](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/storage/StorageLevel.html), [Python](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.StorageLevel.html#pyspark.StorageLevel))를 전달하는 방식으로 설정된다.
`cache()` 메서드는 기본 저장 수준인 `StorageLevel.MEMORY_ONLY`(메모리에 직렬화되지 않은 객체를 저장)을 사용하는 약칭이다. 
사용 가능한 모든 저장 수준은 다음과 같다.

|Storage|Level	Meaning|
|-------|--------------|
|MEMORY_ONLY|JVM 내의 역직렬화된 Java 객체로 RDD를 저장한다. RDD가 메모리에 맞지 않으면 일부 파티션은 캐시되지 않고 필요할 때마다 동적으로 재계산된다. 이것이 디폴트 레벨이다.|
|MEMORY_AND_DISK|JVM 내의 역직렬화된 Java 객체로 RDD를 저장한다. RDD가 메모리에 맞지 않으면 메모리에 맞지 않는 파티션을 디스크에 저장하고 필요할 때 그곳에서 읽는다.|
|MEMORY_ONLY_SER(Java and Scala)|각 파티션당 하나의 바이트 배열로 직렬화된 Java 객체로 RDD를 저장한다. 일반적으로 빠른 직렬화 프로그램을 사용할 때 역직렬화 객체를 사용하는 것 보다 특히 더 공간 효율적이지만, 읽는 데 CPU 부하가 더 많다.|
|MEMORY_AND_DISK_SER(Java and Scala)|MEMORY_ONLY_SER와 유사하지만, 메모리에 맞지 않는 파티션을 필요할 때마다 동적으로 재계산하는 대신 디스크로 스피릴링(spilling)한다.|
|DISK_ONLY|파티션을 디스크에만 저장한다.|
|MEMORY_ONLY_2, MEMORY_AND_DISK_2, etc.|MEMORY_AND_DISK_2 등 위의 수준과 동일하지만, 각 파티션을 클러스터 노드 두 개에 복제한다.|
|OFF_HEAP(experimental)|MEMORY_ONLY_SER와 유사하지만, 데이터를 오프-힙 메모리에 저장한다. 이때 오프-힙 메모리가 활성화되어 있어야 한다.|

> 오프-힙(Off-Heap) 메모리는 JVM의 힙(heap) 영역 외부에 데이터를 저장하는 메모리 공간을 의미한다. 일반적으로 Java 애플리케이션은 JVM의 힙 내에서 객체를 할당하고 관리하지만, 오프-힙 메모리는 JVM의 힙 영역을 벗어나 있는 메모리 공간을 참조한다.

주의: Python에서 저장된 객체는 항상 Pickle 라이브러리로 직렬화된다. 따라서 직렬화 수준을 선택하는 것은 중요하지 않다. 
Python에서 사용 가능한 저장 수준에는 MEMORY_ONLY, MEMORY_ONLY_2, MEMORY_AND_DISK, MEMORY_AND_DISK_2, DISK_ONLY, DISK_ONLY_2, DISK_ONLY_3이 포함된다.

Spark는 사용자가 `persist`를 호출하지 않더라도 shuffle 연산(예: `reduceByKey`)에서 일부 중간 데이터를 자동으로 저장한다. 이는 shuffle 중에 노드가 실패할 경우 전체 입력을 다시 계산하는 것을 피하기 위해 수행된다. 사용자가 결과 RDD를 재사용할 계획이 있다면 여전히 `persist`를 호출하는 것을 권장한다.

### Which Storage Level to Choose?
Spark의 저장 수준은 메모리 사용과 CPU 효율성 사이의 다른 trade-off를 제공하기 위해 설계되었다. 다음 과정을 통해 하나를 선택하는 것을 추천한다.
- RDDs가 기본 저장 수준(MEMORY_ONLY)에 편안하게 맞는다면 그대로 사용해라. 이것은 가장 CPU 효율적인 옵션으로, RDDs의 연산이 가능한 한 빠르게 실행되게 한다.
- 그렇지 않다면, (Java와 Scala의 경우) MEMORY_ONLY_SER를 사용하고 빠른 직렬화 라이브러리를 선택하여 객체를 훨씬 더 공간 효율적으로 만들어라. 여전히 상대적으로 빠르게 액세스할 수 있다. 
- 데이터셋을 계산하는 함수가 비용이 많이 들거나 데이터의 큰 부분을 필터링한다면 디스크로 스피릴링(spill)하지 않는 것이 좋다. 그렇지 않으면, 파티션을 다시 계산하는 것이 디스크에서 읽는 것만큼 빠를 수 있다.
- 웹 애플리케이션의 요청을 처리하기 위해 Spark를 사용하는 경우와 같이 빠른 장애 복구를 원한다면 복제된 저장 수준(replicated storage level)을 사용하라. 모든 저장 수준은 데이터의 손실을 다시 계산함으로써 완전한 장애 허용성을 제공하지만, 복제된 수준은 손실된 파티션을 다시 계산하기를 기다리지 않고도 RDD에서 작업을 계속 실행할 수 있게 해준다.

### Removing Data
Spark는 각 노드에서 캐시 사용량을 자동으로 모니터링하고 가장 최근에 사용되지 않은 순서(Least-Recently-Used, LRU)로 오래된 데이터 파티션을 제거한다. 
캐시에서 데이터가 자동으로 제거되는 것을 기다리는 대신 RDD를 수동으로 제거하려면 `RDD.unpersist()` 메서드를 사용하라. 
이 메서드는 기본적으로 블록되지 않는다. 리소스가 해제될 때까지 블록하려면 이 메서드를 호출할 때 `blocking=true`를 지정하라.

## RDD 요약
RDD는 불변성(Immutable)을 가지며, 여러 노드에 분산되어 저장되는 분산 컬렉션이다.
RDD는 Spark의 핵심 데이터 모델로 사용되며, 다양한 연산을 지원하여 데이터 처리 및 분석 작업을 수행할 수 있다.

RDD의 주요 특징과 동작 방식은 다음과 같다.
- 불변성(Immutable): RDD는 변경할 수 없는 데이터 구조로, RDD는 생성된 후에는 수정할 수 없으며, 새로운 RDD를 생성하여 변환 작업을 수행한다. 이는 데이터의 일관성과 안정성을 보장한다.
- 분산성(Distributed): RDD는 여러 개의 노드에 분산하여 저장되는 데이터 구조이다. RDD는 클러스터의 여러 노드에 분할되어 저장되며, 각 노드에서 동시에 처리될 수 있다.
- 탄력성(Resilient): RDD는 데이터의 손실을 방지하기 위해 장애에 대처할 수 있는 기능을 가지고 있다. RDD는 특정 노드에서 실패하더라도 다른 노드에서 재계산이 가능하므로 데이터의 내구성을 보장한다.
- 지연 평가(Lazy Evaluation): RDD는 지연 평가(Lazy Evaluation) 방식을 사용하여 연산을 지연시킨다. RDD에 연산을 수행해도 결과가 즉시 계산되지 않고, 실제로 데이터가 필요한 시점에서만 연산이 수행된다. 
이를 통해 최적화된 실행 계획을 수립하고 연산 성능을 향상시킬 수 있다.

RDD는 다양한 연산을 지원하여 데이터 처리를 유연하게 수행할 수 있다. 주요 RDD 연산에는 변환 연산(Transformations)과 액션 연산(Actions)이 있다.
- 변환 연산(Transformations): RDD를 변형하여 새로운 RDD를 생성하는 연산이다. 예를 들어, `map`, `filter`, `reduceByKey` 등의 연산을 사용하여 RDD의 요소를 변환, 필터링하거나 그룹화할 수 있다.
- 액션 연산(Actions): RDD에서 결과 값을 반환하는 연산이다. 예를 들어, `count`, `collect`, `reduce` 등의 연산을 사용하여 RDD의 요소를 계산하거나 수집할 수 있다.

RDD는 Spark의 다른 고수준 API인 DataFrame과 Dataset으로 변환될 수 있으며, 더 직관적이고 효율적인 데이터 조작을 위해 사용될 수 있다.
따라서, Spark RDD는 분산되고 탄력적이며, 다양한 변환과 액션 연산을 지원하는 기본적인 데이터 구조로 사용되는 중요한 개념이다.

# Shared Variables
일반적으로 Spark 작업(map 또는 reduce)에 전달된 함수가 원격 클러스터 노드에서 실행될 때, 함수에서 사용되는 모든 변수의 별도의 복사본에 대해 동작한다.
이러한 변수들은 각 머신에 복사되며, 원격 머신의 변수에 대한 업데이트는 드라이버 프로그램으로 다시 전파되지 않는다. 
모든 작업 간에 일반적인 읽기-쓰기 공유 변수를 지원하는 것은 비효율적일 것이다. 
그러나 Spark는 두 가지 일반적인 사용 패턴을 위해 두 가지 제한된 유형의 공유 변수, 즉 브로드캐스트(broadcast) 변수와 어큐뮬레이터(accumulator)를 제공한다.

## Broadcast Variables
Broadcast variables allow the programmer to keep a read-only variable cached on each machine rather than shipping a copy of it with tasks. They can be used, for example, to give every node a copy of a large input dataset in an efficient manner. Spark also attempts to distribute broadcast variables using efficient broadcast algorithms to reduce communication cost.

Spark actions are executed through a set of stages, separated by distributed “shuffle” operations. Spark automatically broadcasts the common data needed by tasks within each stage. The data broadcasted this way is cached in serialized form and deserialized before running each task. This means that explicitly creating broadcast variables is only useful when tasks across multiple stages need the same data or when caching the data in deserialized form is important.

Broadcast variables are created from a variable v by calling SparkContext.broadcast(v). The broadcast variable is a wrapper around v, and its value can be accessed by calling the value method. The code below shows this:
```
>>> broadcastVar = sc.broadcast([1, 2, 3])
<pyspark.broadcast.Broadcast object at 0x102789f10>

>>> broadcastVar.value
[1, 2, 3]
```
After the broadcast variable is created, it should be used instead of the value v in any functions run on the cluster so that v is not shipped to the nodes more than once. In addition, the object v should not be modified after it is broadcast in order to ensure that all nodes get the same value of the broadcast variable (e.g. if the variable is shipped to a new node later).

To release the resources that the broadcast variable copied onto executors, call .unpersist(). If the broadcast is used again afterwards, it will be re-broadcast. To permanently release all resources used by the broadcast variable, call .destroy(). The broadcast variable can’t be used after that. Note that these methods do not block by default. To block until resources are freed, specify blocking=true when calling them.

## Accumulators
Accumulators are variables that are only “added” to through an associative and commutative operation and can therefore be efficiently supported in parallel. They can be used to implement counters (as in MapReduce) or sums. Spark natively supports accumulators of numeric types, and programmers can add support for new types.

As a user, you can create named or unnamed accumulators. As seen in the image below, a named accumulator (in this instance counter) will display in the web UI for the stage that modifies that accumulator. Spark displays the value for each accumulator modified by a task in the “Tasks” table.

<img src="https://github.com/skybluelee/Archeive/assets/107929903/f125a294-4e2c-49ad-b575-21fad4a94bec.png" width="1000" height="500"/>

Tracking accumulators in the UI can be useful for understanding the progress of running stages (NOTE: this is not yet supported in Python).

An accumulator is created from an initial value v by calling SparkContext.accumulator(v). Tasks running on a cluster can then add to it using the add method or the += operator. However, they cannot read its value. Only the driver program can read the accumulator’s value, using its value method.

The code below shows an accumulator being used to add up the elements of an array:
```
>>> accum = sc.accumulator(0)
>>> accum
Accumulator<id=0, value=0>

>>> sc.parallelize([1, 2, 3, 4]).foreach(lambda x: accum.add(x))
...
10/09/29 18:41:08 INFO SparkContext: Tasks finished in 0.317106 s

>>> accum.value
10
```
While this code used the built-in support for accumulators of type Int, programmers can also create their own types by subclassing AccumulatorParam. The AccumulatorParam interface has two methods: zero for providing a “zero value” for your data type, and addInPlace for adding two values together. For example, supposing we had a Vector class representing mathematical vectors, we could write:
```
class VectorAccumulatorParam(AccumulatorParam):
    def zero(self, initialValue):
        return Vector.zeros(initialValue.size)

    def addInPlace(self, v1, v2):
        v1 += v2
        return v1

# Then, create an Accumulator of this type:
vecAccum = sc.accumulator(Vector(...), VectorAccumulatorParam())
```
For accumulator updates performed inside actions only, Spark guarantees that each task’s update to the accumulator will only be applied once, i.e. restarted tasks will not update the value. In transformations, users should be aware of that each task’s update may be applied more than once if tasks or job stages are re-executed.

Accumulators do not change the lazy evaluation model of Spark. If they are being updated within an operation on an RDD, their value is only updated once that RDD is computed as part of an action. Consequently, accumulator updates are not guaranteed to be executed when made within a lazy transformation like map(). The below code fragment demonstrates this property:
```
accum = sc.accumulator(0)
def g(x):
    accum.add(x)
    return f(x)
data.map(g)
# Here, accum is still 0 because no actions have caused the `map` to be computed.
```
