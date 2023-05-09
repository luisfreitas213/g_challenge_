# Import necessary libraries and classes
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 8),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

# Define the DAG itself
dag = DAG(
    'transactions',
    default_args=default_args,
    schedule_interval='30 0 * * *' # Run every day at 00:30
)

# Define the main process as a Python function
def ingestion():
    #Import Script
    import ingestion.parquet_ingestion as pi
    
    table_name = 'Transactions'
    column_delta = 'timestamp'
    connection_source = 'mysql+pymysql://root:my-secret-pw@172.19.0.8/db_g'
    
    # Call the "parquet_ingestion" function from the "ingestion" module, passing the required parameters
    pi.parquet_ingestion(connection_source, table_name, column_delta)
    
def consolidation():
    import consolidation.exec_spark as es
    raw_table = 'Transactions'
    dw_table = 'Transactions'
    partition = 'client_id'
    script = '~/workspace/g_challange/airflow/dags/consolidation/spark_scripts/partition_parquet_append.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script, a=raw_table, b=dw_table, c=partition)
    
    # Move the raw data to a history folder
    es.move_raw(raw_table)

# Define a PythonOperator that will execute the "ingestion" function
ingestion_Transactions = PythonOperator(
    task_id='ing_transactions',
    python_callable=ingestion,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
consolidation_Transactions = PythonOperator(
    task_id='trf_transactions',
    python_callable=consolidation,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Set up the dependency between the two tasks
ingestion_Transactions >> consolidation_Transactions
