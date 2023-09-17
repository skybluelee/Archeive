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
# I/O Stream
## FileInputStream, read
```
public class Main {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static void main(String[] args) {
        var fis1 = measureTime(Main::fileInputStrmEx1);
    }

    public static void fileInputStrmEx1 () {
        try (FileInputStream fis = new FileInputStream(SONG_PATH)) {
            int readByte;
            // while문 내에서 readByte를 초기화 함
            while ((readByte = fis.read()) != -1) {
                // 숫자를 문자형으로 명시적 변환
                char readChar = (char) readByte;

                System.out.print(readChar);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String measureTime (Runnable runnable) {
        long startTime = System.nanoTime();
        runnable.run();
        long endTime = System.nanoTime();
        return String.valueOf("%,d nano sec")
                .formatted(endTime - startTime);
    }
}

Yesterday, all my troubles seemed so far away
ìì ì, ëì ëª¨ë  ìë¦ë¤ì´ ë©ë¦¬ ì¬ë¼ì ¸ ë²ë¦° ë¯ íëë°

...
```
`FileInputStream` 클래스는 파일로부터 데이터를 받아오는데 사용한다.

`read` 메소드는 해당 파일을 1바이트씩 읽어온다. 따라서 데이터 양이 많은 경우 성능 저하 문제로 사용하지 않는 것이 좋다.

위 경우 한글 인코딩 설정을 진행하지 않아 값이 깨져서 나왔다.
## InputStreamReader
```
public class Main {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static void main(String[] args) {
        var fis2 = measureTime(Main::fileInputStrmEx2);
    }

    public static void fileInputStrmEx2 () {
        // 인코딩 설정 - UTF-8
        Charset charset = StandardCharsets.UTF_8;

        try (
                FileInputStream fis = new FileInputStream(SONG_PATH);
                InputStreamReader isr = new InputStreamReader(fis, charset)
        ) {
            int readByte;
            while ((readByte = isr.read()) != -1) {
                char readChar = (char) readByte;
                System.out.print(readChar);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

Yesterday, all my troubles seemed so far away
예전엔, 나의 모든 시름들이 멀리 사라져 버린 듯 했는데

...
```
`InputStreamReader` 클래스는 바이트 스트림을 문자열 스트림으로 가져온다. 이때 인자로 charset을 설정하여 인코딩을 설정할 수 있다.
## 버퍼 사용
```
public class Main {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static void main(String[] args) {
        var fis3 = measureTime(Main::fileInputStrmEx3);
    }

    public static void fileInputStrmEx3 () {
        // 버퍼를 사용
        byte[] buffer = new byte[1024]; // 바이트 (1024개)단위로 문자를 받음

        Charset charset = StandardCharsets.UTF_8;

        try (FileInputStream fis = new FileInputStream(SONG_PATH)) {
            int readByte;
            int count = 0;

            // read에 buffer를 인자로 넣음
            while ((readByte = fis.read(buffer)) != -1) {
                String readStr = new String(
                        buffer, 0, readByte, charset
                );
                System.out.println(readStr);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```
버퍼를 사용하는 경우 1바이트씩 받아오는 것 보다는 빠르지만

마지막 버퍼의 공간을 전부 사용하지 않는다면 남은 공간을 0으로 채우기 때문에 비효율적이다.
## BufferedInputStream
```
public class Main {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static void main(String[] args) {
        var fis3 = measureTime(Main::fileInputStrmEx3);
    }

    public static void bufferedInputEx () {
        Charset charset = StandardCharsets.UTF_8;

        try (
                BufferedInputStream bis = new BufferedInputStream(
                        new FileInputStream(SONG_PATH)
                        //, 4096 // 바이트 크기 지정 가능
                )
        ) {
            byte[] buffer = new byte[1024];
            int readByte;
            int count = 0;

            while ((readByte = bis.read(buffer)) != -1) {
                String readStr = new String(
                        buffer, 0, readByte, charset
                );
                System.out.println(readStr);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```
`BufferedInputStream` 클래스는 기본적으로 8192 바이트의 내부 버퍼를 사용하고, 이때 바이트 크기는 인자로 조절할 수 있다.

