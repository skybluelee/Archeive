**본 문서는 Airflow 공식 문서 [Sensors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html)를 참조함**
# Sensors
Sensor는 정확히 하나의 작업을 수행하도록 설계된 특수한 operator 유형이다.
Sensor는 시간 기반이거나 파일을 기다리거나 외부 이벤트를 기다리는 등 여러 가지 상황에서 어떤 일이 발생할 때까지 기다리고, 성공하게 만들어 다운스트림 작업이 실행될 수 있도록 만든다.

주로 대기 상태에 있기 때문에 sensor는 더 효율적으로 사용할 수 있도록 두 가지 실행 모드가 있다.
1. `poke`(기본값): 센서는 전체 실행 시간 동안 worker 슬롯을 차지합니다.
2. `reschedule`: 센서는 확인하는 동안에만 worker 슬롯을 차지하고 확인 간에는 일정한 기간 동안 대기합니다.

`poke` 및 `reschedule` 모드는 센서를 인스턴스화할 때 직접 구성할 수 있다.
일반적으로 그들 간의 트레이드 오프는 대기 시간입니다. 1초마다 확인하는 것은 `poke` 모드여야 하며, 1분마다 확인하는 것은 `reschedule` 모드여야 합니다.

operator와 마찬가지로 Airflow에는 주요 Airflow와 공급자(provider) 시스템을 통해 사용할 수 있는 미리 구축된 다양한 센서가 있다.
***
[Deferrable Operators & Triggers](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html)
