# DAG
해당 문서는 [airflow.models.dag](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#module-contents)의 일부를 해석한 내용이다.

# airflow.models.dag.DAG
```
classairflow.models.dag.DAG(dag_id, description=None, schedule=NOTSET, start_date=None, end_date=None,
                            default_args=None,
# 공식문서에는 없으나         retries=None, retry_exponential_backoff=None, retry_delay=None
# 자주 사용                  max_retry_delay=None, on_failure_callback=None, on_retry_callback=None,
                            on_success_callback=None, trigger_rule=None
                            max_active_tasks=airflow_conf.getint('core', 'max_active_tasks_per_dag'),
                            max_active_runs=airflow_conf.getint('core', 'max_active_runs_per_dag'),
                            catchup=airflow_conf.getboolean('scheduler', 'catchup_by_default'),
                            concurrency=None, dagrun_timeout=None, tags=None,

                            full_filepath=None, template_searchpath=None, template_undefined=jinja2.StrictUndefined,
                            user_defined_macros=None, user_defined_filters=None, sla_miss_callback=None, 
                            default_view=airflow_conf.get_mandatory_value('webserver', 'dag_default_view').lower(),
                            orientation=airflow_conf.get_mandatory_value('webserver', 'dag_orientation'), doc_md=None,
                            access_control=None, is_paused_upon_creation=None, jinja_environment_kwargs=None,  params=None,
                            owner_links=None, auto_register=True, fail_stop=False, render_template_as_native_obj=False) 
```
[source](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/models/dag.html#DAG)

공식문서에는 없는 몇가지 파라미터를 추가하였다. DAG보다는 Operator에 사용하나, DAG 내부에서도 정의가 가능하기에 추가하였다.

시간을 지정할 때는 반드시 `pendulum`을 사용해야 한다. `datetime.timezone` 라이브러리는 한계점이 존재하여 Airflow에서 사용하지 못하도록 설정하였다.

2.4 버전부터 시간 기반의 스케쥴링 로직 또는 데이터셋 기반의 트리거를 인자로 지정할 수 있게 되었다.

2.4 버전부터 schedule_interval과 timetable은 schedule의 인자로 병합되었다.

> Parametes

- dag_id (str) – DAG의 id이다. 알베벳, 숫자, 대시(-), 점(.), 언더바(_)(모든 ASCII 문자)를 사용할 수 있다.
- description (str | None) - DAG에 대한 설명으로 웹 상에서 확인할 수 있다.
- schedule (ScheduleArg) - DAG Run이 스케쥴되는 규칙을 정의한다. 크론 탭, timedelta 객체, Timetable, Dataset 객체의 list를 사용할 수 있다.
만약 schedule이 정의되지 않으면, DAG는 기본적으로 `timedelta(days=1)`으로 설정된다. [Customizing DAG Scheduling with Timetables](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html)도 확인하라.
- start_date (datetime.datetime | None) - scheduler가 backfill을 시도할 시간을 말한다. 해당 시간을 시작으로 schedule에 해당하는 모든 task가 실행된다.
- end_date (datetime.datetime | None) - DAG가 실행 종료되는 시간이다. 계속해서 scheduling되기 원하면 None으로 설정하거나, end_date를 사용하지 않으면 된다.
- default_args (dict | None) - operator를 초기화할 때 사용되는 키워드 파라미터 생성자이다.
default_args에서 정의된 것이 먼저 사용되고, 이후에 operator의 파라미터를 사용한다. 즉 만약 default_args에서 `True`로 설정하고, operator에서 `False`로 설정하면, 실제로는 `False`로 동작한다.
- retries (int) - task가 fail되는 경우 재시도하는 횟수를 지정한다.
- retry_exponential_backoff (bool) - exponential backoff(실패시 대기 시간을 점진적으로 증가시키는 방법)사용 여부를 지정한다.
- retry_delay (datetime.timedelta) – task가 fail되고 재시도 되기까지의 시간을 지정한다. `retry_delay=datetime.timedelta(minutes=5)`라고 설정하면 task가 실패한 후 5분 후에 재시도된다.
- max_retry_delay (datetime.timedelta) – task 재시도의 최대 지연 시간을 지정한다. `max_retry_delay=datetime.timedelta(hours=1)`로 설정하면, 재시도의 각 지연 시간은 최대 1시간을 초과할 수 없다.
- on_failure_callback (None | DagStateChangeCallback | list[DagStateChangeCallback]) – task가 fail되면 해당 함수가 호출된다. 플러그인을 지정하고 해당 플러그인으로 실패했다는 메시지를 전송한다.
- on_retry_callback (None | DagStateChangeCallback | list[DagStateChangeCallback]) – on_failure_callback과 동일하게 동작하며, 재시도시 재시도한다는 메시지를 전송한다.
- on_success_callback (None | DagStateChangeCallback | list[DagStateChangeCallback]) – on_failure_callback과 동일하게 동작하며, 성공시 성공했다는 메시지를 전송한다.
- trigger_rule (str) – 어떤 의존성을 task에 적용할 지를 정의한다. 옵션은 다음과 같다. { all_success | all_failed | all_done | one_success | one_failed | none_failed | none_failed_or_skipped | none_skipped | dummy}
디폴트값은 all_success이다. 옵션은 string 혹은 static class airflow.utils.TriggerRule로 정의된 상수를 사용하여 설정한다.
- max_active_tasks (int) – 동시에 실행 중인 특정 DAG 내의 task 인스턴스의 최대 수를 제한한다. max_active_task=10로 설정하면, 해당 DAG의 모든 task 인스턴스 중 동시에 활성화될 수 있는 최대 인스턴스 수가 10개로 제한된다.
- max_active_runs (int) – DAG Run이 실행중인 최대 개수를 설정한다. 해당 개수를 넘어가면 스케쥴러는 DAG Run을 생성하지 않는다.
- catchup (bool) – True로 설정하면 start_date부터 현재까지 모든 DAG를 실행한다. False로 설정하면 가장 최신의 DAG만 실행한다.
- concurrency (int) - DAG에 의해 동시에 실행될 수 있는 특정 task 인스턴스의 최대 수를 지정한다. concurrency=5로 설정하면, 특정 task는 해당 DAG 내에서 최대 5개의 인스턴스만 동시에 실행될 수 있다.
- dagrun_timeout (datetime.timedelta | None) – DAG Run이 실행될 수 있는 최대 지속 시간을 설정한다. 이 시간을 넘어가면 해당 DAG는 자동으로 중지된다.


template_searchpath (str | Iterable[str] | None) – This list of folders (non-relative) defines where jinja will look for your templates. Order matters. Note that jinja/airflow includes the path of your DAG file by default

template_undefined (type[jinja2.StrictUndefined]) – Template undefined type.

user_defined_macros (dict | None) – a dictionary of macros that will be exposed in your jinja templates. For example, passing dict(foo='bar') to this argument allows you to {{ foo }} in all jinja templates related to this DAG. Note that you can pass any type of object here.

user_defined_filters (dict | None) – a dictionary of filters that will be exposed in your jinja templates. For example, passing dict(hello=lambda name: 'Hello %s' % name) to this argument allows you to {{ 'world' | hello }} in all jinja templates related to this DAG.


params (collections.abc.MutableMapping | None) – a dictionary of DAG level parameters that are made accessible in templates, namespaced under params. These params can be overridden at the task level.





dagrun_timeout (datetime.timedelta | None) – specify how long a DagRun should be up before timing out / failing, so that new DagRuns can be created.

sla_miss_callback (None | SLAMissCallback | list[SLAMissCallback]) – specify a function or list of functions to call when reporting SLA timeouts. See sla_miss_callback for more information about the function signature and parameters that are passed to the callback.

default_view (str) – Specify DAG default view (grid, graph, duration, gantt, landing_times), default grid

orientation (str) – Specify DAG orientation in graph view (LR, TB, RL, BT), default LR




tags (list[str] | None) – List of tags to help filtering DAGs in the UI.

owner_links (dict[str, str] | None) – Dict of owners and their links, that will be clickable on the DAGs view UI. Can be used as an HTTP link (for example the link to your Slack channel), or a mailto link. e.g: {“dag_owner”: “https://airflow.apache.org/”}

auto_register (bool) – Automatically register this DAG when it is used in a with block

fail_stop (bool) – Fails currently running tasks when task in DAG fails. Warning: A fail stop dag can only have tasks with the default trigger rule (“all_success”). An exception will be thrown if any task in a fail stop dag has a non default trigger rule.
access_control (dict | None) – Specify optional DAG-level actions, e.g., “{‘role1’: {‘can_read’}, ‘role2’: {‘can_read’, ‘can_edit’, ‘can_delete’}}”

is_paused_upon_creation (bool | None) – Specifies if the dag is paused when created for the first time. If the dag exists already, this flag will be ignored. If this optional parameter is not specified, the global config setting will be used.
## default_args
```
default_args={"owner": "airflow", "retries": 3, "start_date": datetime.datetime(2022, 1, 1)}

start_date=datetime.datetime(2022, 1, 1),
owner="airflow",
retries=3
```
위는 딕셔너리 방식(default_args 사용)이고, 아래는 키워드 인자 방식으로 둘의 효과는 동일하다.

동일한 효과인데 default_args를 사용하는 이유는 아래와 같다.
- 일관된 설정 관리: 여러 task에서 동일한 설정 값을 반복적으로 정의하는 것을 피하기 위해 default_args를 사용하여 일관된 기본 설정을 한 번에 정의할 수 있습니다.

- 중앙 집중적인 설정: DAG의 여러 task가 같은 소유자, 재시도 횟수, 이메일 알림 등의 설정을 공유할 때, 중앙에서 한 곳에서 이러한 설정을 관리할 수 있습니다.

- 유지 관리 용이성: default_args를 사용하면 한 곳에서 DAG의 기본 설정을 쉽게 수정하거나 업데이트할 수 있습니다. 이를 통해 코드의 중복성을 줄이고 유지 관리를 간소화할 수 있습니다.

- 문서화: default_args를 사용하여 각 DAG의 기본 설정을 명시적으로 정의하면, 다른 개발자나 팀원들이 DAG의 동작 및 설정에 대해 더 쉽게 이해하고 문서화할 수 있습니다.

- 재사용성: 동일한 기본 설정을 가진 여러 DAG나 task가 있을 경우, default_args를 사용하여 해당 설정을 재사용하고 다른 DAG나 task에서 쉽게 적용할 수 있습니다.

- 오류 방지: default_args를 사용하여 기본적인 설정 값을 제공함으로써, task나 DAG를 정의할 때 필수적인 설정을 누락하는 경우의 오류를 방지할 수 있습니다.



