# S3 -> Lambda -> OpenSearch를 실행하는 과정

# S3 버킷을 트리거로 설정
기존에 버킷이 존재하는 상태에서 시작한다.

<img src="https://github.com/skybluelee/Archeive/assets/107929903/69ea80fe-1f36-408f-9017-76661a03d7a8.png" width="1000" height="400"/>

좌측에 소스를 S3로 정한 후, 사용할 버킷을 설정한다. 이벤트 타입은 객체가 추가되거나 업데이트되는 경우에만 OpenSearch로 보내기위해 PUT으로 지정하였다.

prefix와 suffix를 추가로 설정하여 자신이 원하는 형식의 파일만 트리거하도록 만들 수 있다.

# Lambda 설정
## 함수 생성
새로 작성에서

> 함수 이름: 원하는 대로 설정
>
> 런타임의 경우 본인이 작성할 언어를 선택한다.
> 나의 경우 파이썬을 설정하였다.
>
> 아키텍처: x86_64

## 코드
`OpenSearch_Indexing.py`에 있는 코드를 사용한다.

해당 파일은 S3에 csv파일이 업로드되는 경우 트리거되어 OpenSearch로 전송하는 방식에 맞추어져 있다. 본인이 사용하는 형식에 맞게 변형해야 한다.

## 권한
IAM 사용자가 필요하다. OpenSearch에 접근하기 위해 권한이 필요하다(`awsauth = AWS4Auth(access_key, secret_key, region, service)`에서 사용).

해당 사용자는 OpenSearch에 대한 권한이 필요하다.

Lambda에 대한 정책을 설정해야 한다. Lambda를 생성한 이후 IAM 역할에 Lambda에 대한 역할이 생겼다. S3에 대한 읽기 권한과 OpenSearch에 대한 쓰기 권한이 필요하다.

## 계층 생성
인덱싱하기 위해서는 `requests`와 `requests_aws4auth`모듈이 필요하다. 기존 람다에는 설치되어 있지 않아 사용자가 추가해야 한다.

```
pip install requests -t python
zip -r requests.zip ./python
```
```
pip install requests_aws4auth -t python
zip -r requests_aws4auth.zip ./python
```
해당 명령을 사용하여 압축 파일로 만든다.

이때 다른 명령어 사용시 Lambda가 unzip할 수 없다는 오류가 발생하니 위 코드로 진행하면 된다.

계층 생성에서 이름을 정확하게 전달해야 한다. 이름을 제대로 적지 않으면 import 오류가 발생한다.
앞서 만든 zip 파일을 업로드하고 생성한다.

2개의 계층을 생성하고 Lambda 함수 내에서 계층 -> [Add a layer]를 클릭하여 생성한 계층을 추가한다.

## 로그
Lambda에 대한 로그는 Cloudwatch -> 로그 -> 로그 그룹 에서 확인할 수 있다.

# OpenSearch
## 생성
OpenSearch를 생성한다. 생성시 표준 생성으로 들어가야 더 저렴한 인스턴스, 적은 용량 등을 선택하여 비용을 줄일 수 있다.

나의 경우
> 도메인 생성 방법: 표준 생성
>
> 템플릿: 개발 및 테스트
>
> 배포 옵션: 대기 없는 도메인, 가용 영역: 1-AZ
>
> 엔진 옵션: 2.11(최신)
>
> 데이터 노드
>
> > Instance family - new: General Purpose
> >
> > 인스턴스 유형: t3.small.search
> >
> > 노드 수: 2
> >
> > ...
> >
> > 노드당 EBS 스토리지 크기: 10(최솟값임)
> 
> ...
>
> 네트워크: 퍼블릭 액세스
>
> 세분화된 액세스 제어: 마스터 사용자를 생성
>
> 액세스 정책: 세분화된 액세스 제어만 사용
>
> 암호화: AWS 소유 키 사용
>
> ...
>
> 고급 클러스터 설정 -> 최대 절 수: 1024

로 설정하였다. 참고로 고급 클러스터 설정의 최대 절 수는 기본값이 없어 반드시 설정해야 한다.

## 보안
### 사용자
보안 구성 -> 편집 -> IAM ARN을 마스터 사용자로 설정

에서 초기에 Lambda에서 말한 IAM 사용자의 arn을 사용하고 변경 사항을 저장한다.

해당 상태에서는 로그인이 안되니 다시 보안 구성에서 마스터 사용자로 변경하고 변경 사항을 저장한다.

이와 같이 사용하는 이유는 OpenSearch 내부에서는 사용자를 생성할 때 `:`를 사용하지 못하기 때문이다.

이후 OpenSearch에서 Security -> Roles -> all_access -> Mapped users를 방문하면 arn:aws:iam::1234567890:user/<iam_user_name> 형태의 사용자와 최초에 만든 마스터 사용자가 등록되어 있을 것이다.

세분화된 액세스 제어를 선택하였기 때문에 모든 접근이 허가되어 있다. 보안을 위해 해당 정책을 적절히 변경해야 한다.

# 참고
**[AWS Lambda Layers로 함수 공통용 Python 패키지 재사용하기](https://beomi.github.io/2018/11/30/using-aws-lambda-layers-on-python3/)**

**[[AWS] Lambda에 request 모듈 추가하기](https://velog.io/@jadenchoi94/AWS-Lambda%EC%97%90-request-%EB%AA%A8%EB%93%88-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0)**

**[Amazon OpenSearch Service에서 HTTP 요청 압축](https://docs.aws.amazon.com/ko_kr/opensearch-service/latest/developerguide/gzip.html)**

**[스트리밍 데이터를 Amazon OpenSearch 서비스에 로드](https://docs.aws.amazon.com/ko_kr/opensearch-service/latest/developerguide/integrations.html)**
