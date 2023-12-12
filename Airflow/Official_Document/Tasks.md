**본 문서는 Airflow 공식 문서 [Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html)를 참조함**
# Tasks
task는 Airflow에서의 기본 실행 단위이다. task는 DAG 내부로 정렬되고, task의 실행 순서를 표현하기 위해 upstream과 downstream으로 의존성을 갖고 있다.

task에는 크게 3가지 종류가 있다.
- [Operator](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html): DAG의 대부분을 빠르게 구축할 수 있는 미리 정의된 작업 템플릿이다.
- [Sensor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html): 외부 이벤트가 발생하기를 기다리는 것과 관련된 특수한 연산자의 하위 클래스이다.
- [`@task`로 데코레이트된 Taskflow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html): 사용자가 정의한 Python 함수를 특별한 Task로 패키징하는 방법이다.


내부적으로 task는 모두 Airflow의 `BaseOperator`의 하위 클래스이다. 
Task와 Operator의 개념은 어느 정도 교환 가능하지만, 이들을 별도의 개념으로 생각하는 것이 유용하다. 
본질적으로 Operators와 Sensors는 템플릿이며, DAG 파일에서 하나를 호출할 때 Task를 만드는 것으로 생각할 수 있다.

# Relationships
task를 사용하는 것에 있어 주요 부분은 task끼리의 관계를 정의하는 것 - task간의 의존성 즉 Airflow에서 말하는 upstream, downstream task를 의미한다.
사용자는 task를 먼저 선언하고, 그 이후에 의존성을 선언한다.

upstream task는 해당 task의 바로 위에 있는 task를 말한다. 과거에는 부모 task라고 불렀었다.
upstream이라는 개념은 계층 구조 상 위에 있는 task를 묘사하는 것이 아니라 바로 위의 task를 지칭한다.
downstream도 동일하게 적용되며, 바로 밑의 자식 task를 의미한다.

의존성을 선언하는 방식은 2가지가 있다.
- `>>`, `<<` 연산자(bitshift) 사용하기.
```
first_task >> second_task >> [third_task, fourth_task]
```
- `set_upstream`, `set_downstream` 사용하기.
```
first_task.set_downstream(second_task)
third_task.set_upstream(second_task)
```
2가지 방식은 정확인 동일하게 동작하나, 일반적으로 읽기 쉬운 bitshift 연산자를 추천한다.

