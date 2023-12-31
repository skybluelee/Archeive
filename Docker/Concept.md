# Docker
Docker는 컨테이너화된 애플리케이션을 만들고 배포하기 위한 오픈 소스 플랫폼이다. 컨테이너는 애플리케이션과 해당 종속성을 격리된 환경에서 실행할 수 있도록 하는 가상화 기술이다.
## 주요 개념
**이미지**
- Docker 컨테이너의 실행 환경과 애플리케이션 코드, 라이브러리 등의 모든 요소를 포함하는 패키지이다.
- 이미지는 읽기 전용이며, 애플리케이션을 실행할 때 사용된다.

**컨테이너**
- 이미지의 인스턴스로 격리된 환경에서 실행되는 프로세스이다.
- 컨테이너는 호스트 시스템과 격리되어 있으며, 독립적으로 실행된다.

**도커 레지스트리**
- 도커 이미지를 저장하고 공유할 수 있는 원격 저장소이다.
- Docker Hub, ECR 등이 있다.

**도커 컴포즈(Docker Compose)**
- 여러 컨테이너로 구성된 멀티-컨테이너 애플리케이션을 정의하고 실행하기 위한 도구이다.
- YAML 파일로 컨테이너 구성을 정의하고 한 번에 여러 컨테이너를 실행할 수 있다.
## 특징
**포터빌리티(Portability)**
- Docker 컨테이너는 애플리케이션과 해당 종속성을 포함하며, 실행 환경과 상관없이 동일하게 작동한다.
- 애플리케이션을 다른 환경으로 쉽게 이동하고 배포할 수 있다.

**경량화(Lightweight)**
- Docker 컨테이너는 가상 머신보다 가볍고 빠르게 시작된다.
- 컨테이너는 호스트의 커널을 공유하므로 가상 머신보다 더 효율적으로 리소스를 사용한다.

**쉬운 배포 및 스케일링(Easy Deployment and Scaling)**
- Docker 컨테이너는 빠르게 시작되고 중지할 수 있으며, 필요에 따라 애플리케이션 인스턴스를 스케일링할 수 있다.

**이미지 관리(Immutability)**
- Docker 이미지는 읽기 전용이며 변경되지 않는다.
- 변경 사항이 필요한 경우 새로운 이미지를 빌드하고 배포할 수 있다.

**다양한 환경 지원(Multi-Environment Support)**
- Docker는 Linux, Windows, macOS 등 다양한 운영 체제와 클라우드 환경에서 사용할 수 있다.

**자동화(Automation)**
- Docker는 컨테이너 오케스트레이션 도구인 Docker Compose, Docker Swarm, Kubernetes와 통합하여 자동화된 배포 및 관리를 지원한다.
## 장점
**효율성**
- Docker 컨테이너는 가상화보다 빠르고 효율적으로 리소스를 사용하며, 더 빠른 배포와 스케일링이 가능하다.

**일관성**
- 이미지를 사용하여 애플리케이션과 환경을 일관되게 유지하고, 버그와 호환성 문제를 줄일 수 있다.

**편리한 로컬 개발**
- 개발 환경과 프로덕션 환경 간의 차이를 최소화하고 로컬 머신에서도 동일한 환경을 테스트할 수 있다.

**안전성 및 격리**
- 컨테이너는 격리된 환경에서 실행되므로 애플리케이션 간의 상호 영향을 최소화하고 보안을 강화합니다.

**스케일링 용이성**
- 필요한 경우 컨테이너 인스턴스를 추가하거나 제거하여 애플리케이션을 쉽게 스케일링할 수 있다.
- 서버 확장하는 과정이 용이하다.
