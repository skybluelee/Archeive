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
# Reader, Writer
`InputStream`과 `OutputStream`은 바이트 기반 스트림을 처리할 때 사용하고,

문자 기반 스트림은 `Reader` 와 `Writer`를 사용한다.
## FileReader, BufferedReader, InputStreamReader
**`FileReader`, `FileWriter`의 경우**
```
public static void fileReaderWriterEx () {
    Charset charset = StandardCharsets.UTF_8;    
    try (
            FileReader fr = new FileReader(
                    SONG_PATH, charset
            );
            FileWriter fw = new FileWriter(
                    SONG_PATH.replace("beatles", "beatles_1")
                    , charset
            )
    ) {    
        int c;  // 문자를 숫자로 받고 형변환
        while ((c = fr.read()) != -1) {
            System.out.print((char) c);
            fw.write(c);
        }
    
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```
각 문자를 하나씩 받고 출력한다.
***
**`BufferedReader`, `BufferedWriter`의 경우**
```
public static void bufferedReaderWriterEx () {
    Charset charset = StandardCharsets.UTF_8;    
    try (
            FileReader fr = new FileReader(
                    SONG_PATH, charset      // 디폴트는 8192바이트, 인자로 바이트 설정 가능
            );
            BufferedReader br = new BufferedReader(fr);
            FileWriter fw = new FileWriter(
                    SONG_PATH.replace("beatles", "beatles_2")
                    , charset
            );
            BufferedWriter bw = new BufferedWriter(fw);
    ) {    
        String line; // 한 줄씩 읽음
        while ((line = br.readLine()) != null) {
            System.out.println(line);
            bw.write(line);
            bw.newLine(); // 줄 바꿈
        }    
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```
한 줄씩 받아 읽고 출력한다.
***
**`FileInputStream  - InputStreamReader - BufferedReader`, `FileOutputStream - OutputStreamWriter - BufferedWriter`의 경우**
```
public static void ioStreamReaderWriterEx () {
    Charset charset = StandardCharsets.UTF_8;
    try (
            // 디폴트는 8192바이트, 인자로 바이트 설정 가능
            FileInputStream fis = new FileInputStream(SONG_PATH);
            InputStreamReader ir = new InputStreamReader(fis, charset);
            BufferedReader br = new BufferedReader(ir);
            FileOutputStream fos = new FileOutputStream(
                    SONG_PATH.replace("beatles", "beatles_3")
            );
            OutputStreamWriter ow = new OutputStreamWriter(fos, charset);
            BufferedWriter bw = new BufferedWriter(ow);
    ) {
    
        String line;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
            bw.write(line);
            bw.newLine(); // 줄 바꿈
        }
    
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```
한 줄씩 받아 읽고 출력한다.
***
**결론**
성능은 `InputStreamReader`와 `OuputStreamWriter`를 사용하는 코드가 가장 좋다. 

하지만 코드가 복잡하기 때문에 성능이 우선 사항이 아니라면 코드가 간단한 `FileReader/FileWriter` 혹은 `BufferedReader/BufferedWriter`를 사용한다.
# StringReader, StringWriter
문자열 데이터를 메모리에서 읽거나 쓸 때 사용한다.

대용량 문자열에 대한 텍스트 처리에 적합하다.
```
public class Main3 {
    public static void main(String[] args) {
        String csvTxt = ""
                + "1, 2, 3, 4, 5\n"
                + "6, 7, 8, 9, 10\n"
                + "11, 12, 13, 14, 15\n"
                + "16, 17, 18, 19, 20\n"
                + "21, 22, 23, 24, 25"
                ;
        List<Integer[]> fromCsv = new ArrayList<>();
        
        try (
                StringReader sr = new StringReader(csvTxt);
                BufferedReader br = new BufferedReader(sr);
        ) {
            String line;
            while ((line = br.readLine()) != null) {
                fromCsv.add(
                        Arrays.stream(
                                line.replace(" ", "").split(",")
                        ).map(Integer::parseInt)
                        .toArray(Integer[]::new)
                );
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

numbers.csv
1, 4, 9, 16, 25
36, 49, 64, 81, 100
121, 144, 169, 196, 225
256, 289, 324, 361, 400
441, 484, 529, 576, 625
```
`FileReader, BufferedReader, InputStreamReader`와 다르게 메모리에 담긴 값을 읽고 쓸 수 있다.
# 번외 - print
```
public class Main4 {
    public static void main(String[] args) {
        String PRINT_PATH = "src/sec12/chap04/print.txt";

        PrintStream ps = null;
        FileOutputStream fos = null;

        try {
            fos = new FileOutputStream(PRINT_PATH);
            ps = new PrintStream(fos);

            System.setOut(ps);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }

        System.out.println("hello");
        System.out.printf("%s!%n", "world");
    }
}

print.txt
hello
world!
```
`print`의 경로를 `PrintStream`과 `FileOutputStream`를 사용하여 변경하면 `print`한 결과가 해당 파일로 생성된다.

