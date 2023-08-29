# Kafka Stream vs Spark Stream
[Apache Kafka Vs Apache Spark](https://www.knowledgehut.com/blog/big-data/kafka-vs-spark)를 참조하여 작성하였다.
## Kafka Stream
Kafka Stream은 밀리초 이내의 지연시간을 갖춘 초 단위의 스트림 처리를 제공한다. Kafka Stream은 데이터를 처리하고 저장하는 용도의 클라이언트 라이브러리이다. Kafka Stream은 2가지 방식으로 데이터를 처리한다.
- Kafka -> Kafka
	- Kafka Stream이 집계, 필터링 등을 수행하고 데이터를 다시 Kafka로 전송하는 경우, Kafka는 확장성, 고가용성, 높은 처리율 등을 달성할 수 있다.
- Kafka -> 외부 시스템(Database, Data Science Model 등)
	- 주로 특정 스트리밍 라이브러리(Spark, FLink, Nifi 등)이 Kafka를 메시지 전송 수단으로 활용한다. Kafka에서 메시지를 읽고 메시지 추가 처리하기 위해 작은 시간 창으로 분할한다.
    
Kafka Stream은 이벤트 시간과 처리 시간, 윈도우 처리와 간단한 애플리케이션 상태 관리를 적절하게 구분하기 위한 중요한 스트림 처리 개념 위에 구축되었다. Kafka Streams는 이미 파티션 분할을 통한 확장(Scaling)과 같이 Kafka에 포함된 여러 개념에 기반을 두고 있다.
## Spark Streaming
Spark Streaming은 실시간 입력 데이터 스트림을 수신하고, 특정 시간 동안 데이터를 수집하고, RDD를 만들고, 미니 배치로 데이터를 분할하고, 미니 배치를 처리하여 최종 결과 스트림을 생성한다.

Spark Streaming은 DStream(Discretized Stream)이라 불리는 높은 수준의 추상화를 제공하는데, DStream은 연속적인 데이터 스트림을 의미한다.

DStream은 Kafka, Flume, Kinesis와 같은 입력 데이터 스트림으로부터도 생성될 수 있다. 내부적으로 DStream은 RDD의 결과물로 표현된다.


## 간단 비교
|비교 대상|Spark Streaming|Kafka Streams|
|------|------|-------|
|데이터 처리 방식|실시간 입력 데이터 스트림으로부터 수신된 데이터는 <br> 처리를 위해 작은 배치로 분할됨|데이터 스트림 단위로 처리|
|클러스터 여부|별도의 처리 클러스터가 필요|변도의 처리 클러스터가 필요하지 않음|
|스케일링|스케일링 시 구성 변경 필요|자바 프로세스를 통한 스케일링 진행으로 <br> 구성 변경 필요 없음|
|데이터 처리 방식|At least one semantics <br> 데이터가 한번 이상 처리될 수 있음 <br> 네트워크 문제 또는 시스템 장애와 같은<br> 예기치 않은 이벤트로 인해 데이터가 중복으로 처리될 수 있음|Exactly one semantics <br> 데이터가 정확히 한 번만 처리 <br> 데이터 처리 시스템이 어떤 이유에서든지 중복 처리를 <br> 하지 않고도데이터 손실을 방지|
|작업|Spark Streaming은 그룹 단위로 처리하는 작업에 적합 <br> (group by, ML, window functions 등)|Kafka Stream은 한번에 하나의 레코드를<br>처리하는 능력을 제공 <br> 행 파싱, 데이터 정제 작업에 적합|
|작동 위치|Spark Streaming은 standalone 프레임임<br>다른 프레임워크나 시스템과 연동하지 않고도 독립적으로 작동|Kafka Stream은 MSA나 다른 애플리케이션<br>내부의 라이브러리로 사용 가능|
|저장|Spark은 분산 환경에 데이터를 저장하기 위해 RDD를 사용|Kafka는 토픽에 데이터를 저장|
## 상세 비교
**Latency**
지연이 고려사항이 아니거나, 데이터 호환성이 필요하다면 Spark이 Kafka보다 더 좋은 선택이다. 반면에 지연이 중대한 조건이고 밀리초 이내의 실시간 처리과정이 필요하다면 Kafka가 최고의 선택이다.

Kafka는 이벤트 기반 처리 덕분에 더 좋은 내공장성을 제공한다. 하지만 다른 시스템과 통합하거나 데이터를 다른 시스템과 공유하는 것이 매우 어렵다.

**Processing Type**
Kafka는 이벤트가 발생하는데로 분석하고 지속적인 처리 모델을 제공한다.

Spark은 일괄 처리 방식(batch processing)을 사용하여 입력 스트림을 작은 배치로 나누어 처리한다. 즉 일부 지연이 발생할 수 있으나, 대용량 데이터 처리에 적합하다.
**Memory Management**
Spark는 분산 환경에서 데이터를 제장하기 위해 RDD를 사용한다. RDD 내부의 각 데이터는 몇몇 클러스터 노드에 의해 계산되어 논리적으로 분할된다.

Kafka는 데이터를 토픽 또는 메모리 버퍼에 저장한다. 파티션이 Kafka의 기본적인 저장 단위이며, 로그를 확인하여 Kafka가 파티션을 저장하는지 확인할 수 있다. Kafka는 특정 메시지를 찾고 삭제하기 위해 파티션을 세그먼트에 저장한다. 세그먼트의 기본 단위는 1GB이다. 프로듀서에 의해 생성된 새로운 메시지는 이전 세그먼트가 가득 차 있는지와 상관없이 새로운 세그먼트에 저장된다.
