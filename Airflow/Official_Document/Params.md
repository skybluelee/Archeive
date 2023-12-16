**본 문서는 Airflow 공식 문서 [Params](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/params.html)를 참조함**
# Params
Params는 작업에 런타임 구성을 제공하는 데 사용된다.
DAG 코드에서 기본 Params를 구성하고 DAG를 트리거할 때 추가적인 Params를 제공하거나 Param 값을 런타임에 덮어쓸 수 있다. 
Param 값은 JSON Schema로 유효성이 검증된다. 
예약된 DAG 실행의 경우 기본 Param 값이 사용된다.

또한 정의된 Params는 수동으로 트리거할 때 멋진 UI를 렌더링하는 데 사용된다.
DAG를 수동으로 트리거하면 dag run이 시작되기 전에 Params를 수정할 수 있다. 
사용자가 제공한 값이 유효성 검사를 통과하지 않으면 Airflow은 dagrun을 생성하는 대신 경고를 표시한다.

# DAG-level Params
```
 from airflow import DAG
 from airflow.models.param import Param

 with DAG(
     "the_dag",
     params={
         "x": Param(5, type="integer", minimum=3),
         "my_int_param": 6
     },
 ):
```
DAG에 Params를 추가하기 위해서는, `params` kwarg를 사용하여 초기화해야 한다.
Params 이름을 Params 혹은 Params의 기본값을 가리키는 객체와 맵핑하는 딕셔너리를 사용하라.

# Task-level Params
```
def print_my_int_param(params):
  print(params.my_int_param)

PythonOperator(
    task_id="print_my_int_param",
    params={"my_int_param": 10},
    python_callable=print_my_int_param,
)
```
각각의 task에 Params를 추가할 수도 있다.

task 수준의 Params는 DAG 수준의 Params보다 우선하며 사용자가 DAG를 트리거할 때 제공한 Params는 task 수준의 Params보다 우선한다.

