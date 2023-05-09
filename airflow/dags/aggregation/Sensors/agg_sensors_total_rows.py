from pyspark.sql import SparkSession

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark agg_sensors_total_rows").getOrCreate()

# Read Parquet files from HDFS into a DataFrame
df = spark.read.parquet(f"hdfs:///dw/Sensors/")

# Create a temporary view of the DataFrame
df.createTempView("Sensors")

# Compute the total number of rows in the DataFrame
df = spark.sql("select count(1) as Total_Rows from Sensors").cache()

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.mode("overwrite").parquet(f"hdfs:///agg/agg_sensors_total_rows/")

# Display the result
df.show()
