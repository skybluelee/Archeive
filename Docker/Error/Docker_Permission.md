# 문제
```
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json": dial unix /var/run/docker.sock: connect: permission denied
```
해당 문제는 도커에서는 기본적으로 root 사용자에게만 권한을 주기 때문에 발생한다.
# 해결방법 - 1
```
sudo chmod 666 /var/run/docker.sock
```
임시적인 해결 방법으로 도커나 인스턴스 재실행할 때마다 반복해야 한다.
# 해결방법 - 2 
```
sudo groupadd docker
```
docker 그룹은 도커 설치시 자동으로 추가된다.

만약 해당 그룹이 없다면 위 명령어 실행.

그룹은 `cat /etc/group`에서 확인할 수 있다.
```
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```
## 해결 X
```
reboot
```
reboot 명령어 실행.
