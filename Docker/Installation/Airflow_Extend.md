# Extend Library
크롤링을 위해 selenium과 webdriver_manager를 extend했다.

해당 모듈은 PythonOperator에서 사용한다.

# 셀레니움 이미지 다운로드
Airflow에서 selenium을 사용하기 위해서는 selenium 이미지를 Airflow의 Dockerfile에서 지정해야 한다.

[docker hub](https://hub.docker.com/r/selenium/standalone-chrome)에서 selenium 이미지를 사용하는 방법을 확인할 수 있다.
```
docker pull selenium/standalone-chrome
```

```
$ docker images
REPOSITORY                   TAG       IMAGE ID       CREATED      SIZE
selenium/standalone-chrome   latest    fe7a24405507   7 days ago   1.22GB
```

# `requirements.txt` 작성하기
```
vi requirements.txt

selenium
webdriver_manager
```
`<module_name>==<version>` 형식으로 원하는 버전을 지정할 수 있다.

위의 경우 가장 최신 버전을 사용한다.

# Airflow용 `docker-compose.yaml` 파일 다운로드
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```

# `docker-compose.yaml` 파일 수정하기
## **이미지 이름 변경**
```
x-airflow-common:
  &airflow-common
  # 기존 이미지
  # image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.8.0}
  image: ${AIRFLOW_IMAGE_NAME:--extend_airflow:latest}
```
사용할 이미지로 변경한다.

`extend_airflow:latest`는 이후 빌드할 이미지와 태그이다.

## **예제 삭제**
```
  environment:
    ...
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```
디폴트값은 `'true'`이며 이 상태로 진행하는 경우 기본 예제가 매우 많이 존재하기에 `'false'`로 변경한다.

## **셀레니움 추가**
```
services:
  selenium:
    container_name: remote_chromedriver
    image: selenium/standalone-chrome:latest
    ports:
      - 4444:4444
    restart: always
```
다운받은 이미지를 Airflow의 서비스에 추가한다.

`remote_chromedriver`는 이후 PythonOperator에서 사용된다.

## **최종**
```
...
x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider packages you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-extend_airflow:latest}
  environment:
    ...
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    ...
...
service:
  selenium:
    container_name: remote_chromedriver
    image: selenium/standalone-chrome:latest
    ports:
      - 4444:4444
    restart: always
...
```

# Airflow 이미지 빌드
```
docker build . --tag extend_airflow:latest
```
```
$ docker images
REPOSITORY                   TAG       IMAGE ID       CREATED         SIZE
extend_airflow               latest    a4fc7c18b870   4 seconds ago   1.47GB
selenium/standalone-chrome   latest    fe7a24405507   7 days ago      1.22GB
```

# Airflow 실행
```
docker compose up -d
```
```
$ docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS                            PORTS                                                 NAMES
004f75b53463   extend_airflow:latest               "/usr/bin/dumb-init …"   40 seconds ago   Up 5 seconds (health: starting)   8080/tcp                                              airflow-airflow-triggerer-1
05c8a56b41ee   extend_airflow:latest               "/usr/bin/dumb-init …"   40 seconds ago   Up 5 seconds (health: starting)   8080/tcp                                              airflow-airflow-worker-1
fc3cd0424f4a   extend_airflow:latest               "/usr/bin/dumb-init …"   40 seconds ago   Up 5 seconds (health: starting)   8080/tcp                                              airflow-airflow-scheduler-1
a4b4a71aa411   extend_airflow:latest               "/usr/bin/dumb-init …"   40 seconds ago   Up 5 seconds (health: starting)   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp             airflow-airflow-webserver-1
45fdc1898c72   redis:latest                        "docker-entrypoint.s…"   40 seconds ago   Up 38 seconds (healthy)           6379/tcp                                              airflow-redis-1
f5e52d58023a   selenium/standalone-chrome:latest   "/opt/bin/entry_poin…"   40 seconds ago   Up 38 seconds                     0.0.0.0:4444->4444/tcp, :::4444->4444/tcp, 5900/tcp   remote_chromedriver
6e21f894d6e1   postgres:13                         "docker-entrypoint.s…"   40 seconds ago   Up 39 seconds (healthy)           5432/tcp                                              airflow-postgres-1
```
```
$ ls
Dockerfile  config  dags  docker-compose.yaml  logs  plugins  requirements.txt
```
기존의 docker-compose.yaml, requirements.txt, Dockerfile 이외에 config, dags, logs, plugins 디렉토리가 추가되었다.
# 보안 규칙 추가
Airflow의 포트는 8080으로 보안 그룹의 인바운드 규칙에 8080 포트를 추가한다.
