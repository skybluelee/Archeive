1. **단일 파일 복사**:
   ```
   cp file1.txt file1_backup.txt
   ```

2. **다중 파일 복사**:
   ```
   cp file1.txt file2.txt file3.txt /path/to/destination/
   ```

3. **디렉토리 복사**:
   ```
   cp -r directory1 /path/to/destination/
   ```

4. **디렉토리 및 그 안의 모든 내용 복사**:
   ```
   cp -r directory1/* /path/to/destination/
   ```

5. **디렉토리 및 그 안의 숨김 파일/디렉토리 포함 모든 내용 복사**:
   ```
   cp -r directory1/. /path/to/destination/
   ```

6. **변경 내용 없이 덮어쓰기 (명시적으로 확인하지 않음)**:
   ```
   cp -f file1.txt /path/to/destination/
   ```

7. **대상 디렉토리가 존재하지 않으면 생성**:
   ```
   cp -r directory1 /path/to/new_directory/
   ```

8. **심볼릭 링크를 따라 복사 (원본 파일이 복사되는 것이 아님)**:
   ```
   cp -r -L symbolic_link /path/to/destination/
   ```

9. **권한 및 소유권도 함께 복사**:
   ```
   cp -r --preserve=all directory1 /path/to/destination/
   ```

이러한 예시는 `cp` 명령어의 주요 사용 사례를 보여줍니다. 필요에 따라 옵션과 인자를 조합하여 사용할 수 있습니다.