기본적으로, task는 upstream task가 성공하는 경우에만 실행되지만, 분기를 추가하거나 몇가지의 upstream task에 대해서만 대기하거나 실행 이력에서 현재 실행을 기반으로 행동 방식을 바꾸는 등으로 변형하는 여러가지 방법이 있다.
이는 [Control Flow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#concepts-control-flow)에서 확인할 수 있다.

task는 기본적으로 task간에 정보를 전달하지 않으며 완전히 독립적으로 실행된다. 만약 task간에 정보를 전송하고 싶다면, [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)를 사용하면 된다.

# Task 객체
DAG가 실행될 때마다 DAG가 DAG Run으로 객체화되는 것과 유사하게, DAG 아래의 작업은 task 객체로 객체화된다.

task의 객체는 해당 DAG에 대한 특정 실행(따라서 특정 데이터 간격에 대한 실행)을 의미한다. 또한 task의  생명주기의 어떤 단계에 있는지를 나타내는 상태이기도 하다.

task 객체의 가능한 상태 목록은 아래와 같다.
- `none`: task가 아직 실행을 위해 대기 중이며, 의존성이 아직 충족되지 않은 상태이다.
- `scheduled`: 스케줄러가 작업의 의존성이 충족되었고 실행되어야 함을 결정한 상태이다.
- `queued`: task가 Executor에 할당되었으며 워커를 기다리고 있는 상태이다.
- `running`: task가 워커에서 실행 중인 상태이다(또는 로컬/동기 실행기에서 실행 중인 상태).
- `success`: task가 오류 없이 실행이 완료된 상태이다.
- `restarting`: task가 실행 중인 상태에서 외부에서 다시 시작하도록 요청된 상태이다.
- `failed`: task가 실행 중에 오류가 발생하여 실패한 상태이다.
- `skipped`: task가 분기, LatestOnly 등으로 인해 건너뛰어진 상태이다.
- `upstream_failed`: 상위 task가 실패하고 트리거 규칙에 따라 해당 작업이 필요한 상태이다.
- `up_for_retry`: task가 실패했지만 재시도 시도 기회가 있어 reschedule 될 예정인 상태이다.
- `up_for_reschedule`: 센서인 작업이 `reschedule` 모드에 있는 상태이다.
- `deferred`: task가 트리거로 인해 지연된 상태이다.
- `removed`: task가 DAG에서 실행이 시작된 이후에 DAG에서 삭제된 상태이다.

<img src="https://github.com/skybluelee/Archeive/assets/107929903/0678eb24-2c58-4b40-9892-b020553e3374.png" width="1000" height="700"/>

task는 `none` -> `scheduled` -> `queued` -> `running` -> `success` 순서의 흐름을 갖는 것이 이상적이다.

사용자 지정 task(혹은 operator)가 실행중일 때, 해당 task는 task 객체의 복사본을 전달받는다.
task 메타데이터를 검사할 뿐만 아니라 [XCom](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)과 같은 작업에 대한 메서드도 포함되어 있다.
## Relationship Terminology(DAG 내에서 각 task 객체 간의 상호 작용과 관련된 용어와 개념)
task 객체가 주어지면, 다른 객체와의 관계를 나타내는 것에는 2가지 유형이 존재한다.
```
task1 >> task2 >> task3
```
첫째로 upstream과 downstream task이다.

DAG가 실행중일 때, 해당 DAG에 대한 각 task의 upstream, downstream에 대한 객체를 생성하며, 객체는 동일한 데이터 간격을 갖는다.

동일한 task에 대한 여러 객체가 있을 수 있다. 
그러나 이들은 동일한 DAG의 다른 실행에서 나온 것일 수 있다. 이러한 관계를 나타내기 위해 "이전(previous)"과 "다음(next)"이라는 용어를 사용한다. 이는 upstream, downstream과는 다른 관계이다.

주의: 과거의 Airflow 문서 중 일부는 "이전"을 "상위 스트림"을 의미하는 용어로 사용할 수 있다.

# 시간 초과(Timeouts)
작업이 최대 실행 시간을 가져야 하는 경우 `execution_timeout` 속성을 설정하여 최대 허용 실행 시간을 나타내는 `datetime.timedelta` 값을 설정하면 된다. 
이는 sensor를 포함한 모든 Airflow task에 적용된다. 
`execution_timeout`은 각 실행에 대해 허용되는 최대 시간을 제어한다.
`execution_timeout`이 초과되면 작업이 타임아웃되고 `AirflowTaskTimeout`이 발생한다.

또한 sensor에는 `timeout` 파라미터가 있다. 
이는 sensor가 `reschedule` 모드에 있을 때만 중요하다.
`timeout`은 센서가 성공하기까지 허용되는 최대 시간을 제어한다. 
`timeout`이 초과되면 `AirflowSensorTimeout`이 발생하고 sensor는 재시도 없이 즉시 실패한다.

아래의 `SFTPSensor` 예시는 이를 설명한다.
`sensor`는 `reschedule` 모드이며, 이는 성공할 때까지 주기적으로 실행되고 reschedule 되는 것을 의미한다.
- 센서가 SFTP 서버를 확인할 때마다 실행 시간은 `execution_timeout`에 정의된 대로 최대 60초까지 허용된다.
- 만약 센서가 SFTP 서버를 확인하는 데 60초보다 더 오래 걸린다면 `AirflowTaskTimeout`이 발생하며 이때 센서는 재시도할 수 있다. 이때 재시도 횟수는 `retries`에 정의된 대로 최대 2회까지 가능하다.
- 첫 실행 시작부터 성공할 때까지(즉, 파일 'root/test'이 나타난 후) 센서는 `timeout`에 정의된 대로 최대 3600초까지 허용된다.
다시 말해, 파일이 3600초 이내에 SFTP 서버에 나타나지 않으면 센서는 `AirflowSensorTimeout`을 발생시며, 이 오류가 발생하더라도 재시도하지 않는다.
- 센서가 3600초 간격 동안 네트워크 장애와 같은 다른 이유로 실패하면 `retries`에 정의된 대로 최대 2회까지 재시도할 수 있다. 재시도는 `timeout`을 재설정하지 않으며, 성공할 때까지 최대 3600초의 시간이 주어진다.

ㅇㅇ
