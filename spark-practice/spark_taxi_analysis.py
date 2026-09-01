from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col, round as spark_round


spark = (
    SparkSession.builder
    .appName("TaxiDataAnalysis")
    .master("local[*]")
    .getOrCreate()
)


df = spark.read.parquet("yellow_tripdata_2023-12.parquet")


vendor_stats =(
    df.groupBy()
)


print(f"Total rows: {df.count()}")
df.printSchema()


spark.stop()