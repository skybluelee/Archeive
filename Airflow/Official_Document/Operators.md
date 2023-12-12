**본 문서는 Airflow 공식 문서 [Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)를 참조함**
# Operators
operator는 개념적으로 미리 정의된 task을 위한 템플릿으로, DAG 내에서 선언적으로 정의할 수 있다.
```
with DAG("my-dag") as dag:
    ping = SimpleHttpOperator(endpoint="http://example.com/update/")
    email = EmailOperator(to="admin@example.com", subject="Update complete")

    ping >> email
```
Airflow는 매우 다양한 operator가 있으며, 몇몇은 코어에 내장되어 있거나 사전 설치된 프로바이더에 포함되어 있다.
주요 operator에서 인기 있는 operator는 다음과 같다.
- **BashOperator**: bash 명령을 실행한다.
- **PythonOperator**: 임의의 Python 함수를 호출한다.
- **EmailOperator**: 이메일을 전송한다.
- `@task` 데코레이터를 사용하여 임의의 Python 함수를 실행할 수 있다. 하지만 이는 전달된 인수로 jinja 템플릿을 렌더링하는 것을 지원하지 않는다.

모든 주요 operator는 다음을 참고하라. [Core Operators and Hooks Reference.](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)

사용하고자 하는 operator에 Airflow에 기본적으로 설치되어 있지 않은 경우, [provider packages](https://airflow.apache.org/docs/apache-airflow-providers/index.html)에서 확인할 수 있다.
여기에는 몇가지 아래의 인기 있는 operator가 포함되어 있다.
- SimpleHttpOperator
- MySqlOperator
- PostgresOperator
- MsSqlOperator
- OracleOperator
- JdbcOperator
- DockerOperator
- HiveOperator
- S3FileTransformOperator
- PrestoToMySqlOperator
- SlackAPIOperator

이 외에도 provider packages에서 다양한 operator, hook, sensor, transfer가 존재한다.

Airflow 코드에는 task와 operator가 대부분 교환가능하기에 개념을 섞어 놓은 경우가 종종 있다.
하지만 task는 DAG의 "실행 단위"의 통칭이고, operator는 재사용 가능하고 사용자를 위해 이미 만들어져 있고 몇가지 인자만 주어지면 사용 가능한 task 템플릿을 의미한다.
# Jinja 템플릿
Airflow은 Jinja 템플릿을 활용하며, 이는 [매크로](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#templates-ref)와 조합하여 사용할 때 강력한 도구가 될 수 있다.

예를 들어, `BashOperator`를 사용하여 Bash 스크립트에 데이터 간격의 시작을 환경 변수로 전달하고 싶은 경우가 있다면 아래와 같이 사용할 수 있다.
```
# The start of the data interval as YYYY-MM-DD
date = "{{ ds }}"
t = BashOperator(
    task_id="test_env",
    bash_command="/tmp/test.sh ",
    dag=dag,
    env={"DATA_INTERVAL_START": date},
)
```
여기서 `{{ ds }}`는 템플릿화된 변수이며, `BashOperator`의 `env` 매개변수가 Jinja로 템플릿화되어 있기 때문에 데이터 간격의 시작 날짜는 Bash 스크립트에서 `DATA_INTERVAL_START`라는 이름의 환경 변수로 사용할 수 있다.

문서에서 "템플릿화된"으로 표시된 파라미터는 모두 Jinja 템플릿을 사용할 수 있다. 템플릿 치환은 연산자의 `pre_execute` 함수가 호출되기 직전에 발생한다.
***
```
class MyDataReader:
    template_fields: Sequence[str] = ("path",)

    def __init__(self, my_path):
        self.path = my_path

    # [additional code here...]


t = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    op_args=[MyDataReader("/tmp/{{ ds }}/my_file")],
    dag=dag,
)
```
Jinja 템플릿을 중첩된 필드에서도 사용할 수 있다. 중요한 점은 이러한 중첩된(nested) 필드가 속한 구조에서 해당 중첩된 필드가 템플릿화되어 있어야 한다. 
위의 예제에서와 같이 `template_fields` 속성에 등록된 필드(위 예제의 `path` 필드)는 템플릿 치환에 제출된다.

`template_fields` 속성은 클래스 변수이며 반드시 `Sequence[str]` 유형 (즉, 문자열의 리스트 또는 튜플)임이 보장된다.
***
```
class MyDataTransformer:
    template_fields: Sequence[str] = ("reader",)

    def __init__(self, my_reader):
        self.reader = my_reader

    # [additional code here...]


class MyDataReader:
    template_fields: Sequence[str] = ("path",)

    def __init__(self, my_path):
        self.path = my_path

    # [additional code here...]


t = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    op_args=[MyDataTransformer(MyDataReader("/tmp/{{ ds }}/my_file"))],
    dag=dag,
)
```
모든 중간 필드가 템플릿 필드로 표시되어 있다면 깊게 중첩된 필드도 치환될 수 있다.
***
```
my_dag = DAG(
    dag_id="my-dag",
    jinja_environment_kwargs={
        "keep_trailing_newline": True,
        # some other jinja2 Environment options here
    },
)
```
Jinja `Environment`를 DAG를 만들 때 사용자 정의 옵션에 전달할 수 있다. 한 가지 흔한 사용 예는 Jinja가 템플릿 문자열에서 후행 개행 문자(trailing newline)를 삭제하는 것을 방지하는 것이다.

[Jinja documentation](https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.Environment)에서 여러 이용 가능한 옵션을 찾을 수 있다.
***
몇몇 operator는 `template_ext`에서 정의된 특정 접미사로 끝나는 문자열을 필드 렌더링 시 파일 참조로 간주한다.
이를 통해 DAG 코드에 직접 포함시키지 않고 파일에서 스크립트 또는 쿼리를 직접로드하는 데 유용할 수 있다.
```
run_script = BashOperator(
    task_id="run_script",
    bash_callable="script.sh",
)
```
예를 들어 `script.sh` 파일을 로드하고 해당 내용을 `bash_callable`의 값으로 사용하기 위해, 여러 줄의 bash 스크립트를 실행하는 BashOperator를 생각해보라.

기본적으로 이 방식으로 제공되는 경로는 DAG의 폴더를 기준으로 상대적으로 제공되어야 한다(이는 기본 Jinja 템플릿 검색 경로이므로). 
그러나 `template_searchpath` 인자를 DAG에 설정함으로써 추가적인 경로를 추가할 수 있다.
***
```
print_script = BashOperator(
    task_id="print_script",
    bash_callable="cat script.sh",
)
```
특정 필드에서 템플릿 렌더링을 비활성화하거나 특정 접미사에 대해 템플릿 파일을 읽지 않도록 하려는 경우가 있을 수 있다. 이 경우 위과 같은 작업을 고려하라.
***
```
fixed_print_script = BashOperator(
    task_id="fixed_print_script",
    bash_callable="cat script.sh",
)
fixed_print_script.template_ext = ()
```
이 작업은 `TemplateNotFound: cat script.sh`와 같은 오류를 발생시킬 것이지만, `template_ext`를 오버라이드하여 Airflow가 이 값을 파일 참조로 취급하지 않도록 할 수 있다.
## 필드를 Native Python Object로 렌더링하기
기본적으로 모든 `template_fields`는 문자열로 렌더링된다.
```
transform = PythonOperator(
    task_id="transform",
    op_kwargs={"order_data": "{{ti.xcom_pull('extract')}}"},
    python_callable=transform,
)
```
예를 들어, `extract` 작업이 딕셔너리({"1001": 301.27, "1002": 433.21, "1003": 502.22})를 `XCom` 테이블에 푸시한다고 가정해 보자.
이제 다음 task를 실행할 때 order_data 인자는 문자열('{"1001": 301.27, "1002": 433.21, "1003": 502.22}')로 전달된다.
***
```
dag = DAG(
    dag_id="example_template_as_python_object",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    render_template_as_native_obj=True,
)


@task(task_id="extract")
def extract():
    data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
    return json.loads(data_string)


@task(task_id="transform")
def transform(order_data):
    print(type(order_data))
    for value in order_data.values():
        total_order_value += value
    return {"total_order_value": total_order_value}


extract_task = extract()

transform_task = PythonOperator(
    task_id="transform",
    op_kwargs={"order_data": "{{ti.xcom_pull('extract')}}"},
    python_callable=transform,
)

extract_task >> transform_task
```
만약 렌더링된 템플릿 필드가 기존 파이썬 객체로(위의 예시에서 딕셔너리 형태로) 전송하고자 하면, `render_emplate_as_native_obj=True`를 사용하여 전달할 수 있다.

이 경우 `order_data` 인자는 `{"1001": 301.27, "1002": 433.21, "1003": 502.22}` 형태로 전달된다.

Airflow는 `render_template_as_native_obj`가 `True`로 설정되어 있을 때 Jinja의 [`NativeEnvironment`](https://jinja.palletsprojects.com/en/2.11.x/nativetypes/)를 사용한다.
`NativeEnvironment`를 사용하여 렌더링된 템플릿은 고유 파이썬 형태를 유지한다.

# 파라미터 키워드 예약
Airflow 2.2.0 버전부터 `params` 변수는 DAG 직렬화에서 사용된다.
서드 파티 operator에서는 사용할 수 없다.

만약 사용자가 환경을 업데이트한 결과 아래와 같은 오류가 발생한다면,
```
AttributeError: 'str' object has no attribute '__module__'
```
operator에서 `params`의 이름을 다른 이름으로 변경하라.
