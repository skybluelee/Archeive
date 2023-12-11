**본 문서는 Airflow 공식 문서 [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)를 참조함**
# DAG
**DAG**는 "Directed Acyclic Graph"의 약어로, Task와 Task 간의 의존성을 정의하는 방식을 나타낸다.
Airflow는 데이터 파이프라인을 구성하고 스케줄링하며 모니터링하기 위한 오픈 소스 플랫폼으로, DAG는 이러한 데이터 파이프라인을 표현하는 데 사용된다.

# DAG 선언
DAG를 선언하는 방법은 3가지가 존재한다.
- `with` 내에서 선언하는 경우
```
 import datetime

 from airflow import DAG
 from airflow.operators.empty import EmptyOperator

 with DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 ):
     EmptyOperator(task_id="task")
```
- DAG와 Operator를 각각 선언
```
 import datetime

 from airflow import DAG
 from airflow.operators.empty import EmptyOperator

 my_dag = DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 )
 EmptyOperator(task_id="task", dag=my_dag)
```
- `@dag` 사용
```
import datetime

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator


@dag(start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
def generate_dag():
    EmptyOperator(task_id="task")


generate_dag()
```
## task dependency
task가 여러 개인 경우 의존성을 표현해야 한다.
- `<<`, `>>`
```
first_task >> [second_task, third_task]
```
first_task가 실행된 후, second_task와 third_task가 동시에 실행된다.

```
third_task << fourth_task
```
fourth_task가 실행된 후, third_task가 실행된다.

부등호 방향에 유의!
- `set_upstream`, `set_downstream`
스트림 방향은 위에서 아래로, 즉 downstream은 `>>`를 의미하고, upstream은 `<<`를 의미한다.
```
first_task.set_downstream([second_task, third_task]) <=> first_task >> [second_task, third_task]

third_task.set_upstream(fourth_task) <=> third_task << fourth_task
```
# DAG 불러오기
Airflow는 Python 소스 파일에서 DAG를 불러온다. 이를 위해 설정된 `DAG_FOLDER` 내에서 Python 소스 파일을 찾고, Airflow는 각 파일을 가져와 실행한 다음 해당 파일에서 생성된 DAG 객체를 로드한다.

하나의 Python 파일에서 여러 DAG를 정의하고 불러올 수 있다. 단 global로 선언되어야 한다.
```
dag_1 = DAG('this_dag_will_be_discovered')

def my_function():
    dag_2 = DAG('but_this_dag_will_not')

my_function()
```
위의 경우 dag_1은 global하므로 다른 Python 파일에서 로드하여 사용가능하지만, dag_2의 경우 불가능하다.

이러한 이유는 Airflow가 `DAG_FOLDER` 내에서 DAG를 찾는 동안, 최적화를 위해 대소문자 구분없이 `airflow`와 `dag` 문자열이 포함된 파일만 고려하기 때문이다.
만약 Airflow가 모든 파일을 참조하길 원한다면 `DAG_DISCOVERY_SAFE_MODE`를 비활성화해야 한다.

DAG_FOLDER 내부 또는 그 하위 폴더에 `.airflowignore` 파일을 사용하여 로더가 무시하는 파일 패턴을 사용할 수 있다. 
`.airflowignore` 사용시 해당 파일이 속한 디렉토리와 그 하위 모든 하위 폴더를 무시한다.
자세한 내용은 아래의 `.airflowignore`를 참조.

`.airflowignore` 파일이 요구 사항을 충족시키지 못하고 Airflow가 파싱해야 할 Python 파일을 더 유연하게 제어하고 싶은 경우,
config 파일에서 `might_contain_dag_callable`을 설정하여 callable을 사용할 수 있다.
이 callable은 디폴트 Airflow 휴리스틱(대소문자를 구분없이 `airflow`, `dag` 문자열이 있는지 확인)을 대체한다.
```
def might_contain_dag(file_path: str, zip_file: zipfile.ZipFile | None = None) -> bool:
    # Your logic to check if there are DAGs defined in the file_path
    # Return True if the file_path needs to be parsed, otherwise False
```
# DAG 동작(Run)
DAG은 2가지 방식으로 동작함.
- 수동으로 혹은 API를 통한 제어
- DAG에서 정의한 schedule을 통해 동작

