from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'finflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='finflow_processed', 
    default_args=default_args,
    description='FinFlow fraud detection pipeline',
    schedule_interval= timedelta(hours=1),  # run every hour
    start_date=datetime(2026, 6, 1),
    catchup=False
) as dag:

    run_staging = BashOperator(
        task_id='run_staging',
        bash_command='cd /opt/airflow/dbt_finflow && dbt run --select "path:models/staging/+" --profiles-dir /opt/airflow/dbt_finflow'
    )

    run_silver = BashOperator(
        task_id='run_silver',
        bash_command='cd /opt/airflow/dbt_finflow && dbt run --select "path:models/silver/+"'  
    )

    run_gold = BashOperator(
        task_id='run_gold',
        bash_command='cd /opt/airflow/dbt_finflow && dbt run --select "path:models/gold/+"' 
    )

    run_staging >> run_silver >> run_gold