**본 문서는[S3Hook](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/aws/hooks/s3/index.html),
[S3 customization reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#s3-transfers),
[File transfer configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html),
[Apache Airflow for Data Science - How to Download Files from Amazon S3](https://betterdatascience.com/apache-airflow-amazon-s3-download/)를 참조하였다.**

# S3Hook
> `classairflow.providers.amazon.aws.hooks.s3.S3Hook(aws_conn_id=AwsBaseHook.default_conn_name, transfer_config_args=None, extra_args=None, *args, **kwargs)`

## Parameter
- `aws_conn_id (AwsBaseHook.default_conn_name)`: aws 계정과 연결한다. S3에 대해 적절한 읽기, 쓰기 권한이 있는 IAM 사용자와 연결한다.
- `transfer_config_args (dict | None) `: 데이터 전송 방식을 나타낸다.
- `extra_args (dict | None)`: 전송시 추가 인자(예: 암호화 방식)를 설정한다.

### aws_conn_id
IAM -> 사용자 -> 사용자 생성 -> S3에 대한 권한 설정 -> Access Key, Secret Key 발급

이후 Airflow Web UI -> Connections 추가
> Connection Id: `S3Hook`에서 사용할 `aws_conn_id` 인자
> 
> Connection Type: Amazon Web Services
> 
> AWS Access Key Id: 발급한 access key
> 
> AWS Secret Access Key: 발급한 secret key

### transfer_config_args
**multipart_threshold**
```
import boto3
from boto3.s3.transfer import TransferConfig

# Set the desired multipart threshold value (5GB)
GB = 1024 ** 3
config = TransferConfig(multipart_threshold=5*GB)

# Perform the transfer
s3 = boto3.client('s3')
s3.upload_file('FILE_NAME', 'BUCKET_NAME', 'OBJECT_NAME', Config=config)
```
특정 용량 이상부터는 여러 파트로 나누어 S3에 업로드한다.

위의 경우 5GB를 초과하는 경우 여러 파트로 분할한 후 업로드한다.
***
**max_concurrency**
```
# To consume less downstream bandwidth, decrease the maximum concurrency
config = TransferConfig(max_concurrency=5)

# Download an S3 object
s3 = boto3.client('s3')
s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME', Config=config)
```
S3 API 전송 작업의 최대 동시 실행 수는 연결 속도에 맞게 조정한다.
`max_concurrency` 속성을 조절하여 대역폭 사용량을 늘리거나 줄일 수 있으며, 이 속성의 기본 설정 값은 10이다.

위 코드는 `max_concurrency`를 5로 설정하여 S3 객체를 다운로드할 때 동시에 처리되는 작업 수를 5개로 제한한다.
이렇게 하면 다운스트림 대역폭 사용이 줄어든다.
***
**Threads**
```
# Disable thread use/transfer concurrency
config = TransferConfig(use_threads=False)

s3 = boto3.client('s3')
s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME', Config=config)
```
S3 전송중 동시성을 구현하는 경우 스레드를 사용한다.
스레드 사용을 비활성화하려면 `use_threads` 속성을 `False`로 설정하면 된다.

스레드 사용이 비활성화되면 전송 동시성이 발생하지 않으며, 따라서 `max_concurrency` 속성의 값은 무시된다.

### extra_args
**업로드의 경우**
```
ALLOWED_UPLOAD_ARGS = ['ACL', 'CacheControl', 'ChecksumAlgorithm', 'ContentDisposition', 'ContentEncoding', 'ContentLanguage',
'ContentType', 'ExpectedBucketOwner', 'Expires', 'GrantFullControl', 'GrantRead', 'GrantReadACP', 'GrantWriteACP', 'Metadata',
'ObjectLockLegalHoldStatus', 'ObjectLockMode', 'ObjectLockRetainUntilDate', 'RequestPayer', 'ServerSideEncryption',
'StorageClass', 'SSECustomerAlgorithm', 'SSECustomerKey', 'SSECustomerKeyMD5', 'SSEKMSKeyId', 'SSEKMSEncryptionContext',
'Tagging', 'WebsiteRedirectLocation']
```
***
**다운로드의 경우**
```
ALLOWED_DOWNLOAD_ARGS = ['ChecksumMode', 'VersionId', 'SSECustomerAlgorithm', 'SSECustomerKey', 'SSECustomerKeyMD5',
'RequestPayer', 'ExpectedBucketOwner']
```

## Example - Upload
```
import pendulum
from airflow.models.dag import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="example_S3Hook",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
):
    def s3_upload():
        # 버킷과 키 이름 설정
        # 키에 해당하는 디렉토리, 이름으로 저장되므로 확장자까지 적어야 함
        bucket_name = "<bucket_name>"
        key = "<key_name>"
        # docker-compose.yaml 파일에서 volume으로 설정한 장소에서 사용 가능
        local_file_path = "/opt/airflow/dags/requirements.txt"
        hook = S3Hook(aws_conn_id='aws_conn') # Airflow Web UI에서 AWS Connection 먼저 설정
        hook.load_file(
            bucket_name=bucket_name,
            key=key,
            filename=local_file_path
        )

    dag_s3_upload = PythonOperator(task_id="s3_upload", python_callable=s3_upload)

    dag_s3_upload
```

## Example - Download
```
import pendulum
from airflow.models.dag import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
import os

with DAG(
    dag_id="example_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
):
    def s3_download():
        # 버킷과 키 이름 설정
        bucket_name = "news-data"
        key = 'test.txt'
        # 다운받을 위치
        local_file_path = "/opt/airflow/dags"
        hook = S3Hook(aws_conn_id='aws_conn')
        file = hook.download_file(
            bucket_name=bucket_name,
            key=key,
            local_path=local_file_path
        )
        # 업로드와 달리 리턴 값(다운받을 파일) 존재
        return file

    # 다운로드시 기존 파일 이름 그대로 다운되지 않아 파일명을 변경해야 함
    def rename_file(ti, new_name: str):
        downloaded_file_name = ti.xcom_pull(task_ids=['s3_upload'])
        downloaded_file_path = '/'.join(downloaded_file_name[0].split('/')[:-1])
        os.rename(src=downloaded_file_name[0], dst=f"{downloaded_file_path}/{new_name}")

    dag_s3_download = PythonOperator(task_id="s3_upload", python_callable=s3_download)

    task_rename_file = PythonOperator(
        task_id='rename_file',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'test.txt' # 변경할 파일 이름
        }
    )

    dag_s3_download >> task_rename_file
```