Airflow에서는 주로 `schedule`을 정의하여 DAG를 동작한다.
```
with DAG("my_daily_dag", schedule="@daily"):
    ...

with DAG("my_daily_dag", schedule="0 0 * * *"):
    ...
```
DAG를 동작할 때마다 사용자는 DAG Run이라는 인스턴스를 생성한다. DAG Run은 같은 DAG에 대해서도 동시에 병렬로 동작이 가능하며, DAG는 task가 실행되는 시간 간격이 정의되어 있다.

이러한 점이 유용한 하나의 예시를 들어보자. DAG는 매일 데이터셋을 처리하고 있다. 만약 사용자가 이전 3개월 동안의 모든 데이터를 처리하기 원한다면, Airflow는 **backfill**을 제공하고 이전 3개월 동안의 복사본을 실행할 수 있어,
문제없이 모든 데이터를 처리할 수 있다.

이 DAG Runs은 실제로 같은 날에 동작하지만, 각 DAG Run은 해당 3개월 기간 중 하루를 포함하는 하나의 데이터 간격(data interval)을 가지게 될 것이며, DAG 내부의 모든 작업, 연산자, 및 센서는 실행될 때 이 데이터 간격을 참조한다.

DAG가 실행될 때마다 DAG가 DAG Run으로 구체화되는 것과 유사하게, DAG 내에서 지정된 작업들 또한 DAG와 함께 Task Instance로 구체화된다.

DAG Run의 시작 및 종료 날짜 외에도 논리적 날짜(logical date) 또는 공식적으로는 실행 날짜(execution date)라고 불리는 다른 날짜가 있다.
이 날짜는 DAG Run이 예정된 또는 트리거된 시간을 나타낸다. 이것이 "논리적"이라고 불리는 이유는 DAG Run 자체의 컨텍스트에 따라 여러 의미를 가지고 있기 때문이다.

예를 들어, DAG Run이 사용자에 의해 수동으로 트리거된 경우, 해당 DAG Run의 논리적 날짜는 DAG Run이 트리거된 날짜와 시간이 되며, 이 값은 DAG Run의 시작 날짜와 동일해야 한다.
그러나 DAG가 특정한 스케줄 간격을 사용하여 자동으로 예약되는 경우, 논리적 날짜는 데이터 간격의 시작을 나타내는 시간을 표시할 것이며, DAG Run의 시작 날짜는 논리적 날짜에 스케줄 간격을 더한 값이 된다.
## 크론탭 문법
```
┌───────────── minute (0–59)
│ ┌───────────── hour (0–23)
│ │ ┌───────────── day of the month (1–31)
│ │ │ ┌───────────── month (1–12)
│ │ │ │ ┌───────────── day of the week (0–6) (Sunday to Saturday;
│ │ │ │ │                                   7 is also Sunday on some systems)
│ │ │ │ │
│ │ │ │ │
* * * * * <command to execute>
```
# DAG 할당(Assignment)
모든 단일 Operator 또는 Task를 실행하기 위해서는 DAG에 할당되어야 한다. Airflow는 DAG를 명시적으로 전달하지 않고도 몇 가지 방법으로 DAG를 계산하는 기능을 제공한다.
- `with DAG` 블록 내에서 Operator를 선언한 경우
- `@dag` 데코레이터 내에서 Operator를 선언한 경우
- DAG를 가진 Operator의 상위 또는 하위에 배치한 경우

그렇지 않은 경우에는 `dag=` 매개변수를 사용하여 각 Operator에 DAG를 전달해야 한다.

