from pyspark.sql import SparkSession

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark agg_sensors_total_rows_ppl340_by_year").getOrCreate()

# Read Parquet files from HDFS into a DataFrame
df = spark.read.parquet(f"hdfs:///dw/Sensors/")

# Filter Sensor Name
df = df.filter(" sensor_name = 'PPL340' ")

# Create a temporary view of the DataFrame
df.createTempView("Sensors")

# Compute the total number of rows in the DataFrame
df = spark.sql("Select YEAR, COUNT(1) as total_rows_ppl340 from Sensors GROUP BY YEAR").cache()

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.mode("overwrite").parquet(f"hdfs:///agg/agg_sensors_total_rows_ppl340_by_year/")

# Display the result
df.show()