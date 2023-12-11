**본 문서는 Airflow 공식 문서 [DAG Runs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html)를 참조함**
# DAG Runs
DAG Run은 시간상에서 DAG의 구체적인 인스턴스를 나타내는 객체이다.
DAG가 실행될 때마다 DAG Run이 생성되고 그 안의 모든 task가 실행된다. 
DAG Run의 상태는 task의 상태에 따라 결정된다.
각 DAG Run은 서로 별개로 실행되므로 동시에 여러 번의 DAG 실행이 가능하다.
# DAG Run 상태
DAG Run의 상태는 DAG의 실행이 완료될 때 결정된다. DAG의 실행은 해당 task 및 task 간의 종속성에 달려 있다.
DAG Run의 상태는 모든 작업이 성공(`success`), 실패(`failed`) 또는 건너뛰기(`skipped`)와 같은 최종 상태 중 하나에 있을 때 (다른 상태로의 전환 가능성이 없을 경우) 할당된다.
DAG Run의 상태는 일반적으로 "리프 노드(leaf nodes)" 또는 간단히 "리프(leaves)"라고 불리는 작업을 기반으로 할당된다. 리프 노드는 자식이 없는 task이다.

DAG Run에 대한 최종 상태에는 2가지가 존재한다.
- 만약 모든 리프 노드 상태가 `success`이거나 `skipped`인 경우: `success`
- 특정 리프 노드 상태가 failed이거나 `upstream_failed`인 경우: `failed`

주의해야 할 점은 일부 작업이 특정 트리거 규칙을 정의했을 때다.
이로 인해 예상치 못한 동작이 발생할 수 있다. 
예를 들어, 트리거 규칙이 `all_done`으로 설정된 리프 작업이 있다면 나머지 작업의 상태에 관계없이 실행될 것이며, 이 작업이 성공하면 중간에 어떤 작업이 실패했더라도 전체 DAG Run도 성공으로 표시될 것이다.

(Airflow 2.7 버전에 추가됨)

현재 실행 중인 DAG Run이 있는 DAG는 UI 대시보드의 "Running" 탭에 표시될 수 있다. 
마찬가지로, 가장 최근의 DAG Run이 실패로 표시된 DAG는 "Failed" 탭에서 찾을 수 있다.
# Cron Presets(표현식)
DAG를 간단한 일정에 맞게 실행하려면 해당 DAG의 schedule 인수를 cron 표현식, `datetime.timedelta` 객체 또는 미리 정의된 cron "presets" 중 하나로 설정할 수 있다.
더 복잡한 일정 요구 사항의 경우 [사용자 정의 타임테이블](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html)을 구현할 수 있다.

|preset|meaning|cron|
|------|------|-----|
|`None`|Don’t schedule, use for exclusively “externally triggered” DAGs||
|`@once`|Schedule once and only once||
|`@continuous`|Run as soon as the previous run finishes||
|`@hourly`|Run once an hour at the end of the hour|0 * * * *|
|`@daily`|Run once a day at midnight (24:00)|0 0 * * *|
|`@weekly`|Run once a week at midnight (24:00) on Sunday|0 0 * * 0|
|`@monthly`|Run once a month at midnight (24:00) of the first day of the month|0 0 1 * *|
|`@quarterly`|Run once a quarter at midnight (24:00) on the first day|0 0 1 */3 *|
|`@yearly`|Run once a year at midnight (24:00) of January 1|0 0 1 1 *|

DAG는 각 일정에 대해 별도로 인스턴스화되며 해당 DAG의 실행에 대한 데이터베이스 백엔드에 해당하는 DAG Run 항목이 만들어진다.
## 데이터 간격(Data Interval)
Airflow에서 각 DAG 실행은 작동하는 시간 범위를 나타내는 "데이터 간격"이 할당된다.
예를 들어 `@daily`로 예약된 DAG의 경우 각 데이터 간격은 일반적으로 매일 자정 (00:00)에 시작하여 자정 (24:00)에 끝난다.

보통 DAG Run은 연관된 데이터 간격이 끝난 후 예약되며, 이를 통해 실행이 해당 기간 내의 모든 데이터를 수집할 수 있다.
다시 말하면, 2020-01-01의 데이터 기간을 포함하는 실행은 일반적으로 2020-01-01이 종료된 후, 즉 2020-01-02 00:00:00 이후에 실행된다.

Airflow의 모든 날짜는 어떤 방식으로든 데이터 간격 개념에 연결되어 있다. 
DAG 실행의 "논리적인 날짜(logical date)" (Airflow 2.2 이전 버전에서는 `execution_date`로 불림)는 예를 들어 데이터 간격의 시작을 나타내며, DAG가 실제로 실행되는 시간이 아니다.

마찬가지로 DAG와 해당 작업의 `start_date` 인자는 동일한 논리적인 날짜를 가리키므로 DAG의 첫 번째 데이터 간격의 시작을 나타낸다. 다시 말하면, DAG 실행은 start_date 후에 한 번만 예약된다.

만약 cron 표현식이나 timedelta 객체로는 DAG의 일정, 논리적인 날짜, 또는 데이터 간격을 표현하기에 충분하지 않다면 [Timetables](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html)을 참조하라.
논리적인 날짜에 대한 자세한 정보는 [Running DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#concepts-dag-run) 및 [What does execution_date mean?](https://airflow.apache.org/docs/apache-airflow/stable/faq.html#faq-what-does-execution-date-mean)을 참조하라.

# Re-run DAG
DAG를 다시 실행할 필요가 있는 경우(예를 들어 예정된 DAG가 실패한 경우)가 있다.

## Catchup