# Default Arguments
종종 많은 Operator는 DAG 내부에 `retries`와 같은 default argument를 필요로 한다. 이 경우 `default_args`를 사용하여 적용할 수 있다.
```
import pendulum

with DAG(
    dag_id="my_dag",
    start_date=pendulum.datetime(2016, 1, 1),
    schedule="@daily",
    default_args={"retries": 2},
):
    op = BashOperator(task_id="hello_world", bash_command="Hello World!")
    print(op.retries)  # 2
```

# Dag 데코레이터
기존의 `DAG()` 이외에도 `@dag` 데코레이터를 사용하여 DAG를 선언할 수 있다.
```
from datetime import datetime
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator

# 첫 번째 DAG 정의
@dag(start_date=datetime(2021, 1, 1), schedule_interval="@daily", catchup=False)
def first_dag():
    task1 = DummyOperator(task_id="task1")
    task2 = DummyOperator(task_id="task2")
    task1 >> task2

# 두 번째 DAG 정의
@dag(start_date=datetime(2022, 1, 1), schedule_interval="@weekly", catchup=False)
def second_dag():
    task3 = DummyOperator(task_id="task3")
    task4 = DummyOperator(task_id="task4")
    task3 >> task4

# 첫 번째 DAG 덮어쓰기
@dag(start_date=datetime(2023, 1, 1), schedule_interval="@monthly", catchup=False)
def first_dag():
    task5 = DummyOperator(task_id="task5")
    task6 = DummyOperator(task_id="task6")
    task5 >> task6

example_dag = first_dag()
```
데코레이터는 위와 같이 사용한다. `@dag`를 설정한 후에 사용할 함수를 지정한다.

이때 함수의 이름이 달라야 하며, 함수의 이름이 동일한 경우(맨 아래의 경우) 가장 마지막의 함수로 덮어쓰게 된다.

`@dag` 데코레이터를 사용하면 DAG를 깔끔하게 정의할 수 있을 뿐만 아니라, 함수의 매개변수를 DAG 매개변수로 설정하여 DAG를 트리거할 때 이러한 매개변수를 설정할 수 있다.
또한, 설정된 매개변수는 Python 코드나 Jinja 템플릿 내에서 접근할 수 있다.

Airflow는 `@dag` 데코레이터로 정의한 함수를 단순히 선언만 해서는 충분하지 않으며, `example_dag = first_dag()`와 같이 DAG 파일의 최상위 수준에서 호출되어야 한다.

# 흐름 제어
기본적으로 DAG는 task가 성공적으로 종료되는 경우에만 연이어(의존하여) 동작한다. 이를 수정하는 방식이 여러가지 존재한다.

- Branching - 특정 조건에 따라 어떤 작업으로 이동할지 선택
- Trigger Rules - DAG가 특정 작업을 실행할 조건을 설정. 작업 실행의 조건을 명시하여 특정 규칙에 따라 작업을 실행
- Setup and Teardown - DAG 내에서 설정 및 해제 관계를 정의. DAG 실행 전과 후에 특정 작업을 설정하거나 해제하는 관계를 정의
- Latest Only - 현재 시점에서 실행 중인 DAG에 대해 동작하는 특별한 형태의 분기. 최신 DAG에만 해당하는 작업을 실행
- Depends On Past - 작업이 이전 실행에서 자신에게 의존. 이전 실행에서의 작업 결과에 따라 현재 실행에서의 작업 동작이 변경

## Branching
의존성있는 모든 DAG를 실행하지 않고, 특정 DAG만 실행하고자 하는 경우에 사용한다. `@task.branch` 데코레이터로 사용할 수 있다.

`@task.branch`는 작업 ID(혹은 ID 목록)을 반환한다는 점을 제외하면 `@task`와 거의 유사하다. 특정 경로를 지나가면 나머지 경로는 생략된다.
downstream task를 생략하기 위해 `None`을 반환하기도 한다.