# Referencing Params in a Task
```
 PythonOperator(
     task_id="from_template",
     op_args=[
         "{{ params.my_int_param + 10 }}",
     ],
     python_callable=(
         lambda my_int_param: print(my_int_param)
     ),
 )
```
Params는 `params` 내에서 [templated strings](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#templates-ref)으로 참조될 수 있다.
***
```
 with DAG(
     "the_dag",
     params={"my_int_param": Param(5, type="integer", minimum=3)},
     render_template_as_native_obj=True
 ):
```
Params는 여러 유형을 사용할 수 있지만 템플릿의 기본 동작은 작업에 문자열을 제공하는 것이다.
DAG를 초기화할 때 `render_template_as_native_obj=True`로 설정하여 이 동작을 변경할 수 있다.
***
```
# prints <class 'str'> by default
# prints <class 'int'> if render_template_as_native_obj=True
PythonOperator(
    task_id="template_type",
    op_args=[
        "{{ params.my_int_param }}",
    ],
    python_callable=(
        lambda my_int_param: print(type(my_int_param))
    ),
)
```
위와 같은 방식으로 task에 제공되는 Param의 유형이 존중된다.
***
```
 def print_my_int_param(**context):
     print(context["params"]["my_int_param"])

 PythonOperator(
     task_id="print_my_int_param",
     python_callable=print_my_int_param,
     params={"my_int_param": 12345},
 )
```
params에 접근하는 또다른 방법은 task의 `context` kwarg를 통해 접근하는 것이다.

# JSON Schema Validation
```
with DAG(
    "my_dag",
    params={
        # an int with a default value
        "my_int_param": Param(10, type="integer", minimum=0, maximum=20),

        # a required param which can be of multiple types
        # a param must have a default value
        "multi_type_param": Param(5, type=["null", "number", "string"]),

        # an enum param, must be one of three values
        "enum_param": Param("foo", enum=["foo", "bar", 42]),

        # a param which uses json-schema formatting
        "email": Param(
            default="example@example.com",
            type="string",
            format="idn-email",
            minLength=5,
            maxLength=255,
        ),
    },
):
```
Params는 [JSON 스키마](https://json-schema.org/)를 사용하며, `Param` 객체를 정의하기 위해 [전체 스키마 사양](https://json-schema.org/draft/2020-12/json-schema-validation.html)을 사용할 수 있다.

참조 - 현재 보안 상의 이유로 사용자 정의 클래스에서 파생된 Param 객체를 사용할 수 없다. Airflow에서 Operator ExtraLinks와 마찬가지로 사용자 정의 Param 클래스를 등록하는 시스템을 계획 중이다.

# Use Params to Provide a Trigger UI Form
DAG 레벨 Params는 사용자 친화적인 트리거 폼을 렌더링하는 데 사용된다.
이 폼은 사용자가 "Trigger DAG" 버튼을 클릭할 때 제공된다.

트리거 UI 폼은 미리 정의된 DAG Params를 기반으로 렌더링된다.
DAG에 정의된 Params가 없으면 트리거 폼이 스킵된다.
폼 요소는 Param 클래스를 사용하여 정의하며 속성은 어떻게 폼 필드가 표시되는지를 정의한다.

다음 기능이 트리거 UI 폼에서 지원된다.
- 최상위 DAG Params에서 직접 스칼라 값(부울, 정수, 문자열, 리스트, 딕셔너리)은 자동으로 Param 객체로 맵핑된다.
네이티브 Python 데이터 유형에서는 `type` 속성이 자동으로 감지된다.
따라서 이러한 간단한 유형은 해당 필드 유형으로 렌더링됩니다.
매개변수의 이름은 label로 사용되며 추가 검증은 이루어지지 않는다.
모든 값은 선택적으로 처리됩니다.
- 매개변수 값의 정의로 Param 클래스를 사용하는 경우 다음 속성을 추가할 수 있다.
    - Param 속성 `title`은 엔트리 상자의 폼 필드 레이블로 사용된다. `title`이 정의되지 않은 경우 매개변수 이름/키 대신 사용된다.    
    - Param 속성 `description`은 엔트리 필드 아래에 회색으로 도움말 텍스트로 렌더링된다.
      특별한 형식이나 링크를 위해 HTML 태그를 제공하려면 Param 속성 `description_html`을 사용해야 한다. 예시는 튜토리얼 DAG `example_params_ui_tutorial`에서 확인할 수 있다.    
    - Param 속성 `type`은 필드가 어떻게 렌더링되는지에 영향을 미친다. 아래의 표에 지원 유형을 확인할 수 있다.
    - 폼 필드가 비어 있으면 해당 필드는 Params 딕셔너리에 `None` 값으로 전달된다.
    - 폼 필드는 DAG의 Params 정의 순서대로 렌더링된다.
    - 폼에 섹션을 추가하려면 각 필드에 `section` 속성을 추가하라. 텍스트는 섹션 레이블로 사용된다. `section`이 없는 필드는 기본 영역에서 렌더링된다. 기본적으로 추가 섹션은 축소된다.
    - 표시되지 않아야 하는 Params가 있다면 `const` 속성을 사용하라. 이러한 Params는 제출되지만 폼에서 숨겨진다.
      `const` 값은 [JSON Schema 유효성 검사](https://json-schema.org/understanding-json-schema/reference/generic.html#constant-values)를 통과하려면 기본값과 일치해야 합니다.
    - 폼 하단에 생성된 JSON 구성을 확장할 수 있다. 값을 수동으로 변경하려면 JSON 구성을 조정해야 한다. 폼 필드가 변경될 때 변경 사항이 덮어씌워진다.
    - 제공된 기능 위에 사용자 정의 HTML을 폼으로 렌더링하려면 `custom_html_form` 속성을 사용할 수 있다.

|Param type|Form element type|Additional supported attributes|Example|
|-|-|-|-|
|`string`|텍스트를 수정하기 위해 <br> 한 줄의 텍스트 박스를 생성한다.|- `minLength`: 텍스트의 최소 길이. <br>- `maxLength`: 텍스트의 최대 길이. <br>- `format="date"`: 달력 팝업이 있는 날짜 선택기 생성. <br>- `format="datetime"`: 달력 팝업이 있는 날짜 및 시간 선택기 생성. <br>- `format="time"`: 시간 선택기 생성. <br>- `enum=["a", "b", "c"]`: 스칼라 값에 대한 드롭다운 선택 목록 생성. JSON 유효성 검사에 따라, 값이 선택되어야 하거나 필드를 명시적으로 선택 가능하게 표시. Enum에 대한 자세한 내용은 [JSON Schema Description for Enum](https://json-schema.org/understanding-json-schema/reference/generic.html#enumerated-values) 참조. <br>- `values_display={"a": "Alpha", "b": "Beta"}`: enum을 통해 생성된 선택 드롭다운에 데이터 값과 표시 레이블을 매핑하는 dict와 함께 `values_display` 속성을 추가. <br>- `examples=["One", "Two", "Three"]`: 사용자에게 특정 값 제안을 제시하려면(위의 고정된 enum으로 사용자를 제한하지 않음) examples를 사용할 수 있음. <br> <br> 백엔드에서 DAG 트리거 전에 확인되는 추가 JSON Schema 문자열 유형 유효성 옵션에 대한 자세한 내용은 [JSON Schema 문서](https://json-schema.org/understanding-json-schema/reference/string.html)를 참조하라.|`Param("default", type="string", maxLength=10)` <br><br> `Param(f"{datetime.date.today()}", type="string", format="date")`|
|`number` 또는 `integer`|숫자 값을 제한하는 필드를 생성한다. 일반적으로 HTML 브라우저는 값을 증가 또는 감소시키기 위해 오른쪽에 스피너(spinner)를 추가한다. integer는 정수만 허용하며, number는 정수 및 소수값을 허용한다.|- `minimum`: 숫자 값의 최솟값 <br>- `maximum`: 숫자 값의 최댓값<br><br> 백엔드에서 DAG 트리거 전에 확인되는 [추가적인 JSON Schema 숫자 유형 유효성 옵션](https://json-schema.org/understanding-json-schema/reference/numeric.html)에 대한 자세한 내용은 JSON Schema 문서를 참조하라.|`Param(42, type="integer", minimum=14, multipleOf=7)`|
|`boolean`|`True` 또는 `False`에 사용되는 토글 버튼을 생성한다.|없음|`Param(True, type="boolean")`|
|`array`|HTML 다중 행 텍스트 필드를 생성하며, 편집된 각 행은 값으로 문자열 배열로 만들어진다.|- list와 함께 속성 `examples`를 추가하면 자유 텍스트 필드 대신에 다중 값 선택 옵션이 생성된다. <br>- `values_display={"a": "Alpha", "b": "Beta"}`: 다중 값 선택에 대한 `example`에는 속성 `values_display`를 추가하여 데이터 값을 표시 레이블로 매핑할 수 있다. <br>- 속성 `items`를 추가하면 더 많은 배열 유형 및 [JSON Schema 배열 항목](https://json-schema.org/understanding-json-schema/reference/array.html#items) 설명에 설명된 추가 유형 유효성 검사를 위해 JSON 항목 필드가 생성된다.|`Param(["a", "b", "c"], type="array")`<br><br>`Param(["two", "three"], type="array", examples=["one", "two", "three", "four", "five"])`|
|`object`|텍스트 유효성이 검증된 JSON 엔트리 필드를 생성한다.|HTML 폼은 JSON 입력의 구문만을 유효성 검사한다. 특정 구조의 내용을 검증하려면 [JSON Schema 오브젝트 세부 정보](https://json-schema.org/understanding-json-schema/reference/object.html)를 확인하라.|`Param({"key": "value"}, type=["object", "null"])`|
|`null`|내용이 예상되지 않음을 지정한다. 독립적으로는 이것이 많은 의미를 갖지 않지만, type 속성은 유형 목록도 허용하므로 `type=["null", "string"]`과 같은 유형 조합에 유용하다. 기본적으로 type을 지정하면 JSON 유효성 검사 때문에 필드가 필수로 설정된다. 필드 값을 선택 사항으로 추가하려면 null 값을 허용하는 JSON 스키마 유효성 검사를 허용해야 한다.||`Param(None, type=["null", "string"])`|
***
예제 DAG인 `example_params_trigger_ui`와 `example_params_ui_tutorial`도 확인하는 것이 좋다.
<img src="https://github.com/skybluelee/Archeive/assets/107929903/6f5c96fd-abb4-43fd-8a41-a5879d0a090e.png" width="1200" height="1500"/>

2.7.0 버전에 추가됨.

구성 스위치 `webserver.show_trigger_form_if_no_params`를 사용하면 Params가 정의되지 않은 경우에도 트리거 폼을 강제로 표시할 수 있다.

# Disabling Runtime Param Modification
DAG를 트리거하는 동안 Params를 업데이트할 수 있는 능력은 `core.dag_run_conf_overrides_params` 플래그에 달려 있다.
이 구성을 `False`로 설정하면 기본 Params가 상수로 변경되어 업데이트되지 않는다.
