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
- tags (list[str] | None) – UI에서 DAG를 필터링하는데 도움을 주는 list이다.
***
- full_filepath (string) - DAG 파일의 전체 경로를 나타낸다.
- template_searchpath (str | Iterable[str] | None) – 이 폴더 목록(상대 경로가 아닌)은 jinja가 템플릿을 찾을 위치를 정의한다. 순서가 중요하며, jinja/airflow는 기본적으로 DAG 파일의 경로를 포함한다.
- template_undefined (type[jinja2.StrictUndefined]) – Airflow에서 사용되는 예외(exception) 클래스로, Jinja 템플릿에서 정의되지 않은 변수나 매크로를 참조하려고 시도할 때 발생한다.
- user_defined_macros (dict | None) – 이 jinja 템플릿에서 사용할 매크로들의 dictionary이다. 예를 들어, 이 인자에 `dict(foo='bar')`를 전달하면 이 DAG와 관련된 모든 jinja 템플릿에서 `{{ foo }}`를 사용할 수 있다. 여기서 어떤 종류의 객체도 전달할 수 있다.
- user_defined_filters (dict | None) – 이 인자는 jinja 템플릿에서 사용할 사용자 정의 필터들의 dictionary이다. 예를 들어, `dict(hello=lambda name: 'Hello %s' % name)`를 이 인자에 전달하면 이 DAG와 관련된 모든 jinja 템플릿에서 `{{ 'world' | hello }}`와 같이 필터를 사용할 수 있다.
- sla_miss_callback (None | SLAMissCallback | list[SLAMissCallback]) – sla_miss_callback은 SLA(서비스 수준 계약) 시간 초과를 보고할 때 호출할 함수나 함수들의 목록이다. 자세한 사항은 [sla_miss_callback](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#concepts-sla-miss-callback)을 참조하라.
- default_view (str) – DAG의 기본 뷰(그리드, 그래프, 길이, gantt(시간 경과에 따른 task 실행 상태 표현), landing_times(task가 언제 DAG에 도착했는지 표현))를 설정한다.
- orientation (str) – DAG 그래프 뷰에서 그래프 방향(LR, TB, RL, BT)을 지정한다. 디폴트 값은 LR(왼쪽에서 오른쪽으로)이다.
- doc_md (str) - DAG 객체의 속성 중 하나로, DAG에 대한 문서나 설명을 Markdown 형식으로 제공하는 문자열이다.
- access_control (rbac | superuser_role | viewer_role | user_role | public_role) - Airflow 웹 서버의 보안 및 접근 제어 설정을 관리한다. 이 설정을 통해 특정 사용자나 그룹에 대한 웹 UI, API, CLI 등의 접근 권한을 정의하고 제어할 수 있다.
- is_paused_upon_creation (bool | None) – DAG가 처음 생성될 때 일시 중지 상태(paused)로 설정할 것인지 지정한다. DAG가 이미 존재하는 경우 이 플래그는 무시된다. 이 선택적 매개변수가 지정되지 않으면, 전역 설정 설정이 사용된다.
- jinja_environment_kwargs (dict | None) – 템플릿 렌더링을 위해 Jinja 환경에 전달되는 추가적인 설정 옵션들을 나타낸다.
- params (collections.abc.MutableMapping | None) – 템플릿에서 접근할 수 있는 DAG 수준의 매개변수들을 params 네임스페이스 아래에 정의된 dictionary 형태로 제공한다. 매개변수들은 task 수준에서 재정의(override)될 수 있다.
- owner_links (dict[str, str] | None) – DAG 뷰 UI에서 클릭 가능한 링크로 표시될 소유자(owner) 및 해당 링크들의 dictionary이다. 이 링크들은 HTTP 링크(예: Slack 채널로의 링크) 또는 mailto 링크와 같은 형태로 사용될 수 있다. 예시로는 `{"dag_owner": "https://airflow.apache.org/"}`와 같은 형식이 있다.
- auto_register (bool) – DAG가 특정 디렉토리에서 사용되는 경우 Airflow가 자동으로 DAG를 등록한다.
- fail_stop (bool) – DAG 내의 특정 task가 실패할 때 현재 실행 중인 task도 중단된다. 주의: 중단(stop) 타입의 DAG는 "all_success"와 같은 기본 트리거 규칙을 가진 task만 포함할 수 있다. 중단 타입의 DAG에 기본 트리거 규칙이 아닌 다른 규칙을 가진 task가 있다면 예외가 발생한다.
- render_template_as_native_obj (bool) – 만약 True인 경우, 템플릿을 원래의 Python 타입으로 렌더링하기 위해 Jinja NativeEnvironment를 사용한다. 만약 False인 경우, 템플릿을 문자열 값으로 렌더링하기 위해 Jinja Environment가 사용된다.

## start_date, end_date
시간을 지정할 때는 반드시 `pendulum`을 사용해야 한다. `datetime.timezone` 라이브러리는 한계점이 존재하여 Airflow에서 사용하지 못하도록 설정하였다.
```
import pendulum

from airflow.models.dag import DAG
from airflow.example_dags.plugins.workday import AfterWorkdayTimetable


with DAG(
    dag_id="example_after_workday_timetable_dag",
    start_date=pendulum.datetime(2021, 3, 10, tz="UTC"),
    schedule=AfterWorkdayTimetable(),
    tags=["example", "timetable"],
):
    ...
```
대한민국과 UTC차이는 9시간으로 `pendulum` 없이 사용하고자 하면 UTC + 9시간으로 설정하면 된다.

## 

## default_args
```
default_args={"owner": "airflow", "retries": 3, "start_date": datetime.datetime(2022, 1, 1)}

start_date=datetime.datetime(2022, 1, 1),
owner="airflow",
retries=3
```
위는 딕셔너리 방식(default_args 사용)이고, 아래는 키워드 인자 방식으로 둘의 효과는 동일하다.

동일한 효과인데 default_args를 사용하는 이유는 아래와 같다.
- 일관된 설정 관리: 여러 task에서 동일한 설정 값을 반복적으로 정의하는 것을 피하기 위해 default_args를 사용하여 일관된 기본 설정을 한 번에 정의할 수 있다.
- 중앙 집중적인 설정: DAG의 여러 task가 같은 소유자, 재시도 횟수, 이메일 알림 등의 설정을 공유할 때, 중앙에서 한 곳에서 이러한 설정을 관리할 수 있다.
- 유지 관리 용이성: default_args를 사용하면 한 곳에서 DAG의 기본 설정을 쉽게 수정하거나 업데이트할 수 있다. 이를 통해 코드의 중복성을 줄이고 유지 관리를 간소화할 수 있다.
- 문서화: default_args를 사용하여 각 DAG의 기본 설정을 명시적으로 정의하면, 다른 개발자나 팀원들이 DAG의 동작 및 설정에 대해 더 쉽게 이해하고 문서화할 수 있다.
- 재사용성: 동일한 기본 설정을 가진 여러 DAG나 task가 있을 경우, default_args를 사용하여 해당 설정을 재사용하고 다른 DAG나 task에서 쉽게 적용할 수 있다.
- 오류 방지: default_args를 사용하여 기본적인 설정 값을 제공함으로써, task나 DAG를 정의할 때 필수적인 설정을 누락하는 경우의 오류를 방지할 수 있다.
