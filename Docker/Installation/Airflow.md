**본 문서는 [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)를 해석한 문서이다.**
# Running Airflow in Docker
이 빠른-시작 가이드는 Airflow를 빠르게 설정하고 도커 내에서 [CeleryExecutor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html)를 실행하게 만들어준다.

> 주의
>
> 이 절차는 학습하는데 유용할 수 있다.
> 하지만 실제 상황에 알맞게 사용하도록 조정하는 작업은 복잡할 수 있다.
> 이 절차에 변화를 주는 것은 도커와 도커 컴포즈에 대한 전문 지식을 필요로하며 Airflow는 이에 도움을 줄 수 없다.
>
> 이러한 이유로 Airflow가 프로덕션 환경에서 준비가 된 후에 쿠버네티스와 [Official Airflow Community Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html)를 사용하는 것을 권장한다.

## Before you begin
이 절차는 도커와 도커 컴포즈에 대해 알고 있다고 가정하고 진행한다.
도커나 도커 컴포즈를 사용해본적이 없다면, [Docker Quick Start](https://docs.docker.com/get-started/)의 Docker Compose 섹션을 참조하라.

아래 단계는 설치에 필요한 단계로, 없다면 설치하라.
1. 사용 공간에 Docker Community Edition (CE)를 설치하라. OS에 맞게 도커를 구성하고, Airflow 컨테이너가 적절히 동작하기 위해서는 최소 4GB의 메모리가 필요하다.
더 많은 정보는 [Docker for Windows](https://docs.docker.com/docker-for-windows/#resources) 또는 [Mac documentation](https://docs.docker.com/docker-for-mac/#resources)에서 리소스 섹션을 참고하라.
2. 사용 공간에 도커 컴포즈 2.14.0 이상의 버전을 설치하라.

오래된 버전의 도커 컴포즈는 Airflow `docker-compose.yaml` 파일에서 필요한 모든 특징을 지원하지 않으므로, 최소한의 버전이 맞는지 여러번 확인하라.

> 팁
>
> macOS에서 도커의 기본 메모리 할당량은 Airflow를 작동시키기에 충분하지 않을 수 있다.
> 충분한 메모리가 할당되지 않으면, 웹서버가 계속해서 재시작하는 원인이 될 수 있다.
> 도커 엔진에는 적어도 4GB의 메모리를 할당해야 한다(가능하면 8GB).

> 아래 명령을 실행하여 충분한 메모리가 있는지 확인할 수 있다.
> ```docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'```
