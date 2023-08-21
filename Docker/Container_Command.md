# 컨테이너 시작
## 컨테이너 생성
```
docker create <image>
```
## 컨테이너 생성 및 시작
```
docker run <image>
```
## 컨테이너 시작
```
docker start <container>
```
# docker run 옵션
```
docker run \
        -i \ # 호스트의 표준 입력을 컨테이너와 연결
        -t \ # TTY 할당
        --rm \ # 컨테이너 실행 종료 후 자동 삭제
        -d \ # 백그라운드 모드로 실행
        --name hello-world \ # 컨테이너 이름 지정
        -p 80:80 \ # 호스트 - 컨테이너 포트 바인딩
        -v /opt/example:/example \ # 호스트 - 컨테이너 볼륨 바인딩
        skybluelee/hello-world:latest \ # 실행할 이미지 : 버전
        my-command # 컨테이너에서 실행할 명령어
```
# 컨테이너 상태 확인
## 실행중인 컨테이너 확인
```
docker ps
```
## 전체 컨테이너 확인
```
docker ps -a
```
## 컨테이너 상세 정보 확인
```
docker inspect <container>
```
# 컨테이너 상태 변경
## 컨테이너 일시중지
```
docker pause <container>
```
## 컨테이너 재개
```
docker unpause <container>
```
## 컨테이너 종료
```
docker stop <container>
```
## 컨테이너 강제 종료
```
docker stop <container>
```
## 모든 컨테이너 종료
```
docker stop $(docker ps -a -q)
```
## 컨테이너 삭제
```
docker rm <container>
```
## 컨테이너 강제 종료 후 삭제
```
docker rm -f <container>
```
## 컨테이너 실행 종료 후 자동 삭제
```
docker run --rm
```
## 중지된 모든 컨테이너 삭제
```
docker container prune
```
# 컨테이너 명령어
```
docker exec <container> <command>
```
## 컨테이너에 bash로 접속하기
```
docker exec -i -t my-nginx bash // my-nginx 컨테이너에 bash로 접속
```
## 컨테이너 환경변수 확인하기
```
docker exec my-nginx env
```
# 컨테이너 포트
```
docker run -p [HOST IP:PORT]:[CONTAINER PORT] <container>
```
## 포트 노출
```
docker run -d -p 80:80 nginx // nginx 컨테이너의 80번 포트를 호스트 모든 IP의 80번 포트와 연결하여 실행
```
```
docker run -d -p 127.0.0.1:80:80 nginx // nginx 컨테이너의 80번 포트를 호스트 127.0.0.1 IP의 80번 포트와 여결하여 사용
```
```
docker run -d -p 80 nginx // nginx 컨테이너의 80번 포트를 호스트의 사용 가능한 포트와 연결하여 사용
```
## expose, publish
```
docker run -d --expose 80 nginx // expose 옵션은 문서화 용도로만 사용
```
```
docker run -d -p 80 nginx // publish 옵션은 실제 포트를 바인딩
```
# 볼륨
container 내부에 생성된 파일은 container 종료시 파일도 삭제된다.

특정 application에 data를 쌓아야 하는 경우 등에서 volume 기능을 사용한다.
```
docker run -d \
            --name nginx
            -v /opt/html:/usr/share/nginx/html \
            nginx
// 호스트의 /opt/html 디렉토리를 nginx의 웹 루트 디렉토리로 마운트
```
## 볼륨 공유
```
docker run -d \
          -it \
          -v $(pwd)/html:/usr/share/nginx/html \
          --name web-volume \
          ubuntu:focal

docker run -d \
          --name fastcampus-nginx \
          --volumes-from web-volume \
          -p 80:80 \
          nginx
```
`web-volume`이라는 이름의 볼륨을 생성하고 `--volumes-from`을 사용하면 다른 컨테이너에서 생성된 볼륨을 공유할 수 있다.
## 읽기 전용 볼륨
```
docker run -d \
          -v $(pwd)/html:/usr/share/nginx/html:ro \
          -p 80:80 \
          --name ro-nginx \
          nginx
```
`ro`를 사용하여 read-only 상태로 볼륨을 마운트할 수 있다.
## 볼륨 제거
```
docker volume rm db
```
볼륨 제거 이전에 컨테이너를 먼저 제거해야 정상적으로 제거된다.
# 로그
```
docker logs <container>
```
## 마지막 로그
```
docker logs --tail 5 <container>
```
마지막 5개의 로그 확인
## 실시간 + timestamp
```
docker logs -t -f <container>
```
`-t`는 timestamp, `-f`는 실시간
