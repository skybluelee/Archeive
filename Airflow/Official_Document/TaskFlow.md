**본 문서는 Airflow 공식 문서 [TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)를 참조함**
# TaskFlow
2.0 버전부터 추가됨.

만약 DAG의 대부분을 operator가 아닌 파이썬 코드로 작성했다면, TaskFlow API는 `@task` 데코레이터를 사용하여 추가적인 보일러플레이트 없이 깔끔한 DAG를 쉽게 작성할 수 있다.
> 보일러플레이트(boilerplate): 불필요한 추가 코드 또는 작업

```
from airflow.decorators import task
from airflow.operators.email import EmailOperator

@task
def get_ip():
    return my_ip_service.get_main_ip()

@task(multiple_outputs=True)
def compose_email(external_ip):
    return {
        'subject':f'Server connected from {external_ip}',
        'body': f'Your server executing Airflow is connected from the external IP {external_ip}<br>'
    }

email_info = compose_email(get_ip())

EmailOperator(
    task_id='send_email',
    to='example@example.com',
    subject=email_info['subject'],
    html_content=email_info['body']
)
```
TaskFlow는 XComs를 사용하여 task간의 입력과 출력을 자동으로 처리한다. 또한 자동으로 종속성을 계산합니다.
DAG 파일에서 TaskFlow 함수를 호출할 때 해당 함수를 실행하는 대신 결과를 나타내는 XCom 객체 (`XComArg`)를 얻게 되며, 이를 이용하여 downstream task나 operator에 대한 입력으로 사용할 수 있다.

여기에는 `get_ip`, `compose_email` 및 `send_email`이라는 세 가지 작업이 있다.

처음 두 작업은 TaskFlow를 사용하여 선언되었고 `get_ip`의 반환 값을 `compose_email`로 자동으로 전달한다. 
XCom을 효과적으로 연결할 뿐만 아니라 `compose_email`이 `get_ip`의 downstream에 있음을 자동으로 선언한다.

`send_email`은 더 전통적인 연산자이지만 `compose_email`의 반환 값을 `send_email`의 파라미터로 설정할 수 있으며 다시 한 번 자동으로 `compose_email`의 downstream에 있어야만 동작한다.
***
```
@task
def hello_name(name: str):
    print(f'Hello {name}!')

hello_name('Airflow users')
```
TaskFlow 함수를 호출할 때 일반 값이나 변수를 사용할 수도 있다.
예를 들어, 위 코드는 예상대로 작동할 것이다(그러나 물론 DAG가 실행될 때까지 작업 내부의 코드는 실행되지 않는다. 그때까지 name 값은 작업 매개변수로 유지된다).

TaskFlow에 대해 더 많이 배우고 싶다면 [TaskFlow tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)을 참조하라.
# Context
호출 가능한 함수를 실행할 때 Airflow는 함수에서 사용할 수 있는 키워드 인자 집합을 전달한다. 
이러한 kwargs 집합은 정확히 Jinja 템플릿에서 사용할 수 있는 [컨텍스트 변수(context variable)](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#templates-variables)에 해당한다.

이 작업을 수행하려면 함수 헤더에 `**kwargs`를 정의해야 하며, `ti=None`과 같은 키워드 인수를 직접 추가하여 작업 인스턴스가 전달되도록 할 수 있다.
# Logging
