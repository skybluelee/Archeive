# DAG
해당 문서는 [airflow.models.dag](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/dag/index.html#module-contents)의 일부를 해석한 내용이다.

# airflow.models.dag.DAG
> `classairflow.models.dag.DAG(dag_id, description=None, schedule=NOTSET, start_date=None, end_date=None, full_filepath=None, template_searchpath=None, template_undefined=jinja2.StrictUndefined, user_defined_macros=None, user_defined_filters=None, default_args=None, concurrency=None, max_active_tasks=airflow_conf.getint('core', 'max_active_tasks_per_dag'), max_active_runs=airflow_conf.getint('core', 'max_active_runs_per_dag'), dagrun_timeout=None, sla_miss_callback=None, default_view=airflow_conf.get_mandatory_value('webserver', 'dag_default_view').lower(), orientation=airflow_conf.get_mandatory_value('webserver', 'dag_orientation'), catchup=airflow_conf.getboolean('scheduler', 'catchup_by_default'), on_success_callback=None, on_failure_callback=None, doc_md=None, params=None, access_control=None, is_paused_upon_creation=None, jinja_environment_kwargs=None, render_template_as_native_obj=False, tags=None, owner_links=None, auto_register=True, fail_stop=False, schedule_interval=NOTSET, timetable=None) [source](https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/models/dag.html#DAG)`

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
- 


template_searchpath (str | Iterable[str] | None) – This list of folders (non-relative) defines where jinja will look for your templates. Order matters. Note that jinja/airflow includes the path of your DAG file by default

template_undefined (type[jinja2.StrictUndefined]) – Template undefined type.

user_defined_macros (dict | None) – a dictionary of macros that will be exposed in your jinja templates. For example, passing dict(foo='bar') to this argument allows you to {{ foo }} in all jinja templates related to this DAG. Note that you can pass any type of object here.

user_defined_filters (dict | None) – a dictionary of filters that will be exposed in your jinja templates. For example, passing dict(hello=lambda name: 'Hello %s' % name) to this argument allows you to {{ 'world' | hello }} in all jinja templates related to this DAG.

default_args (dict | None) – A dictionary of default parameters to be used as constructor keyword parameters when initialising operators. Note that operators have the same hook, and precede those defined here, meaning that if your dict contains ‘depends_on_past’: True here and ‘depends_on_past’: False in the operator’s call default_args, the actual value will be False.

params (collections.abc.MutableMapping | None) – a dictionary of DAG level parameters that are made accessible in templates, namespaced under params. These params can be overridden at the task level.

max_active_tasks (int) – the number of task instances allowed to run concurrently

max_active_runs (int) – maximum number of active DAG runs, beyond this number of DAG runs in a running state, the scheduler won’t create new active DAG runs

dagrun_timeout (datetime.timedelta | None) – specify how long a DagRun should be up before timing out / failing, so that new DagRuns can be created.

sla_miss_callback (None | SLAMissCallback | list[SLAMissCallback]) – specify a function or list of functions to call when reporting SLA timeouts. See sla_miss_callback for more information about the function signature and parameters that are passed to the callback.

default_view (str) – Specify DAG default view (grid, graph, duration, gantt, landing_times), default grid

orientation (str) – Specify DAG orientation in graph view (LR, TB, RL, BT), default LR

catchup (bool) – Perform scheduler catchup (or only run latest)? Defaults to True

on_failure_callback (None | DagStateChangeCallback | list[DagStateChangeCallback]) – A function or list of functions to be called when a DagRun of this dag fails. A context dictionary is passed as a single parameter to this function.

on_success_callback (None | DagStateChangeCallback | list[DagStateChangeCallback]) – Much like the on_failure_callback except that it is executed when the dag succeeds.

access_control (dict | None) – Specify optional DAG-level actions, e.g., “{‘role1’: {‘can_read’}, ‘role2’: {‘can_read’, ‘can_edit’, ‘can_delete’}}”

is_paused_upon_creation (bool | None) – Specifies if the dag is paused when created for the first time. If the dag exists already, this flag will be ignored. If this optional parameter is not specified, the global config setting will be used.
