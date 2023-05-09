from pyspark.sql import SparkSession
import sys

# Create a SparkSession with a specific application name
spark = SparkSession.builder.appName(f"Spark {sys.argv[1]}").getOrCreate()

# Read Parquet files from HDFS into a DataFrame
df = spark.read.parquet(f"hdfs:///raw/{sys.argv[1]}/")

# Write the DataFrame partitioned by a specific column in append mode into HDFS as Parquet files
df.write.partitionBy(f"{sys.argv[3]}").mode("append").parquet(f"hdfs:///dw/{sys.argv[2]}/")
