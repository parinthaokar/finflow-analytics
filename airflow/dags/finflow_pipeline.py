import os
import snowflake.connector
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from datetime import datetime, timedelta


def alert_on_failure(context):
    task_id = context['task_instance'].task_id
    dag_id = context['dag'].dag_id
    execution_date = context['execution_date']
    exception = context.get('exception')
    print(f"""
    PIPELINE FAILURE ALERT
    DAG: {dag_id}
    Task: {task_id}
    Time: {execution_date}
    Error: {exception}
    """)


def decide_path():
    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse='COMPUTE_WH',
        database='FINFLOW',
        schema='GOLD'
    )
    cursor = conn.cursor()
    query = '''
        SELECT COUNT(CASE WHEN is_fraud = TRUE THEN 1 END) * 100.0 / COUNT(*) as fraud_rate
        FROM FINFLOW.GOLD.FRAUD_SCORES
        WHERE processed_at > DATEADD(hour, -1, CURRENT_TIMESTAMP())
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    fraud_rate = result[0]
    conn.close()

    if fraud_rate > 15:
        return 'send_fraud_alert'
    else:
        return 'pipeline_complete'


def send_fraud_alert():
    print("ALERT: High fraud rate detected this hour. Manual review required.")


def pipeline_complete():
    print("Pipeline completed successfully. Fraud rate within normal range.")


default_args = {
    'owner': 'finflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': alert_on_failure
}

with DAG(
    dag_id='finflow_processed',
    default_args=default_args,
    description='FinFlow fraud detection pipeline with branching and alerting',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2026, 6, 1),
    catchup=False
) as dag:

    run_staging = BashOperator(
        task_id='run_staging',
        bash_command='cd /opt/airflow/dbt_finflow && dbt run --select "path:models/staging/+" --profiles-dir /opt/airflow/dbt_finflow'
    )

    run_silver = BashOperator(
        task_id='run_silver',
        bash_command='cd /opt/airflow/dbt_finflow && dbt run