**본 문서는 [airflow-spark by cordon-thiago](https://github.com/cordon-thiago/airflow-spark/tree/master)를 참조하였다.**

# Airflow와 Spark을 사용하는 2가지 방식
첫번째 방식은 Airflow와 Spark을 다른 이미지에서 각각 사용하는 방식이다. 해당 방식은 [docker-spark-airflow by yTek01](https://github.com/yTek01/docker-spark-airflow) 참조.

두번째 방식은 Airflow를 기반으로 Spark 이미지를 `docker-compose.yaml` 파일 내에 저장하여 사용하는 방식으로, 본 문서에서 설명하는 방식이다.

# 고려 사항
## Python 버전
`apache/airflow:2.7.0-python3.11` 이미지를 사용하였다.
Airflow의 Python 버전과 Spark의 Python 버전이 다르면 실행이 되지 않는다.
현재 사용중인 Spark의 이미지에서 Python 3.11버전을 사용하기에 Airflow의 Python 버전도 동일하게 설정하였다.

Spark의 이미지가 사용하는 Python 버전은
```
docker exec -it <container_name> bash
python --version
```
을 사용하여 확인할 수 있다.

## Spark Connection
또한 가장 최근인 2.8.0 버전을 사용하지 않는 이유는 Spark와의 Connection을 만들기 위해서는 `openjdk-11-jdk`를 설치해야 한다.

이 과정은 `Dockerfile`에서 실행하는데, 2.8.0 버전의 경우 이미지 빌드 중 오류가 발생하여 2.7.0 버전을 사용하였다.

# 파일
## requirements.txt
```
apache-airflow
pyspark
grpcio-status
apache-airflow-providers-apache-spark
```
Spark과의 Connection을 생성하기 위해서는 적절한 package를 다운받아야 한다.

[Providers packages](https://airflow.apache.org/docs/#providers-packages-docs-apache-airflow-providers-index-html)에서
[apache-airflow-providers-apache-spark](https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/index.html)에 있는 모듈을 설치해야 한다.

## Dockerfile
```
FROM apache/airflow:2.7.0-python3.11

USER root # root 권한이 아니면 설치를 못함

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

USER airflow

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# requirements.txt 파일 복사 및 패키지 설치
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
```

## docker-compose.yaml
```
version: '3.8'
x-airflow-common:
  &airflow-common
  # build: .
  environment:
  ...
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ./app:/usr/local/spark/app

services:
  spark-master:
    image: bitnami/spark:latest
    user: root 
    hostname: spark
    environment:
        - SPARK_MODE=master
        - SPARK_RPC_AUTHENTICATION_ENABLED=no
        - SPARK_RPC_ENCRYPTION_ENABLED=no
        - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
        - SPARK_SSL_ENABLED=no
    volumes:
        - ./app:/usr/local/spark/app
        - ./resources:/usr/local/spark/resources
    ports:
        - "8088:8080"
        - "7077:7077"

  spark-worker:
    image: bitnami/spark:latest
    user: root
    environment:
        - SPARK_MODE=worker
        - SPARK_MASTER_URL=spark://spark:7077
        - SPARK_WORKER_MEMORY=4G
        - SPARK_WORKER_CORES=2
        - SPARK_RPC_AUTHENTICATION_ENABLED=no
        - SPARK_RPC_ENCRYPTION_ENABLED=no
        - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
        - SPARK_SSL_ENABLED=no
    volumes:
        - ./app:/usr/local/spark/app
        - ./resources:/usr/local/spark/resources
```
DAG는 SparkSubmitOperator를 통해 Spark에 작업을 넘긴다.
이때 Spark이 있는 폴더에 Airflow와 Spark이 동시에 접근할 수 있어야 한다.

# 실행
```
docker build . --tag airflow_extend:latest
docker compose up -d
```
Airflow 이미지를 extend하고 해당 이미지를 `docker-compose.yaml`에서 지정하여 사용한다.

# 자주 사용하는 명령어
```
docker ps

docker rm
docker rmi -f

docker build . --tag airflow_extend:latest
docker compose up -d
docker compose down

docker exec -it <container_name> bash

docker exec -it <spark_master_container_name> \
    spark-submit --master spark://spark:7077 \
    /usr/local/spark/app/script.py

docker system prune -a -f --volumes
```