System의 out은 `PrintStream`이므로 다른 스트림과 동일하게 경로로 write할 수 있다.
# Serialization
직렬화는 인스턴스를 바이트 스트림으로 변환하며, 인스턴스를 다른 곳에 보내거나 파일 등으로 저장하기 위해 사용한다.
## 클래스와 필드의 직렬화
```
public class Person implements Serializable {
    // serialVersionUID : 클래스의 버전 번호로 사용
    private static final long serialVersionUID = 1L;
    private String name;
    private int age;
    private double height;
    private boolean married;

    transient private String bloodType;
    transient private double weight;

    private Career career;

    public Person(
            String name, int age, double height, boolean married,
            String bloodType, double weight, Career career
    ) {
        this.name = name;
        this.age = age;
        this.height = height;
        this.married = married;
        this.bloodType = bloodType;
        this.weight = weight;
        this.career = career;
    }
}
```
```
public class Career implements Serializable {
    private static final long serialVersionUID = 1L;
    private String company;
    private int years;

    public Career(String company, int years) {
        this.company = company;
        this.years = years;
    }
}
```
해당 클래스에 직렬화를 사용하기 위해서는 `Serializable` 인터페이스를 implements해야 한다.

이 경우 클래스 내의 모든 필드는 자동으로 직렬화의 대상이 된다. 이때 특정 필드에 대해 직렬화를 원하지 않는 다면 `transient`를 사용하여 직렬화에서 제외할 수  있다.

직렬화 클래스에 다른 클래스의 필드도 직렬화를 하려면 해당 클래스도 `Serializable` 인터페이스를 implements해야 한다.

`serialVersionUID`는 클래스의 버전 번호로 동일한 값을 사용해야 직렬화, 역직렬화가 가능하다.
## 직렬화, 역직렬화
```
public class Main {
    public static String PEOPLE_PATH = "src/sec12/chap05/people.ser";
    public static void main(String[] args) {
        Person person1 = new Person(
                "홍길동", 20, 175.5, false, "AB", 81.2, new Career("ABC Market", 2)
              // name, age, height, married, bloold, weight, career
              // blood type과 weight는 직렬화 대상이 아님  
        );

        List<Person> people = new ArrayList<>();
        people.add(person1);
        people.add(new Person(
                "임꺽정", 45, 162.8, true,
                "A", 68.3,
                new Career("Koryeo Inc.", 20)
        ));
        people.add(new Person(
                "붉은매", 24, 185.3, false,
                "B", 79.3,
                new Career("Cocoa", 30)
        ));

        try (
                FileOutputStream fos = new FileOutputStream(PEOPLE_PATH);
                BufferedOutputStream bos = new BufferedOutputStream(fos);
                ObjectOutputStream oos = new ObjectOutputStream(bos);
        ) {
            oos.writeObject(person1);
            oos.writeObject(person2);
            oos.writeObject(people);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}

```
`FileOutputStream - BufferedOutputStream - ObjectOutputStream`을 사용하여 인스턴스를 스트림으로 출력한다.

