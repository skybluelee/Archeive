**본 문서는 Airflow 공식 문서 [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)를 참조함**
# XComs
XComs(크로스 통신)은 task 간에 서로 대화할 수 있도록 하는 메커니즘으로, 기본적으로 task는 완전히 격리되어 있고 완전히 다른 기기에서 실행된다.

XCom은 키(본질적으로 자신의 이름)뿐만 아니라 `task_id`와 `dag_id`로 식별된다.
그들은 어떤 (직렬화 가능한) 값을 가질 수 있지만, 그들은 작은 양의 데이터만 처리하기 위해 설계되었다.
데이터프레임과 같은 대량의 값을 전달하는 데는 사용하지 말라.

XCom은 명시적으로 Task Instance의 `xcom_push` 및 `xcom_pull` 메서드를 사용하여 그 저장소로 "푸시" 및 "풀"한다.
```
# pushes data in any_serializable_value into xcom with key "identifier as string"
task_instance.xcom_push(key="identifier as a string", value=any_serializable_value)
```
다른 task에서 사용할 값을 "task-1"이라는 task 내에서 푸시하려면 위와 같이 코드를 작성할 수 있다.
***
```
# pulls the xcom variable with key "identifier as string" that was pushed from within task-1
task_instance.xcom_pull(key="identifier as string", task_ids="task-1")
```
그런 다음 위의 코드에서 푸시한 값을 다른 작업에서 끌어오려면 위과 같이 코드를 작성할 수 있다.

많은 operator들은 `do_xcom_push` 인자가 `True`로 설정되어 있으면(기본값), 결과를 `return_value`라는 XCom 키로 자동으로 푸시한다.
`@task` 함수들도 이와 마찬가지로 동작한다.
```
# "pushing_task"에서 return_value XCOM을 끌어옵니다.
value = task_instance.xcom_pull(task_ids='pushing_task')
```
`xcom_pull`은 키를 전달하지 않으면 기본적으로 `return_value`를 사용하므로 위와 같은 코드를 작성할 수 있다.
```
SELECT * FROM {{ task_instance.xcom_pull(task_ids='foo', key='table_name') }}
```
또한 [templates](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#concepts-jinja-templating)에서도 XCom을 사용할 수 있다.

XCom은 Variables의 관련 항목이며, 주된 차이점은 XCom이 task 객체별이며 DAG 실행 내에서 통신을 위해 설계되었는 반면, Variables는 전역(global)이며 전반적인 구성 및 값 공유를 위해 설계되었다는 것이다.

참조 - 만약 첫번째  task 실행이 성공하지 못한다면, 모든 재시도 task XComs가 task 동작을 멱등적으로 만들기 위해 제거될 것이다.

# Custom XCom Backends
XCom 시스템은 교체 가능한 백엔드를 가지고 있으며, `xcom_backend` 구성 옵션을 통해 어떤 백엔드를 사용할지 설정할 수 있다.

자체 백엔드를 구현하려면, **BaseXCom**을 서브클래스화하고 `serialize_value` 및 `deserialize_value` 메서드를 오버라이드해야 한다.

또한 XCom 객체가 UI 또는 보고 목적으로 렌더링될 때 호출되는 `orm_deserialize_value` 메서드도 있다. 
XCom에 크거나 검색 비용이 높은 값이 있는 경우 이 메서드를 오버라이드하여 해당 코드를 호출하지 않고 대신 더 가벼운, 불완전한 표현을 반환하여 UI가 반응적으로 유지하도록 만들 수 있다.

또한 `clear` 메서드를 오버라이드하고 DAG 및 task에 대한 결과를 지울 때 이를 사용할 수 있다. 
이것은 사용자 지정 XCom 백엔드가 데이터 라이프사이클을 더 쉽게 처리할 수 있도록 도와준다.

# Working with Custom XCom Backends in Containers
Airflow가 배포된 환경에 따라(로컬, Docker, K8s 등) 사용자 정의 XCom 백엔드가 올바르게 초기화되었는지 확인하는 것은 유용할 수 있다.
예를 들어, 컨테이너 환경의 복잡성은 사용자의 백엔드가 컨테이나 배포 중에 정확히 로드되었는지 여부를 확인하기 어렵게 만든다.
아래의 내용은 사용자 지정 XCom 구현에 대한 신뢰를 높이는 데 도움이 될 수 있다.
```
from airflow.models.xcom import XCom

print(XCom.__name__)
```
먼저, 컨테이너 터미널에서 명령을 실행할 수 있는 경우 위와 같은 Python 코드를 실행하여 실제로 사용되고 있는 XCom 클래스의 이름을 출력할 수 있다.

이렇게 하면 사용중인 클래스의 이름이 출력된다.
***
```
from airflow.settings import conf

xcom_backend = conf.get("core", "xcom_backend")
```
또한 위와 같은 코드를 사용하여 Airflow의 구성을 검사할 수 있다.

# Working with Custom Backends in K8s via Helm
K8s에서 사용자 정의 XCom 백엔드를 실행하면 Airflow 배포가 더 복잡해진다.
간단히 말해 때로는 문제가 발생하며 디버깅이 어려울 수 있다.

예를 들어, Chart의 `values.yaml`에서 사용자 정의 XCom 백엔드를 정의하고 (`xcom_backend` 구성을 통해), Airflow가 클래스를 로드하지 못하면 전체 Chart 배포가 실패하며 각 pod 컨테이너가 반복적으로 다시 시작을 시도한다.

K8s에서 배포할 때 사용자 정의 XCom 백엔드는 `config` 디렉토리에 있어야 하며, 그렇지 않으면 Chart 배포 중에 찾을 수 없다.

관찰된 문제 중 하나는 흔적(trace)를 얻을 수 있는 윈도우의 크기가 매우 작기 때문에 컨테이너에서 로그를 얻기가 매우 어렵다는 것이다.
루트 원인을 결정할 수 있는 유일한 방법은 올바른 시간에 컨테이너 로그를 조회하고 획득하는 행운이 있는 경우이다.
이로 인해 전체 Helm 차트 배포가 성공적으로 이뤄지지 못할 수 있다.
