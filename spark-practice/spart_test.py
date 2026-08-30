from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("TaxiDataAnalysis")
    .master("local[*]")
    .getOrCreate()
)

print(f"Spark version: {spark.version}")
print(f"Spark UI available at: {spark.sparkContext.uiWebUrl}")

spark.stop()