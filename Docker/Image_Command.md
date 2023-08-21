# 이미지 확인
```
docker images
```
# Dockerfile
[공식 문서](https://docs.docker.com/engine/reference/builder)
## 이미지 생성
```
// Dockerfile
FROM node:12-alpine
RUN apk add --no-cache python3 g++ make
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```
```
//Dockerfile이 존재하는 위치에서 아래 코드 실행
docker build -t my-app:v1 ./
```
해당 위치에서 Dockerfile을 찾아 `my-app:v1`이라는 이미지가 생성된다.
## FROM
```
FROM [--platform=<platform>] <image> [AS <name>]
OR
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
OR
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```
`FROM`은 빌드를 처음으로 실행하고 이후 지시문을 실행하는 기초 이미지를 설정한다. 따라서 유효한 Dockerfile은 반드시 `FROM` 지시문으로 시작해야 한다. 
- `ARG`는 Dockerfile에서 `FROM` 앞에 올 수 있는 유일한 지시문이다.
- `FROM`은 여러 개의 이미지를 생성하거나 다른 이미지에 대한 의존성을 만족하기 위해 하나의 Dockerfile 안에서 여러번 등장할 수 있다. 새로운 `FROM`이 나오기 전에 이미지 아이디로 명시할 수 있다. 각 `FROM`은 이전 지시문에 의한 상태를 초기화한다.
- `AS NAME`을 사용하여 `FROM` 지시문에서 이름을 적용할 수 있다. 이름은 추후`FROM and COPY --from=<name>`를 통해서도 생성할 수 있다.
- `tag` 또는 `digest`값은 옵션이다. 만약 둘 중 하나를 제외한다면, 빌더는 디폴트로 `latest` 태그를 선정한다. 빌더는 만약 `tag`값을 찾지 못한다면 오류를 발생한다.
### ARG
```
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```
`FROM` 이전에 선언된 `ARG`는 빌드 단계 바깥에 있기 때문에, `FROM` 이후에는 사용 불가능하다. 
```
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```
`ARG`를 사용하는 가장 기본적인 방법은 빌드 단계 이전에 사용하는 것이다.
## RUN
```
RUN <command> // 리눅스나 cdm에서 쉘로 운영할 때
RUN ["executable", "param1", "param2"] (exec form)
```
2가지 방식이 있다.

`RUN` 지시문은 현재 이미지의 새로운 층에 명령을 수행하고 결과를 커밋한다. 커밋한 결과의 이미지는 Dockerfile의 다음 부분에서 사용된다.

```
RUN ["/bin/bash", "-c", "echo hello"]
```
`exec` 형식은 쉘 문자열 처리 없이, 쉘 실행 파일(ex. bin/bash)을 포함하지 않은 기본 이미지를 사용하여 `RUN` 명령을 실행하게 만들어 준다.

디폴트 쉘은 `SHELL` 명령어를 사용하여 변경 가능하다.
```
RUN /bin/bash -c 'source $HOME/.bashrc && \
echo $HOME'

RUN /bin/bash -c 'source $HOME/.bashrc && echo $HOME'
```
\(백슬래쉬) 사용 가능하다.
## CMD
`CMD`는 세가지 형식이 존재한다.
```
CMD ["executable","param1","param2"] (exec form, 가장 많이 사용)
CMD ["param1","param2"] (ENTRYPOINT 사용시 디폴트 값)
CMD command param1 param2 (shell form)
```
Dockerfile에 `CMD`는 오직 하나만 존재한다. 만약 여러개를 사용한다면 마지막 `CMD`만 실행된다.

`CMD`의 주 목적은 실행중인 컨테이너에 디폴트 값을 전달하기 위함이다. 이 디폴트 값은 실행 파일을 포함하거나, 생략할 수 있는데, 생략하는 경우 `ENTRYPOINT`를 명시해야 한다.

만약 `CMD`가 `ENTRYPOINT` 지시문에 디폴트 인수(arguments)를 사용한다면, `CMD`, `ENTRYPOINT` 모두 JSON 형식으로 명시되어야 한다.

`shell` 형식과 달리 `exec` 형식은 명령 shell을 사용하지 않으므로 일반적인 쉘 처리가 발생되지 않는다. 예를 들어 `CMD ["echo", "$HOME"]`에서 `$HOME`에 대해 변수 치환(variable substitution)을 실행하지 않는다.
만약 쉘 처리를 하고자 한다면, 쉘 형식을 사용하거나 직접 쉘을 실행해야 한다(`CMD [ "sh", "-c", "echo $HOME" ]`).


`exec` 형식을 사용하고 쉘을 직접 실행할 때, 쉘 형식과 마찬가지로 환경 변수 확장(environment variable expansion)을 수행하는 것은 Docker가 아니라 실행되는 쉘(shell) 자체이다.
```
FROM ubuntu
CMD ["/usr/bin/wc","--help"]
```
만약 쉘 없이 명령을 수행하고자 한다면, 반드시 JSON 형태로 실행 프로그램의 전체 경로를 지정해야 한다.
## LABEL
```
LABEL <key>=<value> <key>=<value> <key>=<value> ...

LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```
`LABEL`은 이미지에 메타데이터를 추가하는 지시문이다. `LABEL`은 key-value 쌍이다.
## EXPOSE
```
EXPOSE <port> [<port>/<protocol>...]
```
`EXPOSE` 지시문은 Docker에게 컨테이너가 작동하는 동안 특정 네트워크 포트를 listen하는 것을 알려준다. 포트가 TCP 또는 UDP 중 어떤 것을 listen할 지 지정할 수 있고 디폴트는 TCP이다.

`EXPOSE` 지시문은 실제로 포트를 개설하지는 않는다. `EXPOSE`는 이미지를 빌드하는 사람과 컨테이너를 운영하는 사람들 간의 '어떤 포트를 개설하겠다'라는 문서 역할을 한다.
실제로 운영중인 컨테이너에 특정 포트를 개설하기 위해서는 `-p` 플래그를 사용하거나, `-P`를 사용하여모든 포트에 노출시킬 수 있다.
```
EXPOSE 80/udp
```
TCP가 기본값이고 위와 같이 UDP를 지정할 수 있다.

TCP, UDP 모두 지정하는 경우, `-P`를 사용하면 포트가 TCP에 1번, UDP에 1번 노출될 것이다.

"-P" 옵션을 사용할 때, 호스트에서는 일시적이고 고차원의(ephemeral high-ordered, 일반적으로 32768부터 61000까지) 호스트 포트를 사용하므로, TCP와 UDP의 포트 번호가 동일하지 않다.
## ENV
```
ENV <key>=<value> ...
```
`ENV` 지시문은 환경변수 key를 value로 설정한다. 이 값은 이미지를 빌드하는 과정에서 사용되며 인라인(한 줄 작성)으로 교체 가능하다.

값은 다른 환경 변수로도 전송되며, 따옴표를 사용한 문자열은 탈출(escape)되지 못하면 제거된다.
```
ENV MY_NAME="John Doe"
ENV MY_DOG=Rex\ The\ Dog
ENV MY_CAT=fluffy
```

`ENV`를 사용한 환경 변수는 이미지를 실행중인 컨테이너에서 유지되며 `docker inspect` 명령어를 통해 확인 가능하고 `docker run --env <key>-<value>`명령을 통해 바꿀 수 있다.

`ENV`를 통한 환경 변수는 상속된다.

`ENV`의 사용은 단점 또한 존재한다. 예를 들어 `ENV DEBIAN_FRONTEND=noninteractive` 설정은 `apt-get`를 사용해야만 변경이 가능한데, 이미지 사용자에게 혼란을 줄 수 있다.
```
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y ...

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ...
```
만약 환경 변수가 빌드하는 동안에만 필요하고 이미지에는 필요하지 않다면 위와 같이 사용할 수 있다.
## ADD
```
ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>
ADD [--chown=<user>:<group>] [--chmod=<perms>] ["<src>",... "<dest>"]
```
`ADD`는 2가지 형식이 존재한다.

후자는 공백을 포함하는 경로가 필요하다.

`ADD` 지시문은 새 파일, 디렉토리나 URL을 `<src>`에서 복사하고, 경로 `<dest>`의 이미지 파일 시스템에 추가한다.

여러 `<src>` 리소스는 특정될 수 있지만, 만약 리소스가 파일이거나 디렉토리라면, 경로는 빌드하는 공간의 상대 경로로 표시된다.

```
ADD hom* /mydir/
```
`hom`으로 시작하는 모든 파일을 /mydir로 복사한다.

`<dest>`는 절대 경로이거나 `WORKDIR`의 상대경로이며, `<src>`는 `<dest>` 컨테이너 내부로 복사된다.

```
ADD arr[[]0].txt /mydir/
```
만약 특수문자가 포함된 파일이나 디렉토리를 복사하고자 한다면, Golang 규칙을 적용하여 탈출하애 한다.
예를 들어 파일이 `arr[0].text`라면 위와 같이 작성해야 한다.

```
ADD --chown=55:mygroup files* /somedir/
ADD --chown=bin files* /somedir/
ADD --chown=1 files* /somedir/
ADD --chown=10:11 files* /somedir/
ADD --chown=myuser:mygroup --chmod=655 files* /somedir/
```
`--chown` 플래그를 사용하여 사용자 이름, 그룹 이름, UID/GID 조합 등을 지정하지 않는다면 모든 새 파일과 디렉토리는 UID/GID가 0부터 생성된다.

그룹 이름이나 UID 혹은 GID 없이 사용자 이름만 지정하는 경우 동일한 UID, GID를 얻게 된다.

만약 사용자 이름 또는 그룹 이름이 주어진다면, 컨테이너의 root 파일 시스템 `/etc/passwd`와 `/etc/group` 파일은 이름을 UID, GID로 바꾸기 위해 사용될 것이다.

만약 컨테이나 루트 파일 시스템이 `/etc/passwd`와 `/etc/group`를 포함하지 않고, 사용자 혹은 그룹 이름이 `--chown` 플래그를 사용중이라면, 빌드는 `ADD` 라인에서 실패할 것이다.

`ADD`는 아래 규칙을 따른다.
- `<src>` 경로는 반드시 빌드하는 문서 내부에 존재해야 한다.
- 만약 `<src>`가 URL이고 `<dest>`가 트레일링 슬래쉬(디렉토리에서 마지막에 나오는 `/`)로 끝나지 않는다면, 파일이 URL에서 다운받아지고 `<dest>`로 복사된다.
- 만약 `<src>`가 URL이고 `<dest>`가 트레일링 슬래쉬로 끝난다면, 파일 이름은 URL을 참조하고 파일이 `<dest>/<filename>` 경로로 다운된다.
- 만약 `<src>`가 디렉토리라면, 해당 디렉토리의 메타데이터를 포함한 모든 파일이 복사된다.
- 만약 `<src>`가 `.zip, .tar.gz, .tar.bz2, .tar, .tgz` 등의 압축 파일이라면, 압축 해제된어 디렉토리가 생성된다.
- 만약 `<src>`가 파일이라면, 메타데이터를 따라 각각 복사된다. 이 경우 만약 `<dest>`가 트레일링 슬래쉬로 끝난다면, 디렉토리와 `<src>`의 파일이 `<dest>/base(<src>)`에 저장된다.
- 만약 복수의 `<src>`가 특정되면, `<dest>`는 디렉토리여야 하며, 트레일링 슬래쉬로 끝나야 한다.
- 만약 `<dest>`가 트레일링 슬래쉬로 끝나지 않는다면, 파일로 간주되고 `<src>`는 `<dest>`로 작성된다.
- 먄약 `<dest>`가 존재하지 않는다면, 해당 경로에 있는 모든 누락된 디렉토리와 함께 <dest>가 생성된다.
## COPY
```
COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>
COPY [--chown=<user>:<group>] [--chmod=<perms>] ["<src>",... "<dest>"]
```
`COPY`는 2가지 형식이 존재한다.
