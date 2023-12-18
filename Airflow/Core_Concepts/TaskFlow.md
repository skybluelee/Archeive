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
`task` 함수에서 로깅을 사용하려면 간단히 Python의 로깅 시스템을 가져와서 사용하면 됩다.
```
import logging

logger = logging.getLogger("airflow.task")
```
이렇게 생성된 모든 로깅 라인은 작업 로그에 기록된다.
# 임의의 객체를 인자로 전달하기
위에서 언급했던 대로 TaskFlow는 XCom을 사용하여 각 task로 변수를 전달할 수 있다. 이 행위는 인자로 사용되는 변수가 직렬화시킬 때 필요하다.
Airflow는 기본적으로 모든 내장 형식(예: int 또는 str)을 지원하며, `@dataclass` 또는 `@attr.define`으로 데코레이트된 객체도 지원한다.
아래의 예제는 `@attr.define`으로 장식된 `Dataset`을 TaskFlow와 함께 사용하는 방법을 보여준다.
```
import json
import pendulum
import requests

from airflow import Dataset
from airflow.decorators import dag, task

SRC = Dataset(
    "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/ytd/12/1880-2022.json"
)
now = pendulum.now()


@dag(start_date=now, schedule="@daily", catchup=False)
def etl():
    @task()
    def retrieve(src: Dataset) -> dict:
        resp = requests.get(url=src.uri)
        data = resp.json()
        return data["data"]

    @task()
    def to_fahrenheit(temps: dict[int, float]) -> dict[int, float]:
        ret: dict[int, float] = {}
        for year, celsius in temps.items():
            ret[year] = float(celsius) * 1.8 + 32

        return ret

    @task()
    def load(fahrenheit: dict[int, float]) -> Dataset:
        filename = "/tmp/fahrenheit.json"
        s = json.dumps(fahrenheit)
        f = open(filename, "w")
        f.write(s)
        f.close()

        return Dataset(f"file:///{filename}")

    data = retrieve(SRC)
    fahrenheit = to_fahrenheit(data)
    load(fahrenheit)


etl()
```
`Dataset`을 사용하는 추가 이점은 해당 `Dataset`이 입력 인수로 사용될 경우 자동으로 `inlet`으로 등록되며, 작업의 반환 값이 `Dataset`이거나 `list[Dataset]`인 경우 자동으로 `outlet`으로 등록된다는 것이다.
## Custom Object
사용자 지정 객체를 전달하고 싶은 경우가 있다.
일반적으로 클래스를 `@dataclass` 또는 `@attr.define`으로 데코레이트하고 Airflow는 필요한 작업을 처리한다.
그러나 직접 직렬화를 제어하고 싶을 때도 있다.
이를 위해 클래스에는 `serialize()` 메서드를 추가하고 클래스에는 `deserialize(data: dict, version: int)` 정적 메서드를 추가하면 된다.
```
from typing import ClassVar


class MyCustom:
    __version__: ClassVar[int] = 1

    def __init__(self, x):
        self.x = x

    def serialize(self) -> dict:
        return dict({"x": self.x})

    @staticmethod
    def deserialize(data: dict, version: int):
        if version > 1:
            raise TypeError(f"version > {MyCustom.version}")
        return MyCustom(data["x"])
```
## Object Versioning
직렬화에 사용될 객체에 버전을 지정하는 것은 좋은 습관이다.
이를 위해 클래스에 `__version__: ClassVar[int] = <x>`를 추가하라.
Airflow는 클래스가 역호환성을 가진다고 가정하므로 버전 2가 버전 1을 역직렬화할 수 있어야 한다.
역직렬화에 대한 사용자 지정 논리가 필요한 경우 `deserialize(data: dict, version: int)`가 명시되어 있는지 확인하라.

참고: `__version__`의 타이핑은 필수이며 `ClassVar[int]`로 지정되어야 한다.
# Sensors and the TaskFlow API
2.5.0 버전에 추가됨.

TaskFlow API를 사용한 sensor 작성 예시는 [Using the TaskFlow API with Sensor operators](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html#taskflow-task-sensor-example)에서 확인할 수 있다.
# History
TaskFlow API는 Airflow 2.0부터 새롭게 도입된 것으로, 이전 버전의 Airflow에서 비슷한 목표를 달성하기 위해 훨씬 더 많은 코드를 사용하는 `PythonOperator`를 사용한 DAG를 더 많이 볼 것이다.

TaskFlow API의 추가 및 설계에 대한 더 많은 자료는 [AIP-31: “TaskFlow API” for clearer/simpler DAG definition](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=148638736)에서 확인할 수 있다.
