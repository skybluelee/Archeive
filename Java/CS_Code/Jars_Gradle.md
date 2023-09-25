# sourcepath, classpath
## sourcepath
컴파일하는 경우(`javac`) `-sourcepath`를 사용하여 경로를 지정한다. 

디렉토리가 아래와 같다면
```
project2
   |
 .idea
  src
   |
 cptest - Hello.java
        - Main.java
```
두 java 파일을 컴파일하기 위해 `$ javac cptest/Main.java` 명령을 실행해야 한다.

이때 실행 디렉토리는 java 프로젝트의 **기본 위치인 src**인데 만약 src가 아닌 project2에서 실행한다면(`$ javac src/cptest/Main.java`) 경로를 찾지 못해 오류가 발생한다.

이러한 경우 sourcepath 옵션을 사용하여 해결할 수 있다.
```
$ javac -sourcepath src src/cptest/Main.java
```
### 컴파일 경로 변경
```
project2
   |
 .idea
  src
   |
 cptest - Hello.java
        - Hello.class
        - Main.java
        - Main.class
```
경로를 지정하지 않으면 java 파일이 있는 장소에 컴파일된다.

`-d` 옵션을 사용하면 경로를 변경할 수 있다.

`$ javac -d compiled -sourcepath src src/cptest/Main.java`
```
project2
   |
 .idea
compiled - Hello.class
         - Main.class
  src
   |
 cptest - Hello.java
        - Main.java
```
## classpath
sourcepath의 내용과 동일하게 기본 위치 바깥에서는 경로를 찾지 못해 오류가 발생한다.

classpath 옵션을 사용하여 이를 해결할 수 있다.
`$ java -classpath compiled cptest/Main`

`$ java -cp compiled cptest/Main`

`-classpath`의 경우 `-cp`로 줄일 수 있다.
### 실행 경로가 다른 경우
해당 경로에 대해서만 실행하는데 만약 class 파일이 다른 경로에 있다면 경로를 찾지 못하고 오류가 발생한다.

`$ java -cp compiled;compiled/bin cptest/Main` 와 같이 경로를 지정할 수 있다.

경로는 `;`를 통해 구분하며 이 경우 compiled 폴더와 compiled/bin 폴더를 클래스 경로로 지정하고 있다.
# JAR
클래스파일, 메타데이터, 리소스 파일 등을 하나의 파일로 만들어 사용할 수 있게 해준다.
## build
해당 프로젝트에 우클릭 -> Build Module '<project_name>' 또는 위의 도구 창에서 Build -> Build Project 클릭하면

out 디렉토리에 빌드된 것을 확인할 수 있다.
## jar 파일 생성
`$ jar cf petshop.jar -C ./out/production/java-practice-jar/ com/petshop/` 명령을 실행하면 프로젝트 딜게토리에 petshop.jar 파일이 생성된다.

위 코드의 옵션은 아래와 같다.
- `c` : JAR 파일 생성
- `f` : 생성할 파일의 이름 지정
- `-C` : 명령어를 실행할 디렉토리 수정 - 패키지가 아닌 위치에서 명령을 실행할 때 사용
- `jar cf {jar 파일명} -C {명령어 실행 디렉토리} {포함할 디렉토리}`
### intelliJ를 사용한 jar 파일 생성
File -> Project Structure -> Artifacts -> Add(+버튼 클릭) -> JAR -> from Modules with Dependencies

Build -> Build artifacts -> Action(Build)

위 과정을 거쳐 jar 파일을 생성할 수 있다.
## jar 내용 확인
`$ jar tf <jar_file_name>`를 통해 내용을 확인한다.

```
$ jar tf petshop.jar

META-INF/
META-INF/MANIFEST.MF
com/petshop/
com/petshop/Cat.class
com/petshop/Dog.class
com/petshop/Main.class
com/petshop/Pet.class
```
패키지 내의 클래스 파일이 jar 파일 안에 존재한다.
## 압축풀기
`$ jar xf <jar_file_name>`를 통해 압축을 풀 수 있다.

`$ jar xf petshop.jar`을 사용하여 압축을 풀면 해당 파일을 확인할 수 있다.
## 다른 프로젝트에 적용
File -> Project Structure -> Module -> Dependencies -> Add(+버튼 클릭) -> 1 JARs or Directories... -> jar 파일 선택

의 과정을 통해 jar 파일을 가져온다.
# 빌드 도구
## 설정
Maven의 경우 New Project에서 Build System을 Maven을 선택하고 프로젝트를 생성한다.

Gradle의 경우 New Project에서 Build System을 Gradle을, DSL을 Groovy를 선택하고 프로젝트를 생성한다.

Maven은 pom.xml 파일에서 Gradle은 build.gradle 파일에서 설정을 변경할 수 있다.
## Gradle
intelliJ의 우측 코끼리 모양(마우스를 올리면 gradle이라 나옴)을 클릭하면 gradle UI를 확인할 수 있다.

Task 내부에 여러 작업이 존재하는데, 예를 들어 build를 더블 클릭하면 java 파일이 컴파일 되고, clean을 더블 클릭하면 컴파일 결과가 없어진다. jar를 더블 클릭하여 jar 파일을 생성하는 등의 gradle 작업을 UI를 통해 진행할 수 있다.
### 외부 라이브러리 가져오기
MVN Repository에서 임의의 라이브러리[https://mvnrepository.com/artifact/com.semanticcms/semanticcms-changelog-taglib/1.7.1](SemanticCMS Changelog Taglib)를 가져오고 싶다면 Gradle이나 Gradle (Short)를 복사하고,
build.gradle 파일의 dependencies에 붙여넣고 Gradle UI에서 새로고침을 클릭하면 외부 라이브러리를 가져올 수 있다.
