해당 문서는 [PythonOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#),
[airflow.operators.python](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html),
[example_python_operator.py](https://github.com/apache/airflow/blob/providers-amazon/8.13.0/airflow/example_dags/example_python_operator.py),
[example_python_decorator.py](https://github.com/apache/airflow/blob/providers-amazon/8.13.0/airflow/example_dags/example_python_decorator.py)를 참조하였다.
# PythonOperator
`class airflow.operators.python.PythonOperator(*, python_callable, op_args=None, op_kwargs=None, templates_dict=None, templates_exts=None, show_return_value_in_logs=True, **kwargs)`

Airflow에서 callable을 실행할 때, Airflow는 함수 내에서 사용할 수 있는 키워드 인자들의 집합을 전달한다.
이 키워드 인자들의 집합은 정확하게 Jinja 템플릿에서 사용할 수 있는 것들과 동일하다.
이 기능을 활용하려면 함수의 헤더에 `**kwargs`를 정의하거나 직접 가져오고자 하는 키워드 인자들을 추가할 수 있다. 예를 들어, 아래의 코드로는 callable에서 `ti`와 `next_ds` 컨텍스트 변수의 값을 가져올 수 있다.
```
def my_python_callable(ti, next_ds):
    pass
```
```
def my_python_callable(**kwargs):
    ti = kwargs["ti"]
    next_ds = kwargs["next_ds"]
```

## Parameter
- python_callable (Callable) – 호출 가능한 객체에 대한 참조, 즉 실행 가능한 함수나 메서드를 가리킨다.
- op_kwargs (Mapping[str, Any] | None) – 함수 내에서 사용할 키워드 인자들의 dictionary로 함수에서 언패킹되어 사용된다.
- op_args (Collection[Any] | None) – 함수 내에서 사용할 위치 인자들의 목록으로 함수 호출 시 언패킹되어 함수에 전달된다.
- templates_dict (dict[str, Any] | None) – 값이 템플릿화될 dictionary이다. Airflow 엔진은 `__init__`와 `execute` 사이에 이 값을 템플릿화한다. 템플릿이 적용된 후에는 해당 값들이 callable의 컨텍스트에서 사용 가능하다.
- templates_exts (Sequence[str] | None) – 템플릿 필드를 처리하는 동안 해결할 파일 확장자들의 목록이다. 예를 들면 `['.sql', '.hql']`와 같은 형태로 사용된다.
- show_return_value_in_logs (bool) – 반환 값 로그를 표시할지 여부를 나타내는 boolean 값이다. 기본값은 True로, 반환 값 로그 출력을 허용한다. 큰 데이터(예: 대량의 XCom을 TaskAPI에 전송하는 경우)를 반환할 때 로그 출력을 방지하려면 False로 설정하면 된다.
- execution_timeout (timedelta) - 함수 최대 실행 시간을 지정한다. 해당 시간을 초과하면 task는 fail된다. `execution_timeout=timedelta(seconds=600)`로 설정하면 함수가 10분내에 성공하지 못할시 재시도한다.


## example
```
from airflow.models.dag import DAG
from airflow.operators.python import (
#   ExternalPythonOperator,
    PythonOperator,
#   PythonVirtualenvOperator,
#   is_venv_installed,
)

with DAG(
    dag_id="example_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
):
    # 첫번째 파이썬 함수
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs) # **kwargs는 이 임의의 키워드 인자를 받아들이는 dictionary로,
                       # 만약 인자를 제공하지 않으면, kwargs 사전은 빈 사전(empty dictionary)으로 채워져 아무것도 출력되지 않음
        print(ds)      # ds는 인자로 직접 받음
        return "Whatever you return gets printed in the logs"

                              # task_id는 웹 UI에서 확인
    run_this = PythonOperator(task_id="print_the_context", python_callable=print_context)
                                                           # python_callable에 파이썬 함수의 이름을 인자로 전달
    # 두번째 파이썬 함수
    def log_sql(**kwargs):
                                                            # kwargs중 templates_dict dictionary의 값을 사용
        logging.info("Python task decorator query: %s", str(kwargs["templates_dict"]["query"]))

    log_the_sql = PythonOperator(
        task_id="log_sql_query",
        python_callable=log_sql,
        templates_dict={
                            "query": "sql/sample.sql" # templates_dict dictionary에 query, txt 파일을 지정함
                            "txt_data": ".txt"
                       },
        templates_exts=[".sql", ".txt"], # 파일의 확장자 지정
    )

    # 세번째 파이썬 함수
    def my_sleeping_function(random_base):
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

    # PythonOperator에서 for문 사용 가능
    for i in range(5):
        sleeping_task = PythonOperator(
            task_id=f"sleep_for_{i}", python_callable=my_sleeping_function, op_kwargs={"random_base": i / 10}
        )

        run_this >> log_the_sql >> sleeping_task
```
```
dag = DAG(
    dag_id = 'Comment_Extract_0',
    start_date = datetime(2023,5,10),
    end_date = datetime(2023, 5, 24, 12, 0),
    schedule = '0/10 * * * *',
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    }
)

def etl(**context):
    sql_num = context["params"]["sql_num"]
    remote_webdriver = 'remote_chromedriver0'
    with webdriver.Remote(f'{remote_webdriver}:4444/wd/hub', options=options) as driver:
        # Scraping part
        driver.get(context["params"]["link"])
        title, input_time = crawling_functions.main(driver, 0)
        timestamp = crawling_functions.comments_analysis(driver, title, sql_num)

        while(1):
            try:
                crawling_functions.more_comments(driver)
            except:
                break
        crawling_functions.comments(driver, title, timestamp, sql_num, input_time)

etl = PythonOperator(
    task_id = 'etl',
    python_callable = etl,
    execution_timeout=timedelta(seconds=600), # 10분내에 성공하지 못하면 retry
    # kwargs에 파일을 지정할 수도 있고, 아래와 같이 값을 지정할 수도 있음
    params = {
        "link": "https://n.news.naver.com/article/082/0001213904?ntype=RANKING",
        "sql_num" : "_0"
    },
    dag = dag
)

etl
```
# task
`airflow.operators.python.task(python_callable=None, multiple_outputs=None, **kwargs)`

`airflow.decorators.task()`는 deprecated되었으므로 `python.task`를 사용하라.

`@task.python`를 호출하고 Python 함수를 Airflow task로 변환하게 해준다.

## Parameter
- python_callable (Callable) – 호출 가능한 객체에 대한 참조, 즉 실행 가능한 함수나 메서드를 가리킨다.
- op_kwargs (Mapping[str, Any] | None) – 함수 내에서 사용할 키워드 인자들의 dictionary로 함수에서 언패킹되어 사용된다.
- op_args (Collection[Any] | None) – 함수 내에서 사용할 위치 인자들의 목록으로 함수 호출 시 언패킹되어 함수에 전달된다.
- multiple_outputs (bool | None) – 설정된 경우, 함수의 반환 값은 여러 개의 XCom 값으로 언패킹(unrolled)된다. dictionary는 키를 키로 사용하여 XCom 값으로 언패킹된다. 디폴트 값은 False이다.

## example
```
from airflow.decorators import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
# @dag 바로 밑에 사용하고자 하는 task 선언
def example_python_decorator():
    # 첫번째 파이썬 함수
    @task(task_id="print_the_context")
    # @task 바로 밑에 기존에 사용하고자 하는 함수 선언
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return "Whatever you return gets printed in the logs"

    # 기존에는 run_this = PythonOperator(task_id="print_the_context", python_callable=print_context) 였음
    # 함수 이름을 인자로 지정
    run_this = print_context()

    # 두번째 파이썬 함수             # @task 내에서 인자를 지정. 기존에는 PythonOperator 내에서 인자를 지정하였음                        
    @task(task_id="log_sql_query", templates_dict={"query": "sql/sample.sql"}, templates_exts=[".sql"])
    def log_sql(**kwargs):
        logging.info("Python task decorator query: %s", str(kwargs["templates_dict"]["query"]))

    log_the_sql = log_sql()

    # 세번째 파이썬 함수
    @task
    def my_sleeping_function(random_base):
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

    for i in range(5):
        sleeping_task = my_sleeping_function.override(task_id=f"sleep_for_{i}")(random_base=i / 10)
                                            # override는 task 객체 내의 특정 속성 값을 재정의(override)하는 데 사용
                                            # for문을 돌면서 변화하는 random_base 값에 따라 task 객체를 생성하면서 값을 override
        run_this >> log_the_sql >> sleeping_task
```
