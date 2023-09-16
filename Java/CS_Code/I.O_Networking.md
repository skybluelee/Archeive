# Path
```
public class Main {
    public static final String CUR_PATH = "src/sec12/chap02/";
    public static void main(String[] args) {
        Path path1 = Paths.get("");
        Path path1Abs = path1.toAbsolutePath();     // path1Abs: "D:\Java_Project\project1"
        String path1Abs_str = path1Abs.toString();  // path1Abs_str: "D:\Java_Project\project1"

        Path path2 = Paths.get("my_file.txt");      // path2: "my_file.txt"
        Path path2Abs = path2.toAbsolutePath();     // path1Abs_str: "D:\Java_Project\project1\my_file.txt"

        Path path3 = Paths.get(CUR_PATH, "sub1", "sub2", "sub3");  // path3: "src\sec12\chap02\sub1\sub2\sub3"

        Path path4 = path3.resolve(path2);  // path4: "src\sec12\chap02\sub1\sub2\sub3\my_file.txt"

        Path path5 = path4.getParent();  // path5: "src\sec12\chap02\sub1\sub2\sub3"

        Path path6 = path4.relativize(path2); // path6: "..\..\..\..\..\..\..\my_file.txt"

        Path path7 = path4.getFileName(); // path7: "my_file.txt"

        Path path8 = path4.subpath(3, 5); // path: "sub1\sub2"
    }
}
```
`get()`에 빈 문자열을 인자로 주고, `toAbsolutePath()` 메소드를 사용하면 프로젝트의 절대 경로를 가져온다. 이때 불러온 `path1Abs`은 문자열이 아닌 Path 객체로, 문자열 형태로 받기 위해서는 `toString` 메소드를 사용해야 한다.

`get()`에 문자열 인자를 주고, `toAbsolutePath()` 메소드를 사용하면 절대경로 + <인자> 형태가 된다.

`get()`에 문자열 여러개를 인자로 주면 `,`를 디렉토리로 간주하여 경로를 반환한다.

`a.resolve(b)`는 `a\b` 형식으로 경로를 통합한다.

`getParent()`는 부모 경로를 반환한다.

`a.relativize(b)`는 a에 대한 b의 상대 경로를 반환한다.

`getFileName()`은 제일 마지막 경로나 파일 이름을 반환한다.

`subpath(a,b)`는 a번째 디렉토리부터 b까지의 디렉토리를 반환한다.
# Files
```
public class Main {
    public static final String CUR_PATH = "src/sec12/chap02/";
    public static void main(String[] args) {
        System.out.println(Files.exists(path2)); // false
        try {
            Files.createFile(path2);
        } catch (IOException e) {}

        System.out.println(Files.exists(path2)); // true

        try {
            Files.createDirectory(
                    Paths.get(CUR_PATH, "myFolder")
            );
        } catch (IOException e) {}

        try {
            // getBytes : 문자열로부터, 주어진 인코딩 형식에 따라 바이트 배열로 반환
            Files.write(path4, "안녕하세요".getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {}
    }
}
```
`createFile()` 메소드는 경로가 존재하는 경우 해당 경로에 파일을 생성하고, 파일명만 존재하는 경우 프로젝트 경로에 파일을 생성한다.

`createDirectory` 해당 경로에 디렉토리를 생성한다.

`write` 메소드는 해당 경로에 있는 파일에 내용을 작성한다. `write`는 덮어쓰기만 사용하므로 기존 내용에 추가되거나 하지 않는다.
```
public class Main {
    public static void main(String[] args) {
        byte[] path4Bytes;
        try {
            path4Bytes = Files.readAllBytes(path4); // path4Bytes: [-20, -107, ...]
        } catch (IOException e) {}
        String path4Contents = new String(path4Bytes); // path4Contents: "hello"

        List<String> path4Read = null;
        try {
            path4Read = Files.readAllLines(path4);
            path4Read.stream()
                     .forEach(System.out::println);
        } catch (IOException e) {}


        try (Stream<String> lineStrm = Files.lines(path4)) {
            lineStrm
                    //.limit(3) // 필요에 따라 설정
                    .forEach(System.out::println);
        } catch (IOException e) {}
    }
}
```
파일의 내용을 읽어오는 방법으로는 `readAllBytes`, `readAllLines`, `lines`가 있다.

`readAllBytes` 메소드는 byte로 읽어온 후 문자열로 형 변환해야 한다

`readAllLines`는 각 라인을 읽어 리스트에 저장한다.

`readAllBytes`와 `readAllLines`는 대용량 파일에는 적절하지 않다.

`lines`는 스트림으로 받아오고, 대용량 파일을 읽는데 적합하다.
```
public class Main {
    public static void main(String[] args) {
        // copy
        Path copied = Paths.get(
                path4.getParent().toString(), "copied.txt"
        );        
        try {
            Files.copy(path4, copied);
        } catch (IOException e) {}
        // move
        Path moved = Paths.get(
                path4.getParent().getParent().toString(),
                "moved.txt"
        );
        try {
            Files.move(copied, moved);
        } catch (IOException e) {}
        // delete
        try {
            Files.delete(moved);
        } catch (IOException e) {}
    }	
}
```
`copy(a, b)` 메소드는 a의 내용을 b로 복사하고, `move(a, b)` 메소드는 a를 b로 이동한다.

`copy`와 `move` 메소드는 b에 해당하는 디렉토리와 파일을 먼저 생성해야 한다.

`delete` 메소드의 경우 인자로 주어진 파일을 삭제한다.
