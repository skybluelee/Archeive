# 사용 이유
인스턴스에 `git clone`한 후에 특정 파일을 다시 git으로 `push`하는 경우,
vscode에서 아래와 같은 방법을 사용할 수 있다.

# 사용 방법
```
git config --global user.name "<user_name>"
git config --global user.email <email>
```
***
해당 결과는
```
$ git config --list --show-origin

file:/home/ubuntu/.gitconfig    user.name=<>
file:/home/ubuntu/.gitconfig    user.email=<>
```
위의 명령을 통해 제대로 실행된 것을 확인할 수 있다.
