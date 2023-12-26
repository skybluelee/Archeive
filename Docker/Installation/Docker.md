본 문서는 Docker를 설치하는 방법에 대한 설명으로 [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)를 해석한 내용이다.

# OS requirements
Docker를 설치하기 위해서는 64비트의 우분투 버젼이 필요하다.

- Ubuntu Mantic 23.10
- Ubuntu Lunar 23.04
- Ubuntu Jammy 22.04 (LTS)
- Ubuntu Focal 20.04 (LTS)

우분투에서 사용하는 도커 엔진은 x86_64 (or amd64), armhf, arm64, s390x, 그리고 ppc64le (ppc64el) 구조와 호환 가능하다.

# 오래된 버전 제거
도커 엔진을 설치하기 전에 충돌 방지를 위해 특정 패키지를 제거해야 한다.

배포자 유지보수자들은 APT에서 도커 패키지의 비공식 배포판을 제공한다. 도커 엔진의 공식 버전을 설치하기 전에 이러한 패키지들을 반드시 제거해야 한다.

제거 패키지 목록:
- docker.io
- docker-compose
- docker-compose-v2
- docker-doc
- podman-docker

게다가 도커 엔진은 `containerd`와 `runc`에 의존성을 갖는다.
도커 엔진은 이 의존성을 하나의 번들 `containerd.io`로 묶어 사용한다.
기존에 `containerd` 혹은 `runc`를 설치했다면 충돌 방지를 위해 삭제하라.

패키지 삭제 명령은 아래와 같다.
```
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get`를 사용하여 해당 패키지가 삭제할 수 있다.

`/var/lib/docker/`에 저장된 이미지, 컨테이너, 볼륨, 네트워크는 도커를 해제할 때 자동으로 삭제되지 않는다.
처음부터 설치하기를 원한다면 아래의 Uninstall Docker Engine를 참조하라.

# Installation methods
원하는 여러 가지 방식으로 도커를 설치할 수 있다.

- [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)사용하기. 가장 초기의 그리고 가장 빠른 설치 방법이다.
- Docker's apt repository에서 설치하는 방법으로 아래에서 확인하라.
- 수동으로 설치하고 수동으로 업데이트하기.
- convenience script 사용하기. 시험용, 개발용 환경에서만 사용하는 것을 추천한다.

## Install using the apt repository
도커를 새 머신에 설치하기 전에 도커 리포지토리를 설정할 필요가 있다.
그 후에 리포지토리에서 도커를 설치하고 업데이트한다.

1. Set up Docker's apt repository
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
> 주의: 만약 우분투 derivative distro(Linux Mint와 같은)를 사용한다면, `VERSION_CODENAME` 대신에 `UBUNTU_CODENAME`를 사용해야 한다.

2. Install the Docker packages.
**가장 최신의 버전 설치**
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
***
**특정 버전 설치**

특정 버전을 설치하기 위해서는 사용 가능한 버전의 목록을 먼저 확인하고 시작하라.
```
# List the available versions:
apt-cache madison docker-ce | awk '{ print $3 }'

5:24.0.0-1~ubuntu.22.04~jammy
5:23.0.6-1~ubuntu.22.04~jammy
...
```
원하는 버전을 확인하고 설치하라.
```
VERSION_STRING=5:24.0.0-1~ubuntu.22.04~jammy
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```
3. `hello-world` 이미지를 사용하여 도커가 제대로 설치되었는지 확인하라.
```
sudo docker run hello-world
```
이 명령은 테스트 이미지를 다운로드하고 컨테이너에서 해당 이미지를 실행한다.
컨테이너가 동작한다면 확인 메시지를 출력하고 종료된다.

> 팁: 루트 없이 실행하려고 할 때 오류가 발생하는가?
도커 사용자 그룹은 존재하지만 사용자가 없어서 도커 명령어를 실행하기 위해 `sudo`를 사용해야 한다.
> Linux 포스트 설치로 계속 진행하여 비권한 사용자가 도커 명령어를 실행하도록 하고, 기타 선택적인 구성 단계를 진행하세요
