from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(
    'spark_simple_dag',
    default_args=default_args,
    description='A simple DAG to run Spark job',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Spark 작업 실행
spark_task = SparkSubmitOperator(
    task_id='spark_task',
    application="/usr/local/spark/app/script.py",  # Spark 코드가 저장된 경로
    conn_id='spark_default',  # 여기서 지정한 id로 Spark Connection에 사용
    dag=dag,
)

spark_task
