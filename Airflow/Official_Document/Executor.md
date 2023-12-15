**본 문서는 Airflow 공식 문서 [Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html)를 참조함**
# Executor
executor는 task 객체가 실행되는 메커니즘이다.
executor는 공통 API를 가지고 있으며 플러그 가능(pluggable), 즉 설치 요구 사항에 따라 executor를 교체할 수 있다.

Airflow는 한 번에 하나의 executor만 구성할 수 있다. 이는 설정 파일의 `[core]` 섹션에서 `executor` 옵션을 사용하여 설정할 수 있다.
```
[core]
executor = KubernetesExecutor
```
내장된 executor는 위와 같이 이름으로 참조된다.

참조 - Airflow 설정에 대한 더 많은 정보는 [Setting Configuration Options](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html)에서 확인할 수 있다.
***
```
$ airflow config get-value core executor
SequentialExecutor
```
현재 어떤 executor가 설정되어 있는지 확인하고 싶다면, `airflow config get-value core executor` 명령을 사용하면 된다.
# Executor Types
executor에는 2가지 유형이 존재한다. 
하나는 task를 로컬에서(`scheduler` 프로세스 내에서) 실행하고, 다른 하나는 task를 원격으로 실행하는 것이다(일반적으로 worker pool을 통해).
Airflow는 기본적으로 `SequentialExecutor`로 구성되어 있다.
이는 로컬 executor로, 실행을 위한 가장 간단한 옵션이다. 
그러나 `SequentialExecutor`는 병렬 태스크 실행을 허용하지 않기 때문에 프로덕션 환경에서는 적합하지 않다.
이로 인해 Airflow의 일부 기능(예: 센서 실행)이 제대로 작동하지 않을 수 있다.
대신, 소규모 단일 머신 프로덕션 설치에는 `LocalExecutor`를 사용하거나, 다중 머신/클라우드 설치에는 원격 실행기 중 하나를 사용해야 한다.

**Local Executors**
- [Debug Executor (deprecated)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html)
- [Local Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local.html)
- [Sequential Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/sequential.html)

**Remote Executors**
- [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html)
- [CeleryKubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery_kubernetes.html)
- [Dask Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/dask.html)
- [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html)
- [LocalKubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local_kubernetes.html)

참고 - 새로운 Airflow 사용자는 로컬이나 원격 executor 중 하나를 사용하는 분리된 executor 프로세스가 필요하다고 생각할 수도 있다.
하지만 이는 틀린 판단이다.
executor 로직은 스케줄러 프로세스 내부에서 실행하며, 선택한 실행기에 따라 작업을 로컬에서 실행하거나 실행하지 않을 것이다.

# 사용자만의 executor 작성하기
Airflow의 모든 executor는 공통 인터페이스를 구현하여 플러그 가능하며, 특정 executor는 Airflow 내의 모든 기능과 통합에 액세스할 수 있다.
주로 Airflow 스케줄러는 이 인터페이스를 사용하여 executor와 상호 작용하지만 로깅, CLI 및 backfill과 같은 다른 구성 요소도 사용한다.
이 공개 인터페이스는 **BaseExecutor**이다.
코드를 통해 가장 자세하고 최신의 인터페이스를 확인할 수 있으며, 몇 가지 중요 사항을 아래에 적어놓았다.

