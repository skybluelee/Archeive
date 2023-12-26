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
>
> 아래 명령을 실행하여 충분한 메모리가 있는지 확인할 수 있다.
> ```
> docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
> ```

> 경고
>
> 몇몇 작업 시스템(Fedora, ArchLinux, RHEL, Rocky)와 같은 운영 체제들은 OS 팀에 의해 유지보수되는 커뮤니티 도커 구현 내에서 Airflow가 Docker Compose 내에서 실행될 때 100%의 메모리를 소비하는 커널 변경 사항을 도입하였다.
>
> 이는 Airflow의 일부 종속성이 문제를 가진 호환되지 않는 containerd 구성과 관련된 문제로, 몇 가지 이슈에서 추적되고 있습니다:
> - [Moby issue](https://github.com/moby/moby/issues/43361)
> - [Containerd issue](https://github.com/containerd/containerd/)
>
> containerd 팀으로부터 아직 해결책이 제시되지 않았지만, [Linux에 Docker Desktop을 설치하는 것](https://docs.docker.com/desktop/install/linux-install/)이
> 이 문제를 해결한다는 [이 댓글](https://github.com/moby/moby/issues/43361#issuecomment-1227617516)에서 언급되었으며,
> 이를 통해 Breeze를 문제없이 실행할 수 있게 되었다.

## Fetching docker-compose.yaml
Docker Compose에서 Airflow를 배포하려면 `docker-compose.yaml` 파일을 가져와야 한다.
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```
> 버전에 관해
>
> 해당 버전(현재는 2.8.0)은 주기적으로 업데이트된다.

> 중요!
>
> 2023년 7월부터 컴포즈 V1의 업데이트가 중단되었다.
> 도커 컴포즈의 새로운 버전으로 업데이트하는 것을 강력하게 권장하며, 기존의 `docker-compose.yaml`은 컴포즈 V1에서 제대로 동작하지 않을 수 있다.

이 파일은 몇가지 서비스에 대한 설정을 갖고 있다.
- `airflow-scheduler`: 스케줄러는 모든 task와 DAG를 모니터링하고, task의 의존성이 완료되면 작업 인스턴스를 트리거한다.
- `airflow-webserver`: 웹서버는 http://localhost:8080에서 사용할 수 있다.
- `airflow-worker`: 워커는 스케줄러에 의해 주어진 작업을 실행한다.
- `airflow-triggerer`: 트리거는 지연 가능한 task를 위한 이벤트 루프를 실행한다.
- `airflow-init`: 초기화 서비스이다.
- `postgres`: 데이터베이스이다.
- `redis`: 스케줄러에서 워커로 메시지를 전달하는 redis 브로커이다.

추가로, `--profile flower` 옵션을 추가하거나(예: `docker compose --profile flower up`) 명시적으로 명령줄에서 특정하여(예: `docker compose up flower`) flower를 활성화할 수 있다.
- `flower`: 환경을 모니터링하는 [flower app](https://flower.readthedocs.io/en/latest/)을 실행한다. `http://localhost:5555`에서 사용 가능하다.

모든 서비스는 Airflow와 CeleryExecutor를 실행할 수 있게 만든다.
더 많은 정보는 [Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)를 참조하라.

컨테이너가 마운트되는 몇몇 디렉토리가 존재하며, 이 디렉토리는 컴퓨터와 컨테이너 사이에서 동기화된다.
- `./dags`: DAG 파일을 여기에 넣을 수 있다.
- `./logs`: 작업 실행 및 스케줄러에서의 로그가 포함되어 있다.
- `./config`: 사용자 정의 로그 파서를 추가하거나 cluster 정책을 구성하기 위해 airflow_local_settings.py를 추가할 수 있다.
- `./plugins`: 사용자 정의 플러그인을 여기에 넣을 수 있다.

이 파일은 가장 최근의 Airflow 이미지[apache/airflow](https://hub.docker.com/r/apache/airflow)를 사용한다.
새로운 파이썬 라이브러리나, 시스템 라이브러리가 필요하다면 [이미지를 빌드](https://airflow.apache.org/docs/docker-stack/index.html)해야 한다.

## Initializing Environment
Airflow를 시작하기 전에, 사용 환경에 대한 준비, 즉 필요한 파일, 디렉토리를 생성하고 데이터베이스를 초기화해야 한다.

### Setting the right Airflow user
리눅스에서 빠르게 시작하기 위해서 호스트의 user id와 group id가 0으로 설정되어 있는 것을 알아야 한다.
그렇지 않으면 dag, log, plugin에서 생성된 파일은 루트 사용자 소유로 생성될 것이다.
도커 컴포즈에서 이를 설정해야 한다.
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
[도커 컴포즈 환경 변수](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#docker-compose-env-variables)를 확인하라.

다른 작업 시스템에서 `AIRFLOW_UID`가 설정되지 않았다는 경고를 받을 수도 있으나, 무시해도 된다.
```
`docker-compose.yaml` 파일이 있는 디렉토리에 `.env` 파일을 생성하여 이 경고를 제거할 수 있다.
```
AIRFLOW_UID=50000

### Initialize the database
모든 작업 시스템에서 데이터베이스 마이그레이션을 실행하고 사용자 계정을 생성해야 한다.
이는 아래 코드를 실행하면 된다.
```
docker compose up airflow-init
```
초기화가 완료되면, 아래와 같은 메시지가 출력될 것이다.
```
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.8.0
start_airflow-init_1 exited with code 0
```
id와 비밀번호가 `airflow`인 계정이 생성되었다.

## Cleaning-up the environment
도커 컴포즈 환경은 "빠른 시작"에 맞추어져 있다.
프로덕션 환경에서 사용되도록 설계되지 않았으며 여러 주의사항이 있다.
그 중 하나는 어떤 문제에서도 복구하는 가장 좋은 방법이 그것을 정리하고 처음부터 다시 시작하는 것이다.

아래와 같은 방법을 사용하는 것이 가장 좋은 방법이다.
- `docker-compose.yaml` 파일이 있는 디렉토리에서 `docker compose down --volumes --remove-orphans` 명령어 실행하기.
- `docker-compose.yaml` 파일에 대한 모든 디렉토리를 `rm -rf '<DIRECTORY>'` 명령어를 사용하여 제거하기.
- `docker-compose.yaml` 파일을 다시 다운로드하는 것부터 시작하여 다시 시작하기.

## Running Airflow
아래 코드를 실행하여 서비스를 시작할 수 있다.
```
docker compose up
```
> 주의: docker-compose는 오래된 명령어로 [Stackoverflow](https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose)도 확인하라.

컨테이너의 상태를 확인하고 컨테이너가 unhealthy한 상태에 놓여있지 않는지 확인해야 한다.
```
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                              NAMES
247ebe6cf87a   apache/airflow:2.8.0   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-worker_1
ed9b09fc84b1   apache/airflow:2.8.0   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    8080/tcp                           compose_airflow-scheduler_1
7cb1fb603a98   apache/airflow:2.8.0   "/usr/bin/dumb-init …"   3 minutes ago    Up 3 minutes (healthy)    0.0.0.0:8080->8080/tcp             compose_airflow-webserver_1
74f3bbe506eb   postgres:13            "docker-entrypoint.s…"   18 minutes ago   Up 17 minutes (healthy)   5432/tcp                           compose_postgres_1
0bd6576d23cb   redis:latest           "docker-entrypoint.s…"   10 hours ago     Up 17 minutes (healthy)   0.0.0.0:6379->6379/tcp             compose_redis_1
```

## Accessing the environment
Airflow를 시작하고, 3가지 방법을 사용하여 상호작용할 수 있다.
- [CLI 명령](https://airflow.apache.org/docs/apache-airflow/stable/howto/usage-cli.html) 실행하기.
- [웹 인터페이스](https://airflow.apache.org/docs/apache-airflow/stable/ui.html) 사용하기.
- [REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html) 사용하기.

### Running the CLI commands
CLI 명령어를 사용할 수 있지만, `airflow-*` 서비스에 미리 정의되어 있어야 한다.
예를 들어 `airflow info`를 실행하기 위해서는 아래 명령어를 실행해야 한다.
```
docker compose run airflow-worker airflow info
```
만약 리눅스나 Mac OS를 사용한다면, 더 단순한 명령어를 사용하는 래퍼 스크립트를 다운받아 쉽게 동작시킬 수 있다.
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/airflow.sh'
chmod +x airflow.sh
```
아래 명령어를 사용하여 간편하게 실행할 수 있다.
```
./airflow.sh info
```
컨테이너의 bash shell을 사용하기 위한 파라미터로 `bash`를 사용하거나 파이썬 컨테이너를 사용하기 위해 `python`을 사용할 수 있다.
```
./airflow.sh bash
```
```
./airflow.sh python
```

### Accessing the web interface
클러스터가 시작되면, 웹 인터페이스에 로그인하고, DAG를 실행할 수 있다.

웹 서버는 `http://localhost:8080`에서 사용할 수 있다.
기본 id와 비밀번호는 `airflow`이다.

### Sending requests to the REST API
[기본 사용자 이름, 비밀번호 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 현재 REST API를 지원한다, 즉 request를 API로 전송하는 도구가 존재한다.

웹 서버는 `http://localhost:8080`에서 사용할 수 있다.
기본 id와 비밀번호는 `airflow`이다.

pool list를 찾기 위한 request를 보내는 간단한 `curl`을 사용한 명령은 아래와 같다.
```
ENDPOINT_URL="http://localhost:8080/"
curl -X GET  \
    --user "airflow:airflow" \
    "${ENDPOINT_URL}/api/v1/pools"
```

## Cleaning up
컨테이너를 중단, 삭제하고 데이터베이스와 다운로드한 이미지를 제거하려면 아래의 명령을 실행하라.
```
docker compose down --volumes --rmi all
```

## Using custom images
