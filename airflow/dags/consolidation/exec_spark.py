import os   

def execution_spark(spark_script, **kwargs):
    '''This function takes in a Spark script path and any number of keyword arguments that
    will be passed to the script when it's executed. The function then constructs a command to
    execute the Spark script using the spark-submit command with the yarn resource manager
    and dev queue. It then loops through all the keyword arguments and appends them to the command as strings.
    Finally, it executes the command using the os.system() method.'''
    
    # Define the command to execute the spark script with yarn in the 'dev' queue
    command = f"~/spark-3.2.0-bin-hadoop3.2/bin/spark-submit --master yarn --queue dev {spark_script}"
    
    # Loop through all the keyword arguments passed in and append them to the command as strings
    for arg in kwargs.values():
        command += f" '{str(arg)}'"
        
    # Execute the command using the os.system() method
    os.system(command)
    
    
def move_raw(table_name):
    '''This function moves all the Parquet files from the /raw/{table_name}
    directory in HDFS to the /raw_history/{table_name}
    directory using the hdfs dfs -mv command in the shell.'''
    
    # Move files from /raw/{table_name} to /raw_history/{table_name}
    # using HDFS command in the shell
    os.system(f"~/hadoop-3.3.1/bin/hdfs dfs -mv /raw/{table_name}/*.parquet /raw_history/{table_name}/")