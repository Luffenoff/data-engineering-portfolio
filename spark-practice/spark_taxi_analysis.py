from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col


spark = (
    SparkSession.builder
    .appName("TaxiDataAnalysis")
    .master("local[*]")
    .getOrCreate()
)


df = spark.read.parquet("yellow_tripdata_2023-12.parquet")


print(f"Total rows: {df.count()}")
df.printSchema()


spark.stop()