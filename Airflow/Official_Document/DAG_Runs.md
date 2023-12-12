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
Airflow DAG은 `start_date`(`end_date`이 존재할 수도 있음), 그리고 비 데이터셋(non-dataset) 스케줄로 정의되며, 스케줄러는 이를 개별 DAG 실행으로 변환하여 실행한다. 
스케줄러는 기본적으로 마지막 데이터 간격 이후에 실행되지 않은(혹은 실행 기록이 지워진 경우) 모든 데이터 간격에 대해 DAG 실행을 시작한다. 이 개념을 **Catchup**이라고 한다.

만약 DAG이 자체 catchup을 처리하지 않도록 작성되지 않았다면(다시 말하면 간격이 아닌 현재 시간에 제한되어 있는 경우), catchup을 끄고 싶을 것이다. 
이는 DAG에서 `catchup=False`를 설정하거나 설정 파일에서 `catchup_by_default=False`로 설정하여 수행할 수 있다. catchup을 끄면 스케줄러는 최신 간격에 대해서만 DAG Run을 생성한다.
```
"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/main/airflow/example_dags/tutorial.py
"""
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

import datetime
import pendulum

dag = DAG(
    "tutorial",
    default_args={
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": datetime.timedelta(minutes=3),
    },
    start_date=pendulum.datetime(2015, 12, 1, tz="UTC"),
    description="A simple tutorial DAG",
    schedule="@daily",
    catchup=False,
)
```
위의 예에서 DAG이 스케줄러 데몬에서 2016-01-02 6시에 선택된 경우(또는 CLI에서 실행하는 경우), 2016-01-01부터 2016-01-02까지의 데이터 간격으로 단일 DAG Run이 생성되고, 
다음 DAG Run은 2016-01-02 새벽 자정 이후에 데이터 간격이 2016-01-02에서 2016-01-03으로 생성된다.