`@task.branch` 데코레이터로 데코레이트된 함수에서 반환된 작업 ID는 반드시 해당 함수가 데코레이트된 작업 이후에 직접적으로 위치한 작업을 가리켜야 한다.
```
@dag
def my_dag():
    @task
    def start():
        ...

    @task.branch
    def decide():
        # This function should return the task_id of a task downstream from "decide"
        # 이 함수는 "decide" 작업 이후에 위치한 작업의 task_id를 반환해야 합니다.
        if some_condition:
            return "some_task"
        else:
            return "another_task"

    @task
    def some_task():
        ...

    @task
    def another_task():
        ...

    start >> decide
    decide >> [some_task, another_task]
```
위의 경우 `decide` 함수가 `some_task` 또는 `another_task` 중 하나의 작업 ID를 직접 가리키고 있다.
### branch는 항상 task를 skip하는가?
```
                --------> branch_a --------
                |                         |
start -----> branch ---------------------------> join
                |
                --------> branch_b
```
branch_b로 분기하는 경우 일반적인 경우와 같이 다른 task는 skip한다.

하지만 join으로 분기하는 경우 join이 branch_a의 downstream task이기도 하므로 branch_a task를 skip하지 않고 동작시킨다.
### `@task.branch`, XComs
`@task.branch`가 XComs(교환 통신)와 함께 사용될 수 있으며, 이를 통해 상위 작업에서 생성된 컨텍스트를 활용하여 동적으로 분기를 결정하고 어떤 분기를 따를지 결정할 수 있다.

XComs는 작업 간에 데이터를 교환하는 데 사용되며, `@task.branch`를 사용하여 작업 간에 XComs를 전달하여 상위 작업의 결과를 기반으로 동적으로 DAG의 흐름을 제어할 수 있다.
```
@task.branch(task_id="branch_task")
def branch_func(ti=None):
    xcom_value = int(ti.xcom_pull(task_ids="start_task"))
    if xcom_value >= 5:
        return "continue_task"
    elif xcom_value >= 3:
        return "stop_task"
    else:
        return None


start_op = BashOperator(
    task_id="start_task",
    bash_command="echo 5",
    xcom_push=True,
    dag=dag,
)

branch_op = branch_func()

continue_op = EmptyOperator(task_id="continue_task", dag=dag)
stop_op = EmptyOperator(task_id="stop_task", dag=dag)

start_op >> branch_op >> [continue_op, stop_op]
```
`BashOperator`를 사용하여 bash_command를 통해 쉘 명령어를 실행하고, 실행 결과를 XCom으로 Push하도록 설정되어 있다.

Push한 XCom 값을 기반으로 `branch_func` 작업이 실행되며, 그 결과에 따라 `continue_task` 또는 `stop_task` 작업 중 하나가 동적으로 실행된다.
### BaseBranchOperator
사용자 정의 Operators에 분기 기능을 구현하고자 할 때, `BaseBranchOperator`를 상속할 수 있다.

`BaseBranchOperator`는 `@task.branch` 데코레이터와 유사한 동작을 가지지만, `choose_branch` 메서드의 구현을 제공해야 한다.

`@task.branch` 데코레이터를 사용하는 것이 `BranchPythonOperator`를 직접 인스턴스화하는 것보다 권장된다. 일반적으로 `BranchPythonOperator`를 직접 사용하는 것은 사용자 정의 Operator를 구현할 때만 권장된다.

`BaseBranchOperator`는 `@task.branch` 데코레이터의 callable과 유사하게 동작하며, downstream task의 ID나 ID 목록을 반환한다. downstream task를 skip 하기 위해서는 `None`을 반환하기도 한다.
```
class MyBranchOperator(BaseBranchOperator):
    def choose_branch(self, context):
        """
        Run an extra branch on the first day of the month
        """
        if context['data_interval_start'].day == 1:
            return ['daily_task_id', 'monthly_task_id']
        elif context['data_interval_start'].day == 2:
            return 'daily_task_id'
        else:
            return None
```
월의 첫날인 경우 `daily_task_id`와 `monthly_task_id` 두 개의 task를 실행하고, 2일인 경우 `daily_task_id` task를 실행한다.

이외의 경우 `None`을 반환하여 모든 task를 skip한다.
## Latest Only
Airflow의 DAG Run은 현재 날짜와 동일하지 않은 날짜에서 동작하기도 한다. 예를 들면 몇몇 데이터를 backfill하기 위해 지난달의 DAG 복사본을 동작하기도 한다.

