**본 문서는 Airflow 공식 문서 [TaskFlow](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)를 참조함**
# TaskFlow
2.0 버전부터 추가됨.

만약 DAG의 대부분을 operator가 아닌 파이썬 코드로 작성했다면, TaskFlow API는 `@task` 데코레이터를 사용하여 추가적인 보일러플레이트 없이 깔끔한 DAG를 쉽게 작성할 수 있다.
> 보일러플레이트(boilerplate): 불필요한 추가 코드 또는 작업

