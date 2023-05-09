from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, max, count

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark agg_count_less_avg_by_year_ppl340").getOrCreate()

# Read Parquet files from HDFS into a DataFrame and filter by sensor name
df = spark.read.parquet(f"hdfs:///dw/Sensors/").filter("sensor_name = 'PPL340'")

# Group by year and calculate count and average of sensor values
df = df.groupBy("YEAR").agg(count("sensor_value").alias("count_sensor_value"), avg("sensor_value").alias("avg_sensor_value"))

# Filter the data where the count of sensor values is less than the average sensor value
df = df.filter("count_sensor_value < avg_sensor_value ")

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.mode("overwrite").parquet(f"hdfs:///agg/agg_count_less_avg_by_year_ppl340/")

# Display the result
df.show()
