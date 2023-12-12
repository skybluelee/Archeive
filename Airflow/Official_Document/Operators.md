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