`BufferedInputStream`를 사용하는 경우 `byte[]` 형태로 받아오는 것에 비해
1. 내부 버퍼로부터 가져오고,
2. 공간이 남을 때, 해당 공간을 채우지 않고 받아오므로
성능이 더 좋다.
## FileOutputStream, write
```
public class Main2 {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static final String IMG_PATH = "src/sec12/chap03/windows.jpeg";
    public static void main(String[] args) {
        writeLittleStar();
    }

    public static void writeLittleStar () {
        var filePath = "src/sec12/chap03/little_star.txt";
        Charset charset = StandardCharsets.UTF_8;

        List<String> lines = Arrays.asList(
                "hello",
                "world"
        );

        try (
                BufferedOutputStream bos = new BufferedOutputStream(
                        new FileOutputStream(filePath)
                )
        ) {
            for (String line : lines) {
                byte[] buffer = (line + "\n").getBytes(charset);
                bos.write(buffer, 0, buffer.length);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```
`FileOutputStream` 클래스와 `BufferedOutputStream` 클래스는 각각 파일을 쓰고, 버퍼링을 사용하며 `FileOutputStream`에 경로를 인자로 주는 객체를 `BufferedOutputStream`의 인자로 주어 사용한다.

`write` 메소드는 `BufferedOutputStream` 객체에 해당 값을 입력하는 방식으로 파일을 작성한다.
## copy
```
public class Main2 {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static final String IMG_PATH = "src/sec12/chap03/windows.jpeg";
    public static void main(String[] args) {
        copyWithFilesClass(IMG_PATH, "new_windows2.jpeg");
    }

    public static void copyWithFilesClass (String from, String newFileName) {
        Path fromPath = Paths.get(from);
        Path toPath = fromPath.getParent().resolve(Paths.get(newFileName));

        try {
            Files.copy(fromPath, toPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```
`copy` 메소드는 기존 경로와 복사할 경로를 인자로 받아 복사한다.

내부에서 `BufferedInputStream`, `BufferedOutputStream`를 자체적으로 사용하여 예외 처리가 구현되어 있고, 간결하기 때문에 주로 사용된다.
### `BufferedInputStream`, `BufferedOutputStream`
```
public class Main2 {
    public static final String SONG_PATH = "src/sec12/chap03/beatles.txt";
    public static final String IMG_PATH = "src/sec12/chap03/windows.jpeg";
    public static void main(String[] args) {
        copyWithBis(IMG_PATH, "new_windows2.jpeg");
    }

    public static void copyWithBis (String from, String newFileName) {
        Path fromPath = Paths.get(from);
        Path toPath = fromPath.getParent().resolve(Paths.get(newFileName));
        String to = toPath.toString();

        try (
                BufferedInputStream bis = new BufferedInputStream(
                        new FileInputStream(from)
                );
                BufferedOutputStream bos = new BufferedOutputStream(
                        new FileOutputStream(to)
                )
        ) {

            byte[] buffer = new byte[1024];
            int readBytes;
            while ((readBytes = bis.read(buffer)) != -1) {
                bos.write(buffer, 0, readBytes);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```
위의 `copy` 메소드를 사용한 방식의 풀이이다.

`BufferedInputStream` 클래스를 사용하여 복사하고자 하는 파일을 읽고 `BufferedOutputStream` 클래스를 사용하여 복사 경로에 파일을 생성한다.
## DataInoutStream, DataOutputStream
```
public class Main3 {
    public static void main(String[] args) {
        String DATA_PATH = "src/sec12/chap03/data.bin";

        try (
                FileOutputStream fos = new FileOutputStream(DATA_PATH);
                DataOutputStream dos = new DataOutputStream(fos);
        ) {
            // 각 자료형의 값을 이진 데이터로 저장
            dos.writeBoolean(true);
            dos.writeInt(123);
            dos.writeDouble(3.14);
            dos.writeChar('A');
            dos.writeUTF("한국어"); // 문자열을 UTF-8 형식으로
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

       try (
                FileInputStream fis = new FileInputStream(DATA_PATH);
                DataInputStream dis = new DataInputStream(fis);
        ) {
            boolean read1 = dis.readBoolean();
            int read2 = dis.readInt();
            double read3 = dis.readDouble();
            char read4 = dis.readChar();
            String read5 = dis.readUTF();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```
`DataInoutStream`, `DataOutputStream` 클래스는 `.bin` 파일과 같이 사용자가 읽는 것이 아닌 저장하는 용도에 주로 사용한다.

위와 같이 파일을 생성한 경우 파일을 읽을 때 생성한 순서대로, 정확한 자료형으로만 값을 제대로 확인할 수 있다.
