# JOIN
형식이 다른 두 테이블을 하나로 만드는 행위로, 조건이 맞는 두 테이블의 튜플을 하나로 이어 붙여 새로운 튜플을 생성한다.

일반적으로 두 테이블은 PK와 FK의 관계에 의해 JOIN이 성립된다.
# Inner JOIN
특정 컬럼의 동일한 튜플에 대해 JOIN하며 동일한 값을 가진 레코드만 반환된다.
# Natural JOIN
방식 자체는 Inner JOIN과 동일하지만 JOIN 속성을 표시하지 않는다. 이때 동일한 속성이 여러번 나오게 되는데 중복되는 속성을 제거하는 방식이다.
# OUTER JOIN
## LEFT OUTER JOIN
LEFT OUTER JOIN은 좌측 테이블의 모든 행을 포함하고, 우측 테이블에서 해당하는 값이 있는 경우에만 연결한다.

우측 테이블에 일치하는 값이 없는 경우에도 결과에는 좌측 테이블의 모든 행이 포함되며, 이때 값이 없는 경우 Null로 대체된다.
## RIGHT OUTER JOIN
RIGHT OUTER JOIN은 우측 테이블의 모든 행을 포함하고, 좌측 테이블에서 해당하는 값이 있는 경우에만 연결한다.

좌측 테이블에 일치하는 값이 없는 경우에도 결과에는 우측 테이블의 모든 행이 포함되며, 이때 값이 없는 경우 Null로 대체된다.
## FULL OUTER JOIN
FULL OUTER JOIN은 두 테이블 간의 모든 행을 포함하며, 일치하는 값이 없는 경우에도 모든 행을 반환한다.
# CROSS JOIN
Cartesain Product라고도 하며 두 테이블의 모든 가능한 조합을 생성한다.

상호 조인 결과의 전체 행 개수는 두 테이블의 각 행의 개수를 곱한 수만큼 된다.
# SELF JOIN
한 테이블 내에서 서로 다른 행을 결합하는데 사용한다. 실행하는 JOIN으로 테이블에 서로 다른 alias를 주어 실행한다.