`.ser` 파일이 생성되며, 이는 읽기 위한 파일이 아닌 저장용 파일이다.
```
public class Main2 {
    public static String PEOPLE_PATH = "src/sec12/chap05/people.ser";
    public static void main(String[] args) {
        Person person1Out;
        List<Person> peopleOut;

        try (
                FileInputStream fis = new FileInputStream(PEOPLE_PATH);
                BufferedInputStream bis = new BufferedInputStream(fis);
                ObjectInputStream ois = new ObjectInputStream(bis);
        ) {

            person1Out = (Person) ois.readObject();
            // person1Out: name="홍길동", age=20, height=175.5, married=false, bloodType=null, weight=0.0, career-company="ABC Market", year=2
            peopleOut = (ArrayList) ois.readObject();
            // size = 4
            // 0 - name="홍길동", ...
            // 1 - name="임꺽정", ...
            // 2 - name="붉은매", ...

        } catch (IOException | ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }
}
```
`FileInputStream - BufferedInputStream - ObjectInputStream`으로 인스턴스를 역직렬화한다.

앞서 `.bin` 파일과 동일하게 생성한 순서대로 역직렬화를 실시해야 한다.

직렬화를 사용하여 필드를 저장한 경우 기본적으로 이전 값이 그대로 나오지만, `transient`를 선언한 필드의 값은 `null`값이 나오는 것을 확인할 수 있다.
# URL
## 기본 클래스와 메소드
```
public class Main {
    public static void main(String[] args) throws MalformedURLException { // URL에 대한 오류 throw
        URL url1 = new URL("https://showcases.yalco.kr/java/index.html");

        URL url2 = new URL("https://showcases.yalco.kr");
        URL url3 = new URL(url2, "/java/index.html");
        URL url4 = new URL("https://example.com/path/to/resource?param=value")

        String url1Str = url1.toExternalForm(); // url1Str: https://showcases.yalco.kr/java/index.html
        String url3Str = url3.toExternalForm(); // url3Str: https://showcases.yalco.kr/java/index.html
        boolean sameUrl = url1.equals(url3);    // sameUrl: true

        // 전체 url을 문자열로 반환
        String content = url4.toExternalForm(); // "https://example.com/path/to/resource?param=value"
        // 파일 이름 + 쿼리 문자열
        String file = url4.getFile();           // "/path/to/resource?param=value"
        // 파일 이름
        String path = url4.getPath();           // "/path/to/resource"
        // 호스트 부분
        String host = url4.getHost();           // "example.com"
        // 사용 포트
        long port = url4.getPort();             // -1
        // 디폴트 포트
        long defPort = url4.getDefaultPort();   // 443
    }
}
```
`URL` 클래스는 인자가 하나인 경우 해당 문자열의 url 객체를 생성한다. 인자가 두 개인 경우 첫번째 url 객체에 두번째 인자를 추가한 객체를 생성한다.
## 인터넷 연결
```
public class Main2 {
    public static void main(String[] args) throws IOException {
        URL yalco = new URL("https://showcases.yalco.kr");
        URL home = new URL(yalco, "/java/index.html");

        URLConnection conn = home.openConnection();

        try(
                InputStream is = conn.getInputStream();

                var isr = new InputStreamReader(is);
                var br = new BufferedReader(isr);

                var sw = new StringWriter();
                var pr = new PrintWriter(sw)
        ) {
            String line;
            while ((line = br.readLine()) != null) {
                pr.printf("%s%n", line);
            }
            System.out.println(sw);
        }
    }
}
```
`openConnection` 메소드를 사용하여 해당 링크에 접속할 수 있다.

`URLConnection`의 객체 `conn`은 html 정보를 담고 있으며 위 코드는 html의 각 라인을 출력한다.
# 소켓 통신
## TCP
TCP의 경우 UDP에 비해 속도가 느리지만, 데이터 전송 순서를 보장하고 상대방의 수신 여부에 따라 자동 재전송을 실행한다.
```
public class TCPServer {
    public static final String SERVER_IP = "127.0.0.1";
    public static final int PORT_NO = 1234;

    public static void main(String[] args) {

        try (
                ServerSocket serverSkt = new ServerSocket(PORT_NO)
        ) {
            while (true) {   // 서버는 계속 켜져있어야 함
                try (
                        Socket clientSkt = serverSkt.accept();

                        var is = clientSkt.getInputStream();
                        var isr = new InputStreamReader(is);
                        var br = new BufferedReader(isr);
                        var sw = new StringWriter();
                        var piw = new PrintWriter(sw);

                        var os = clientSkt.getOutputStream();

                        var pow = new PrintWriter(os, true); // autoflush: true
                ) {
                    String line;
                    int lineCount = 1;
                    while ((line = br.readLine()) != null) {
                        piw.printf(
                                "%3d :  %s%n".formatted(
                                        lineCount++, line
                                )
                        );
                        // 클라이언트에게 수신
                        pow.printf("수신: %s %n".formatted(line.substring)), line.length();
                    }
                    System.out.println(sw);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```