그럼에도 이전 날짜에 대한 DAG Run을 전부 실행하지 않는 것을 원하는 경우가 있는데, 이때 `LatestOnlyOperator`를 실행한다.

이 특별한 Operator는 현재 "latest" DAG 실행이 아닌 경우 (현재 시간이 execution time과 다음 scheduled time 사이에 있고, 외부에서 트리거된 실행이 아닌 경우) 자체적으로 downstream task를 모두 skip 한다.

```
import datetime

import pendulum

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="latest_only_with_trigger",
    schedule=datetime.timedelta(hours=4),
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example3"],
) as dag:
    latest_only = LatestOnlyOperator(task_id="latest_only")
    task1 = EmptyOperator(task_id="task1")
    task2 = EmptyOperator(task_id="task2")
    task3 = EmptyOperator(task_id="task3")
    task4 = EmptyOperator(task_id="task4", trigger_rule=TriggerRule.ALL_DONE)

    latest_only >> task1 >> [task3, task4]
    task2 >> [task3, task4]
```
<img src="https://github.com/skybluelee/Archeive/assets/107929903/8d8c7bda-0e0d-4ce8-b498-de9e80952888.png" width="1000" height="400"/>

- `task1`은 `latest_only`의 downstream이므로 최신(latest) 실행인 경우를 제외하면 전부 skip된다.
- `task2`는 `latest_only`와 독립적이므로, 항상 실행된다.
- `task3`는 `task1`과 `task2`의 downstream인데, _success_ 해야만 트리거되는 규칙에 의해 `task1`에서의 downstream에서는 연쇄적으로 skip(cascaded skip)된다.
- `task4`는 `task1`과 `task2`의 downstream인데, trigger_rule이 `TriggerRule.ALL_DONE`으로 설정되어 있으므로, skip되지 않는다.

## Depends On Past
이전 DAG Run에서 성공적으로 완료된 경우에만 task를 실행되도록 설정할 수 있다. 이를 위해서는 해당 작업의 `depends_on_past` 매개변수를 True로 설정해야 한다.

주의해야 할 점은 DAG가 처음으로 자동으로 실행될 때, 즉 첫 번째 실행 시점에서는 이전 실행이 없으므로 해당 작업은 항상 실행된다는 것이다.

## Trigger Rules
기본적으로 Airflow는 upstream task가 성공적으로 종료될 때까지 대기한다.

하지만 이건 디폴트 값일 뿐, `trigger_rule` 인자를 task에 지정하여, 이를 제어할 수 있다. `trigger_rule` 목록은 아래와 같다.

- `all_success` (기본값): 모든 상위 작업이 성공한 경우에만 실행.
- `all_failed`: 모든 상위 작업이 실패하거나 upstream_failed 상태인 경우에 실행.
- `all_done`: 모든 상위 작업이 실행을 완료한 경우에 실행.
- `all_skipped`: 모든 상위 작업이 건너뛰어진 경우에 실행.
- `one_failed`: 적어도 하나의 상위 작업이 실패한 경우에 실행 (다른 상위 작업이 완료되지 않아도 됨).
- `one_success`: 적어도 하나의 상위 작업이 성공한 경우에 실행 (다른 상위 작업이 완료되지 않아도 됨).
- `one_done`: 적어도 하나의 상위 작업이 성공하거나 실패한 경우에 실행.
- `none_failed`: 모든 상위 작업이 실패하지 않았거나 upstream_failed 상태가 아닌 경우에 실행.
- `none_failed_min_one_success`: 모든 상위 작업이 실패하지 않았거나 upstream_failed 상태가 아니며, 적어도 하나의 상위 작업이 성공한 경우에 실행.
- `none_skipped`: 모든 상위 작업이 건너뛰어지지 않은 경우 (성공, 실패, 또는 upstream_failed 상태)에 실행.
- `always`: 어떤 종속성도 없으며, 언제든 실행할 수 있음.

