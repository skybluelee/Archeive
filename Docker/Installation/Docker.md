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

> 팁:
>
> 루트 없이 실행하려고 할 때 오류가 발생하는가?
> 
> 도커 사용자 그룹은 존재하지만 사용자가 없어서 도커 명령어를 실행하기 위해 `sudo`를 사용해야 한다.
> [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall)로 계속 진행하여 비권한 사용자가 도커 명령어를 실행하도록 하고, 선택적인 구성을 설정하라.

### Upgrade Docker Engine
도커를 업그레이드하기 위해서는 위의 특정 버전을 가장 최신 버전으로 설정하고 실행하면 된다.

## Install from a package
도커의 `apt` 레포지토리를 사용하여 도커를 설치할 수 없는 경우, `deb` 파일을 다운하고 도커를 수동으로 설치할 수 있다.
도커 업그레이드가 필요한 경우 새로운 파일을 다운받으면 된다.

1. (https://download.docker.com/linux/ubuntu/dists/)를 방문하라.
2. 리스트 내에서 우분투 버전을 선택하라.
3. `pool/stable/`로 가서 적용가능한 구조(amd64, armhf, arm64, or s390x)를 선택하라.
4. 도커 엔진, CLI, containerd, and Docker Compose packages에 해당하는 `deb`파일을 다운받아라.
- `containerd.io_<version>_<arch>.deb`
- `docker-ce_<version>_<arch>.deb`
- `docker-ce-cli_<version>_<arch>.deb`
- `docker-buildx-plugin_<version>_<arch>.deb`
- `docker-compose-plugin_<version>_<arch>.deb`
5. `.deb` 패키지를 설치하라. 도커 패키지를 다운로드한 디렉토리로 경로를 업데이트하라.
```
sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
  ./docker-ce_<version>_<arch>.deb \
  ./docker-ce-cli_<version>_<arch>.deb \
  ./docker-buildx-plugin_<version>_<arch>.deb \
  ./docker-compose-plugin_<version>_<arch>.deb
```
6. `hello-world` 이미지를 사용하여 제대로 설치되었는지 확인하라.
```
sudo service docker start
sudo docker run hello-world
```
## Install using the convenience script
도커는 개발 환경에 대화식이 아닌 방식으로 도커를 설치하기 위한 편의 스크립트(convenience script)를 [https://get.docker.com/](https://get.docker.com/?_gl=1*1r0an3*_ga*NDI1NjAyMjQ2LjE2ODE3MjE1MDY.*_ga_XJWPQMJYHQ*MTcwMzU2ODc4NS4zNi4xLjE3MDM1NzE1OTYuNjAuMC4w)에서 제공한다.
편의 스크립트는 프로덕션 환경에는 권장되지 않지만, 필요에 맞게 프로비저닝 스크립트를 생성하는 데 유용하다.
또한 [패키지 저장소를 사용하여 설치하는 설치 단계](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)에 대해 알아보기 위해 저장소를 사용하는 설치 방법을 참조하라. 
이 스크립트의 소스 코드는 오픈 소스이며, [GitHub의 docker-install 저장소](https://github.com/docker/docker-install)에서 찾을 수 있다.

인터넷에서 다운로드한 스크립트를 로컬에서 실행하기 전에 항상 그 스크립트를 확인하라. 설치 전에 편의 스크립트의 잠재적인 위험과 제한 사항을 알아보는 것이 좋다.
- 스크립트는 `root` 또는 `sudo` 권한을 요구한다.
- 스크립트는 Linux 배포판과 버전을 감지하고 패키지 관리 시스템을 자동으로 구성하려고 시도한다.
- 스크립트는 대부분의 설치 매개변수를 사용자 정의할 수 있게 허용하지 않는다.
- 스크립트는 확인을 요청하지 않고 종속성 및 권장 사항을 설치한다. 이로 인해 호스트 머신의 현재 구성에 따라 많은 수의 패키지가 설치될 수 있다.
- 기본적으로 스크립트는 Docker, containerd, runc의 최신 안정적인 버전을 설치한다. 이 스크립트를 사용하여 기계를 프로비저닝할 때, 이로 인해 Docker의 예상치 않은 주요 버전 업그레이드가 발생할 수 있다. 제품 시스템에 배포하기 전에 항상 테스트 환경에서 업그레이드를 테스트하라.
- 스크립트는 기존의 Docker 설치를 업그레이드하는 데 설계되지 않았다. 스크립트를 사용하여 기존 설치를 업데이트할 때, 종속성이 예상한 버전으로 업데이트되지 않을 수 있어 오래된 버전이 설치될 수 있다.
***
아래 예시는 (https://get.docker.com/)에서 스크립트를 다운로드하고 최신의 stable 버전의 도커를 설치하는 예시이다.
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```
이제 도커 엔진을 성공적으로 설치하고 시작했을 것이다.
도커 서비스는 `Debian` 기반의 배포판에서는 자동으로 시작된다. CentOS, Fedora, RHEL 또는 SLES와 같은 RPM 기반의 배포판에서는 적절한 `systemctl` 또는 service 명령어를 사용하여 수동으로 시작해야 한다.
메시지가 나타내는대로, 기본적으로 권한 없는 사용자는 도커 명령을 실행할 수 없다.

### Install pre-releases
도커는 Linux에 도커의 사전 릴리스를 설치하기 위한 편의 스크립트도 (https://test.docker.com/) 에서 제공한다. 
이 스크립트는 get.docker.com의 스크립트와 동일하지만, 패키지 관리자를 도커 패키지 저장소의 테스트 채널을 사용하도록 설정한다.
테스트 채널에는 도커의 안정된 버전과 사전 릴리스(베타 버전, 릴리스 후보)가 모두 포함되어 있다. 
이 스크립트를 사용하여 새 릴리스에 빠르게 접근하고, stable 버전으로 출시되기 전에 테스트 환경에서 그것들을 사용하라.

Linux의 테스트 채널에서 도커의 최신 버전을 설치하려면 다음을 실행하라.
```
curl -fsSL https://test.docker.com -o test-docker.sh
sudo sh test-docker.sh
```

### Upgrade Docker after using the convenience script
