**본 문서는 Airflow 공식 문서 [Variable](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html)를 참조함**
# Variables
변수는 Airflow의 런타임 구성 개념으로, 전역적이며 task에서 쿼리할 수 있는 일반적인 키/값 저장소이다.
Airflow의 사용자 인터페이스를 통해 쉽게 설정하거나 JSON 파일로 대량 업로드할 수 있다.

```
from airflow.models import Variable

# Normal call style
foo = Variable.get("foo")

# Auto-deserializes a JSON value
bar = Variable.get("bar", deserialize_json=True)

# Returns the value of default_var (None) if the variable is not set
baz = Variable.get("baz", default_var=None)
```
변수를 사용하고자 한다면, 간단하게 import하고 해당 변수 모델을 `get` 메서드를 호출하면 된다.
***
```
# Raw value
echo {{ var.value.<variable_name> }}

# Auto-deserialize JSON value
echo {{ var.json.<variable_name> }}
```
[templates](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#concepts-jinja-templating) 또한 사용할 수 있다.
***
변수는 전역적이며 전체 설치를 포괄하는 전반적인 구성에만 사용해야 한다.
단일 task/operator에서 다른 task/operator로 데이터를 전달하기 위해서는 대신 XCom을 사용해야 한다.

또한 DAG 파일에 대부분의 설정 및 구성을 유지하고 소스 제어를 사용하여 버전을 지정하는 것이 좋다. 
변수는 실제로 런타임에 완전히 의존하는 값이기 때문이다.,

설정과 변수를 다루는 더 자세한 정보는 [Managing Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html)에서 확인할 수 있다.