참고 - Airflow의 공개 인터페이스에 대한 자세한 내용은 [Public Interface of Airflow](https://airflow.apache.org/docs/apache-airflow/stable/public-airflow-interface.html)를 참조하라.

일부 사용자가 사용자 지정 executor를 작성하는 이유는 다음과 같을 수 있다.
- 특정 도구나 컴퓨팅을 위한 서비스와 같이 특정 사용 사례에 맞는 executor가 없는 경우.
- 선호하는 클라우드 공급자의 컴퓨팅 서비스를 활용하는 executor를 사용하고 싶은 경우.
- 사용자 또는 조직에만 사용 가능한 task 실행을 위한 개인 도구/서비스가 있는 경우.

## Important BaseExecutor Methods
이러한 메서드들은 사용자가 자체 executor를 구현할 때 오버라이딩하지 않아도 되지만 알고 있으면 유용하다.
- `heartbeat`: Airflow 스케줄러 Job 루프는 주기적으로 실행기의 `heartbeat` 메서드를 호출한다.
이는 Airflow 스케줄러와 executor 간의 주요 상호 작용 지점 중 하나이다.
이 메서드는 몇 가지 메트릭을 업데이트하고 새로 추가된 task를 실행하도록 유도하며 실행 중 또는 완료된 태스크의 상태를 업데이트한다.
- `queue_command`: Airflow Executor는 BaseExecutor 메서드를 호출하여 executor에서 실행할 작업을 제공한다. BaseExecutor는 간단히 executor 내부의 대기 중인 작업 목록에 TaskInstances를 추가한다.
- `get_event_buffer`: Airflow 스케줄러는 executor가 실행 중인 TaskInstances의 현재 상태를 검색하기 위해 이 메서드를 호출한다.
- `has_task`: 스케줄러는 이 BaseExecutor 메서드를 사용하여 executor가에 특정 task 객체가 이미 대기 중이거나 실행 중인지 여부를 확인한다.
- `send_callback`: executor에 구성된 sink로 콜백을 전송한다.

## Mandatory Methods to Implement
다음 메서드들은 Airflow에서 executor를 지원할 수 있도록 최소한으로 오버라이딩되어야 한다.
- `sync`: `sync` 메서드는 executor의 동작 중에 주기적으로 호출된다.
이 메서드를 구현하여 executor가 알고 있는 task의 상태를 업데이트한다.
선택적으로 스케줄러로부터 받은 대기 중인 task를 실행하려고 시도할 수도 있다.
- `execute_async`: 명령을 비동기적으로 실행한다. 여기서 명령은 Airflow CLI 명령으로 Airflow task를 실행하는 것을 의미한다.
이 메서드는 스케줄러에 의해 주기적으로 실행되는 실행기 하트비트 중에 (몇 개의 레이어를 거쳐) 호출된다.
실제로 이 메서드는 대개 태스크를 내부 또는 외부의 task 대기열에 인큐하는 용도로 사용된다(예: KubernetesExecutor).
그러나 직접적으로 task를 실행하기도 합니다(예: LocalExecutor). 이는 실행기에 따라 다를 수 있다.

## Optional Interface Methods to Implement
다음 메서드들은 Airflow executor를 기능적으로 사용하려면 오버라이딩이 필요하지 않다. 그러나 이러한 메서드를 구현하면 강력한 기능과 안정성이 제공될 수 있다.
- `start`: Airflow 스케줄러(및 백필) 작업은 executor 객체를 초기화한 후에 이 메서드를 호출한다. executor에 필요한 추가 설정을 여기에서 완료할 수 있다.
- `end`: Airflow 스케줄러(및 백필) 작업은 종료하는 동안 이 메서드를 호출합니다. 실행 중인 작업을 완료하기 위해 필요한 동기화 정리를 여기서 수행해야 한다.
- `terminate`: executor를 강제적으로 중지시킨다. 동기적으로 완료를 기다리지 않고 진행 중인 작업을 즉시 중지 또는 종료할 수 있다.
- `cleanup_stuck_queued_tasks`: task가 `task_queued_timeout`보다 오랜 시간 동안 대기 중인 상태로 남아 있으면 스케줄러에 의해 수집되어 executor에 제공되며,
이 메서드를 통해 이를 처리(제거 혹은 중지)할 기회를 부여하고 사용자에게 경고 메시지를 표시할 수 있다.
- `try_adopt_task_instances`: 버려진 task(예: 스케줄러 작업이 중단된 경우)는 이 메서드를 통해 executor에 제공되어 채택하거나 다른 방식으로 처리할 수 있다.
채택할 수 없는 태스크(기본적으로 BaseExecutor는 모든 태스크를 채택할 수 없다고 가정함)는 반환되어야 한다.
- `get_cli_commands`: 이 메서드를 구현함으로써 executor는 사용자에게 CLI 명령을 제공할 수 있다. 자세한 내용은 아래의 CLI 섹션을 참조하라.
- `get_task_log`: 이 메서드를 구현함으로써 executor는 Airflow task 로그에 로그 메시지를 제공할 수 있다. 자세한 내용은 아래의 로깅 섹션을 참조하라.

## Compatibility Attributes
`BaseExecutor` 클래스 인터페이스에는 Airflow 코어 코드에서 executor가 호환 여부를 확인하기 위해 사용하는 일련의 속성이 포함되어 있다. 
Airflow executor를 직접 작성할 때 사용 사례에 따라 이러한 속성을 올바르게 설정해야 한다.
각 속성은 기능을 활성화/비활성화하거나 실행기에서 기능을 지원/지원하지 않음을 나타내는 불리언(Boolean) 값이다.
- `supports_pickling`: executor가 실행 전에 데이터베이스에서 피클된 DAG를(파일 시스템에서 DAG 정의를 읽는 대신) 읽어올 수 있는지 여부를 나타낸다. 
- `supports_sentry`: executor가 [Sentry](https://sentry.io/)를 지원하는지 여부를 나타낸다.
- `is_local`: executor가 원격 또는 로컬인지 여부를 나타낸다. 위의 Executor Types 섹션을 참조하라.
- `is_single_threaded`: executor가 단일 스레드인지 여부를 나타냅니다. 이것은 특히 어떤 데이터베이스 백엔드가 지원되는지에 관련이 있다. 단일 스레드 실행기는 SQLite를 포함한 모든 백엔드에서 실행할 수 있다.
- `is_production`: executor가 프로덕션 용도로 사용되어야 하는지 여부를 나타낸다. 비프로덕션 환경에서 executor가 사용하려고 할 때 사용자에게 UI 메시지가 표시된다.
- `change_sensor_mode_to_reschedule`: Airflow 센서를 poke 모드에서 실행하면 executor의 스레드를 차단할 수 있으며 경우에 따라 Airflow도 차단할 수 있다.
- `serve_logs`: executor가 로그를 제공하는지 여부를 나타낸다. 태스크에 대한 로깅에 대한 자세한 내용은
[Logging for Tasks](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/logging-tasks.html)를 참조하라.

## CLI
```
@staticmethod
def get_cli_commands() -> list[GroupCommand]:
    sub_commands = [
        ActionCommand(
            name="command_name",
            help="Description of what this specific command does",
            func=lazy_load_command("path.to.python.function.for.command"),
            args=(),
        ),
    ]

    return [
        GroupCommand(
            name="my_cool_executor",
            help="Description of what this group of commands do",
            subcommands=sub_commands,
        ),
    ]
```
Airflow executor는 `get_cli_commands` 메서드를 구현하여 `airflow` 명령 줄 도구에 포함될 CLI 명령을 제공할 수 있다.
예를 들어 `CeleryExecutor` 및 `KubernetesExecutor`와 같은 executor는 이 메커니즘을 활용한다.
이 명령은 필요한 워커 설정, 환경 초기화 또는 기타 구성을 수행하는 데 사용될 수 있다.
명령은 현재 구성된 executor에 대해서만 제공된다.
executor에서 CLI 명령을 제공하는 의사 코드 예제는 위에서 확인할 수 있다.

참고 - 현재 Airflow 명령 네임스페이스에는 엄격한 규칙이 없다. Airflow executor나 구성 요소와 충돌을 일으키지 않도록 CLI 명령에 충분히 고유한 이름을 사용하는 것은 개발자의 책임이다.

참고 - 새로운 executor를 만들거나 기존의 executor를 업데이트할 때, 반드시 모듈 레벨에서 비용이 많이 드는 작업 또는 코드를 가져오거나 실행하지 않도록 주의해야 한다.
executor 클래스는 여러 곳에서 import할 수 있고 import가 느리면 Airflow 환경, 특히 CLI 명령의 성능에 부정적인 영향을 미칠 수 있다.

## Logging
```
def get_task_log(self, ti: TaskInstance, try_number: int) -> tuple[list[str], list[str]]:
    messages = []
    log = []
    try:
        res = helper_function_to_fetch_logs_from_execution_env(ti, try_number)
        for line in res:
            log.append(remove_escape_codes(line.decode()))
        if log:
            messages.append("Found logs from execution environment!")
    except Exception as e:  # No exception should cause task logs to fail
        messages.append(f"Failed to find logs from execution environment: {e}")
    return messages, ["\n".join(log)]
```
실행기는 `get_task_logs` 메서드를 구현하여 Airflow task 로그에 포함될 로그 메시지를 제공할 수 있다.
이는 task 실패의 경우 실행 환경이 Airflow task 코드가 아닌 실행 환경 자체에서 발생한 것일 수 있으므로 추가적인 컨텍스트가 있는 경우 유용할 수 있다. 
또한 실행 환경에서의 설정/해체 로깅을 포함하는 데도 도움이 될 수 있다. `KubernetesExecutor`는 특정 Airflow task를 실행한 pod에서 로그를 가져와 해당 Airflow task의 로그에 표시하는 데 이 기능을 활용한다.
executor에서 task 로그를 제공하는 코드 예제는 위에서 확인할 수 있다.

## Next Steps
```
[core]
executor = my_company.executors.MyCustomExecutor
```
새로운 executor 클래스를 `BaseExecutor` 인터페이스를 구현하여 만들었다면, 해당 Executor를 Airflow에서 사용하도록 설정하려면 `core.executor` 구성 값을 executor 모듈 경로로 설정하면 된다.

참고 - Airflow 구성에 대한 자세한 내용은 [Setting Configuration Options](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html)을 참조하고,
Airflow에서 Python 모듈을 관리하는 방법에 대한 자세한 내용은 [Modules Management](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html)를 참조하십시오.
