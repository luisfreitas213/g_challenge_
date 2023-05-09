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
    'sensors',
    default_args=default_args,
    schedule_interval='30 0 * * *' # Run every day at 00:30
)

# Define the main process as a Python function
def ingestion():
    #Import Script
    import ingestion.parquet_ingestion as pi
    
    table_name = 'Sensors'
    column_delta = 'timestamp'
    connection_source = 'mysql+pymysql://root:my-secret-pw@172.19.0.8/db_g'
    
    # Call the "parquet_ingestion" function from the "ingestion" module, passing the required parameters
    pi.parquet_ingestion(connection_source, table_name, column_delta)
    
def consolidation():
    import consolidation.exec_spark as es
    raw_table = 'Sensors'
    dw_table = 'Sensors'
    partition = 'YEAR'
    script = '~/workspace/g_challange/airflow/dags/consolidation/spark_scripts/partition_parquet_append.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script, a=raw_table, b=dw_table, c=partition)
    
    # Move the raw data to a history folder
    es.move_raw(raw_table)
    
def agg_sensors_total_rows():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_sensors_total_rows.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    
def agg_sensors_total_rows_ppl340():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_sensors_total_rows_ppl340.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    
def agg_sensors_total_rows_ppl340_by_year():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_sensors_total_rows_ppl340_by_year.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    
def agg_distinct_sensors():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_distinct_sensors.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    
def agg_count_less_avg_by_year_ppl340():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_count_less_avg_by_year_ppl340.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    
def agg_average_ppl340_by_year():
    import consolidation.exec_spark as es
    script = '~/workspace/g_challange/airflow/dags/aggregation/Sensors/agg_average_ppl340_by_year.py'
    
    # Call the "execution_spark" function from the "exec_spark" module, passing the required parameters
    es.execution_spark(spark_script=script)
    

# Define a PythonOperator that will execute the "ingestion" function
ingestion_Sensors = PythonOperator(
    task_id='ing_Sensors',
    python_callable=ingestion,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
consolidation_Sensors = PythonOperator(
    task_id='trf_Sensores',
    python_callable=consolidation,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_sensors_total_rows = PythonOperator(
    task_id='agg_sensors_total_rows',
    python_callable=agg_sensors_total_rows,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_sensors_total_rows_ppl340 = PythonOperator(
    task_id='agg_sensors_total_rows_ppl340',
    python_callable=agg_sensors_total_rows_ppl340,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_sensors_total_rows_ppl340_by_year = PythonOperator(
    task_id='agg_sensors_total_rows_ppl340_by_year',
    python_callable=agg_sensors_total_rows_ppl340_by_year,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_distinct_sensors = PythonOperator(
    task_id='agg_distinct_sensors',
    python_callable=agg_distinct_sensors,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_count_less_avg_by_year_ppl340 = PythonOperator(
    task_id='agg_count_less_avg_by_year_ppl340',
    python_callable=agg_count_less_avg_by_year_ppl340,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

# Define a PythonOperator that will execute the "consolidation" function
agg_average_ppl340_by_year = PythonOperator(
    task_id='agg_average_ppl340_by_year',
    python_callable=agg_average_ppl340_by_year,
    trigger_rule='one_success', # Define the trigger rule for the task
    dag=dag # Assign the DAG to the task
)

ingestion_Sensors >> consolidation_Sensors
consolidation_Sensors >> agg_sensors_total_rows
consolidation_Sensors >> agg_sensors_total_rows_ppl340
consolidation_Sensors >> agg_sensors_total_rows_ppl340_by_year
consolidation_Sensors >> agg_distinct_sensors
consolidation_Sensors >> agg_count_less_avg_by_year_ppl340
consolidation_Sensors >> agg_average_ppl340_by_year