원한다면 Trigger Rules와 Depends on Past 기능을 혼합하여 사용할 수 있다.

### Trigger Rules와 분기 작업
Trigger Rules와 skip된 task간의 상호작용, 특히 분기 작업(branching operation)에 의해 skip되는 경우에 대해 반드시 알아야 하는 점이 있다. 분기 작업에서는 `all_success`나 `all_failed`를 거의 사용하지 않을 것이다.

skip된 task는 `all_success`나 `all_failed` trigger rule에 의해 연속적으로 skip하게 된다.
```
# dags/branch_without_trigger.py
import pendulum

from airflow.decorators import task
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

dag = DAG(
    dag_id="branch_without_trigger",
    schedule="@once",
    start_date=pendulum.datetime(2019, 2, 28, tz="UTC"),
)

run_this_first = EmptyOperator(task_id="run_this_first", dag=dag)


@task.branch(task_id="branching")
def do_branching():
    return "branch_a"


branching = do_branching()

branch_a = EmptyOperator(task_id="branch_a", dag=dag)
follow_branch_a = EmptyOperator(task_id="follow_branch_a", dag=dag)

branch_false = EmptyOperator(task_id="branch_false", dag=dag)

join = EmptyOperator(task_id="join", dag=dag)

run_this_first >> branching
branching >> branch_a >> follow_branch_a >> join
branching >> branch_false >> join
```
<img src="https://github.com/skybluelee/Archeive/assets/107929903/a7d00ff3-fda8-469e-b255-1aa14b6fec4f.png" width="1000" height="200"/>

`join`은 `follow_branch_a`와 `branch_false`의 downstream이다. `join` task는 `trigger_rule`이 기본값인 `all_success`으로 설정되어 있으므로
분기 작업에 의해 발생한 fail에 의해 skip될 것이다.

<img src="https://github.com/skybluelee/Archeive/assets/107929903/13428b5a-5615-46d1-bb73-4138bd1391de.png" width="1000" height="200"/>

`join` task의 `trigger_rule`을 `none_failed_min_one_success`로 설정하여, 기존에 원하던 결과를 얻을 수 있다.

# 설정 및 해제
데이터 워크플로우에서 자원을 생성한 다음 일부 작업을 수행하고 나서 해당 자원을 제거하는 것이 일반적이며, Airflow에서는 이를 지원한다.

해당 정보는 [Setup and Teardown](https://airflow.apache.org/docs/apache-airflow/stable/howto/setup-and-teardown.html)에서 확인할 수 있다.

# Dynamic DAGs
DAG는 파이썬 코드로 정의되기 때문에, 완전 선언식(declarative)일 필요는 없다. 루프, 함수를 비롯한 여러가지를 사용할 수 있다.
```
 with DAG("loop_example", ...):

     first = EmptyOperator(task_id="first")
     last = EmptyOperator(task_id="last")

     options = ["branch_a", "branch_b", "branch_c", "branch_d"]
     for option in options:
         t = EmptyOperator(task_id=option)
         first >> t >> last
```
일반적으로, DAG의 구조나 레이아웃을 상대적으로 일정하게 유지하는 것이 좋다. 동적인 DAG는 주로 구성 옵션을 동적으로 로딩하거나 연산자 옵션을 변경하는 데 사용되는 것이 더 나은 경우가 많다.

# DAG 시각화
DAG 시각화를 원한다면 2가지 선택지가 있다.
- Airflow UI를 로드하고, DAG를 선택하고, "Graph"를 선택하기.
- `airflow dags show`를 실행하고, 이미지 파일로 렌더링하기.

Airflow에서는 일반적으로 Graph 사용을 추천하는데, 그래프가 사용자가 선택한 DAG Run 내의 모든 task 객체의 상태를 보여주기 때문이다.

물론, DAG를 개발 할 수록 매우 복잡해지므로, DAG 시각화를 수정하여 더 쉽게 이해할 수 있도록하는 몇가지 방법을 제공한다.

## TaskGroups