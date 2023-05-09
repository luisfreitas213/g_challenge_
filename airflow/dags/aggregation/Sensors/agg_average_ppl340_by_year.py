from pyspark.sql import SparkSession

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark agg_average_ppl340_by_year").getOrCreate()

# Read Parquet files from HDFS into a DataFrame
df = spark.read.parquet(f"hdfs:///dw/Sensors/")

# Create a temporary view of the DataFrame
df.createTempView("Sensors")

# Compute the total number of rows in the DataFrame
df = spark.sql("Select YEAR, AVG(sensor_value) as avg_ppl340 from Sensors where sensor_name = 'PPL340' GROUP BY YEAR;")

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.mode("overwrite").parquet(f"hdfs:///agg/agg_average_ppl340_by_year/")

# Display the result
df.show()
