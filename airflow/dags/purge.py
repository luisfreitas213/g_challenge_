from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 1),
    'retries': 0
}

dag = DAG(
    'purge',
    default_args=default_args,
    schedule_interval=timedelta(days=183)  # run every 6 months (183 days)
)

t1 = BashOperator(
    task_id='transactions',
    bash_command='~/workspace/g_challange/airflow/dags/purge/transactions_del_182.sh',
    dag=dag
)

t2 = BashOperator(
    task_id='sensors',
    bash_command='~/workspace/g_challange/airflow/dags/purge/sensors_del_182.sh',
    dag=dag
)

t1
t2
