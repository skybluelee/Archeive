# OLTP, OLAP
OLTP, OLAP는 다양한 데이터 처리 작업에 사용되는 2가지 주요 데이터 처리 접근 방식이다.

OLTP와 OLAP는 데이터베이스 및 데이터 처리 요구 사항에 따라 서로 다른 목적을 가지고 있으며, 다른 유형의 시스템 및 데이터베이스 구조를 필요로 한다.

OLTP는 실시간 트랜잭션 처리를 중심으로 하고, OLAP는 데이터 분석과 의사 결정 지원을 중심으로 하며, 이러한 시스템은 조직 내에서 데이터 관리와 활용을 최적화하기 위해 함계 사용될 수 있다.
## OLTP(Online Transaction Processing)
**용도**
- OLTP 시스템은 주로 실시간 트랜잭션 처리를 위해 설계되었다. 일상적인 업무 작업을 수행하며 데이터베이스에 데이터를 추가, 수정, 삭제 및 조회하는데 사용된다.

**특징**
- 작은 트랜잭션 단위: OLTP 시스템에서는 작은 데이터 조작 작업이 반복적으로 발생한다.
- 높은 동시성: 다수의 사용자가 동시에 OLTP 시스템에 액세스하여 데이터를 조작할 수 있어야 한다.
- 실시간 응답: 사용자가 트랜잭션을 요청하면 빠른 응답이 필요하다.
- 정확한 데이터: 데이터의 일관성과 정확성이 매우 중요하다.

**예시**
- 은행 ATM 트랜잭션, 온라인 주문 처리, 예약 시스템 등
## OLAP(Online Analytical Processing)
**용도**
- OLAP 시스템은 주로 데이터 분석 및 의사 결정 지원을 위해 설계되었다. 대규모 데이터를 집계, 분석하고 다차원 데이터베이스에서 질의를 실행하여 BI 및 데이터 마이닝 작업을 수행한다.

**특징**
- 대규모 데이터 집계: OLAP 시스템은 대량의 데이터를 집계하고 다차원 데이터베이스에서 데이터 큐브를 생성한다.
- 복잡한 분석: 사용자는 다양한 분석 작업을 수행하고 데이터를 탐색할 수 있어야 한다.
- 의사 결정 지원: OLAP는 의사 결정을 지원하고 BI 작업을 수행하는데 중요한 역할 한다.
- 데이터 요약: 데이터 큐브는 데이터의 요약 버전을 제공하며 복잡한 질의에 빠르게 응답할 수 있도록 도와준다.

**예시**
- 판매 분석, 재고 관리, 시장 조사 등