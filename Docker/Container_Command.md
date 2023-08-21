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