`datetime.timedelta` 객체를 스케줄로 사용하는 경우 다르게 동작할 수 있음에 주의해야 한다.
이 경우에는 생성된 단일 DAG 실행이 2016-01-01 06:00부터 2016-01-02 06:00까지의 데이터를 포함하게 된다(현재 시간을 기준으로 끝나는 하나의 스케줄 간격).
cron 표현식과 델타 기반 스케줄 간의 차이에 대한 더 자세한 설명은 [timetables comparison](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html#differences-between-the-cron-and-delta-data-interval-timetables)을 참조하라.

`dag.catchup` 값이 `True`인 경우 스케줄러는 2015-12-01부터 2016-01-02까지 완료된 각 간격에 대해 DAG Run을 생성한다(아직 완료되지 않은 2016-01-02 간격에 대한 실행은 생성되지 않는다). 그리고 스케줄러는 이를 순차적으로 실행한다.

또한 DAG을 특정 기간 동안 끄고 다시 활성화하면 `catchup`이 트리거된다.

이 동작은 쉽게 기간으로 나뉠 수 있는 원자적(atomic) 데이터셋에 적합하다. DAG가 내부적으로 `catchup`을 수행하는 경우 `catchup`을 끄는 것이 좋다.
## Backfill
가끔은 특정한 기간에 대해 DAG을 실행하고 싶을 수 있다. 
예를 들어, 데이터 채우기 DAG가 start_date를 2019-11-21로 가지고 있지만, 다른 사용자가 한 달 전, 즉 2019-10-21의 출력 데이터를 요청하는 경우가 있을 수 있다. 이 과정을 Backfill이라고 한다.

Backfill은 이전의 데이터 간격에 대해 DAG을 실행하여 역사적인(historical) 데이터를 채우는 작업을 의미한다.
이는 데이터 웨어하우스나 데이터 레이크에 이전 데이터를 업데이트하거나 채우는 데 유용할 수 있다.
백필은 데이터 간격을 건너뛰거나 놓치지 않고 특정 기간 동안의 작업을 수행하는 데 도움이 된다.

Airflow에서는 `catchup` 설정을 사용하여 이러한 백필 작업을 쉽게 처리할 수 있다. `catchup`을 활성화하면 지정된 시작 날짜부터 현재까지의 모든 데이터 간격에 대해 DAG이 실행된다.
따라서 `catchup`을 활성화하여 이전 데이터를 채우는 백필 작업을 수행할 수 있다.
***
```
airflow dags backfill \
    --start-date START_DATE \
    --end-date END_DATE \
    dag_id
```
`catchup`이 비활성화 되어 있는 상태에서 Backfill을 사용하고 싶은 경우, 위의 코드를 CLI에서 사용할 수 있다.

[backfill 명령어](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#backfill)는 해당 DAG의 start_date과 end_date 사이의 모든 시간 간격에 대해 재실행을 진행한다.
## Re-run Tasks
몇몇 task는 계획된 실행 중에 실패하기도 한다. 로그를 통해 오류를 수정하고 나면, 사용자는 예약된 날짜에 대한 작업을 지워서(clear) 재실행할 수 있다. 
작업 인스턴스를 지우면 작업 인스턴스 레코드가 삭제되지 않는다. 대신, `max_tries`를 0으로 업데이트하고 현재 작업 인스턴스 상태를 `None`으로 설정하여 작업을 다시 실행하게 된다.

실패한 task를 클릭하고, **clear** 버튼을 누르면, executor가 해당 task를 재실행한다.

재실행 옵션은 아래와 같다.
- Past: DAG의 가장 최근 데이터 간격 이전 실행에서의 작업의 모든 객체
- Future: DAG의 가장 최근 데이터 간격 이후 실행에서의 작업의 모든 객체
- Upstream: 현재 DAG에서의 상위 작업
- Downstream: 현재 DAG에서의 하위 작업
- Recursive: 자식 DAG 및 부모 DAG의 모든 작업
- Failed: DAG의 가장 최근 실행에서 실패한 작업들만
***
```
airflow tasks clear dag_id \
    --task-regex task_regex \
    --start-date START_DATE \
    --end-date END_DATE
```
CLI 명령을 통해서도 task를 지울 수 있다.
***
```
airflow tasks clear --help
```
지정된 `dag_id`와 시간 간격에 대한 명령은 해당 정규식과 일치하는 모든 작업 객체를 지울 수 있다. 
더 많은 옵션에 대해서는 [clear 명령어](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#clear)의 도움말을 확인하라.
# External Triggers
DAG Run은 CLI를 통해서도 수동으로 생성될 수 있다.
```
airflow dags trigger --exec-date logical_date run_id
```
스케줄러 외부에서 생성된 DAG Run은 해당 트리거의 타임스탬프와 연관되며 예약된 DAG Run과 함께 UI에서 표시된다. 
DAG 내부에서 전달된 논리적인 날짜는 `-e` 인수를 사용하여 지정할 수 있다. 디폴트 값은 현재 UTC 시간대의 현재 날짜이다.

또한 웹 UI를 사용하여 수동으로 DAG Run을 트리거할 수도 있습니다(UI에서 "DAGs" 탭 -> 열 링크 -> "Trigger Dag" 버튼).
## DAG 트리거 중에 파라미터 생략하기
```
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    "example_parameterized_dag",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)

parameterized_task = BashOperator(
    task_id="parameterized_task",
    bash_command="echo value: {{ dag_run.conf['conf1'] }}",
    dag=dag,
)
```
CLI나 API 또는 UI를 통해 트리거하는 동안 JSON 블롭으로 DAG Run에 대한 설정을 생략하는 것이 가능하다.

`dag_run.conf` 파라미터는 operator 템플릿 필드 내에서만 사용할 수 있음을 유의하라.
### CLI 사용
```
airflow dags trigger --conf '{"conf1": "value1"}' example_parameterized_dag
```
### UI 사용
<img src="https://github.com/skybluelee/Archeive/assets/107929903/9a80f165-d4b3-4fde-acc0-a26ed0936733.png" width="9000" height="500"/>