TCP 서버는 `ServerSocket` 클래스 객체를 생성하여 `try with resource`문에서 서버 소켓을 생성한 상태로 진행한다.

이후 서버는 계속 켜져있는 상태여야 하므로 `while(1)`을 사용해 무한 반복 상태로 만들고 입력과 출력 코드를 작성한다.

서버로 들어오는 값은 `getInputStream` 메소드를 사용하고, 클라이언트로 전송할 값은 `getOutputStream` 메소드를 사용한다.

`PrintWriter` 메소드의 `true`는 autoflush를 의미하는데, 이는 값을 수신받는 즉시 이하의 코드를 실행하는 명령이다.
```
public class TCPClient {
    public static String lyric = "";

    public static void main(String[] args) {
        try (
                Socket socket = new Socket(SERVER_IP, PORT_NO);

                var os = socket.getOutputStream();
                var pw = new PrintWriter(os, true); // autoflush

                var is = socket.getInputStream();
                var isr = new InputStreamReader(is);
                var br = new BufferedReader(isr);
        ) {
            for (var line : lyric.split("\n")) {
                pw.println(line);
                System.out.println(br.readLine());
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}
```
클라이언트는 서버 IP, 포트 번호를 인자로 하는 소켓을 생성하고, 해당 소켓에 연결한다.

서버와 동일하게 수신받는 메소드와 송신하는 메소드는 `getInputStream, getOutputStream`이다.
## UDP
UDP는 TCP에 비해 속도가 빠르지만 순서를 보장하지 않는다.
```
public class UDPServer {
    public static final int PORT_NO = 2345;

    public static void main(String[] args) {
        try (DatagramSocket serverSkt = new DatagramSocket(PORT_NO)) {
            while (true) {
                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(
                        receiveData, receiveData.length
                );

                serverSkt.receive(receivePacket);

                String received = new String(
                        receivePacket.getData(),
                        0, receivePacket.getLength()
                );
                System.out.println(received);

                for (var i = 0; i < 9; i++) {
                    var answer = received + (i + 1);
                    byte[] toSend = answer.getBytes();

                    // 송신
                    DatagramPacket sendPacket = new DatagramPacket(
                            toSend,                         
                            toSend.length,                  
                            receivePacket.getAddress(),     
                            receivePacket.getPort()         
                    );

                    serverSkt.send(sendPacket);
                }
            }
        } catch (SocketException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
        }
    }
}
```
UDP의 경우 `DatagramSocket` 클래스를 통해 소켓 객체를 생성한다. 인자로 포트 번호를 지정한다.

UDP는 순서를 보장할 필요가 없기 때문에 `DatagramPacket` 클래스로 생성한 객체에 생성한 바이트 배열을 인자로 지정하여 값을 한번에 수신한다.
이때 필요한 인자는 4가지로 수신할 값, 값의 크기, IP 주소, 포트 번호를 인자로 지정한다.

수신과 송신은 TCP에 비해 간결한데 `DatagramSocket` 클래스의 객체에 `receive, send` 메소드를 통해 값을 수신하고 송신할 수 있다.

순서 상관 없이 전송하기 때문에 TCP와 달리 autoflush 기능이 존재하지 않는다.
```
public class UDPClient {
    public static final String SERVER_IP = "127.0.0.1";

    public static void main(String[] args) {
        try (DatagramSocket clientSkt = new DatagramSocket()) {
            InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

            for (var i = 0; i < 100; i++) {
                byte[] sendData = ("click " + (i + 1)).getBytes();
                DatagramPacket sendPacket = new DatagramPacket(
                        sendData,
                        sendData.length,
                        serverAddr,
                        PORT_NO
                );

                clientSkt.send(sendPacket);

                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(
                        receiveData, receiveData.length
                );

                for (var j = 0; j < 9; j++) {
                    clientSkt.receive(receivePacket);

                    String response = new String(
                            receivePacket.getData(),
                            0, receivePacket.getLength()
                    );
                    System.out.println(response);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```
