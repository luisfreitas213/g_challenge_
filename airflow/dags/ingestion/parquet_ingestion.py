# Data Source Connection 

from sqlalchemy import create_engine
import pandas as pd  
import os      
import time
from datetime import datetime


def parquet_ingestion(connection_source, table_name, column_delta):
    # create a SQLAlchemy engine object for connecting to the database
    sqlEngine = create_engine(connection_source, pool_recycle=3600)

    # connect to the database using the engine object
    dbConnection = sqlEngine.connect()

    try:
        # read the maximum delta execution date for the current process from the Control_ingestion table
        df_control_ingestion = pd.read_sql(f"select max(delta_execution) as max_date from db_g.Control_ingestion where process_name = '{table_name}'", dbConnection);
        # extract the max_date value from the dataframe
        max_date = df_control_ingestion["max_date"][0]
        
        # if there is no previous delta execution date, ingest all data from the table
        if max_date == None:
            df = pd.read_sql(f"select * from db_g.{table_name}", dbConnection);
            
        # otherwise, ingest only the rows with a delta value greater than the maximum date
        else:
            df = pd.read_sql(f"select * from db_g.{table_name} where {column_delta} > '{df_control_ingestion['max_date'].iat[0]}'", dbConnection);
        
        # print the dataframe
        print(df)
    
    # handle any value errors that occur during the execution of the try block
    except ValueError as vx:
        print(vx)
    
    # handle any other exceptions that occur during the execution of the try block
    except Exception as ex:
        print(ex)
    
    # if no exceptions occur during the execution of the try block
    else:
        if not df.empty:
            
            # Ingestion data 
            # ts stores the time in seconds
            # get the current timestamp in seconds
            ts = time.time()
            
            # write the dataframe to a parquet file
            df.to_parquet(f'~/workspace/g_challange/airflow/dags/ingestion/tmp_files/{table_name}_{str(ts)}.parquet')

            # copy the parquet file to HDFS using the Hadoop command line tool
            os.system(f"~/hadoop-3.3.1/bin/hdfs dfs -put ~/workspace/g_challange/airflow/dags/ingestion/tmp_files/{table_name}_{str(ts)}.parquet /raw/{table_name}/{table_name}_{str(ts)}.parquet")

            # remove the temporary parquet file from the local filesystem
            os.system(f"rm ~/workspace/g_challange/airflow/dags/ingestion/tmp_files/{table_name}_{str(ts)}.parquet")
        
            # record the new maximum delta execution date and the filename in the Control_ingestion table
            new_max_data = str(df['timestamp'].max())
            parameters = [datetime.now(), table_name, f"{new_max_data}", f"{table_name}_{str(ts)}"]
            dbConnection.execute(f'INSERT INTO db_g.Control_ingestion ' \
                                f'(timestamp, process_name, delta_execution, file_generated) ' \
                                f'VALUES (%s,%s,%s,%s)', parameters);
            
            # close the database connection
            dbConnection.close();
            
            # print a success message
            print("successfully"); 
            
        # if no new data was ingested, print a message indicating that
        else:
            print("not new data")
        

