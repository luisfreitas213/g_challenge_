#!/bin/bash

# Set the HDFS directory you want to clean up
dir=/raw_history/Sensors/

# Calculate the timestamp for six months ago
timestamp=$(date -d "6 months ago" +%s)

# List all files in tThe directory and filter by files older than six months
files=$(~/hadoop-3.3.1/bin/hdfs dfs -ls $dir | grep "^-" | awk -v timestamp="$timestamp" '{if ($6 < timestamp) print $NF}')

# Loop through each file and delete it
for file in $files; do
  ~/hadoop-3.3.1/bin/hdfs dfs -rm $file
  echo "Deleted file: $file"
done

echo "Cleanup complete!"

