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
- show_return_value_in_logs (bool) – 반환 값 로그를 표시할지 여부를 나타내는 boolean 값이다. 기본값은 True로, 반환 값 로그 출력을 허용한다.
큰 데이터(예: 대량의 XCom을 TaskAPI에 전송하는 경우)를 반환할 때 로그 출력을 방지하려면 False로 설정하면 된다.

# task
`airflow.operators.python.task(python_callable=None, multiple_outputs=None, **kwargs)`

`airflow.decorators.task()`는 deprecated되었으므로 `python.task`를 사용하라.

`@task.python`를 호출하고 Python 함수를 Airflow task로 변환하게 해준다.

## Parameter
- python_callable (Callable) – 호출 가능한 객체에 대한 참조, 즉 실행 가능한 함수나 메서드를 가리킨다.
- op_kwargs (Mapping[str, Any] | None) – 함수 내에서 사용할 키워드 인자들의 dictionary로 함수에서 언패킹되어 사용된다.
- op_args (Collection[Any] | None) – 함수 내에서 사용할 위치 인자들의 목록으로 함수 호출 시 언패킹되어 함수에 전달된다.
- multiple_outputs (bool | None) – 설정된 경우, 함수의 반환 값은 여러 개의 XCom 값으로 언패킹(unrolled)된다. dictionary는 키를 키로 사용하여 XCom 값으로 언패킹된다. 디폴트 값은 False이다.
