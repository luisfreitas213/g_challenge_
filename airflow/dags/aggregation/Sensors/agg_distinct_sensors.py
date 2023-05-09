from pyspark.sql import SparkSession

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark agg_distinct_sensors").getOrCreate()

# Read Parquet files from HDFS into a DataFrame
df = spark.read.parquet(f"hdfs:///dw/Sensors/")

# Filter Sensor Name
df = df.select('sensor_name').distinct()

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.mode("overwrite").parquet(f"hdfs:///agg/agg_distinct_sensors/")

# Display the result
df.show()