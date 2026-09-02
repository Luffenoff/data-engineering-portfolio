from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col, round as spark_round


spark = (
    SparkSession.builder
    .appName("TaxiDataAnalysis")
    .master("local[*]")
    .getOrCreate()
)


df = spark.read.parquet("yellow_tripdata_2023-12.parquet")

# DataFrame API
vendor_stats =(
    df.groupBy("VendorID")
    .agg(
        count("*").alias("trip_count"),
        spark_round(avg("fare_amount"), 2).alias("avg_fare")
    )
    .orderBy("VendorID")
)


print("DataFrame API result")
vendor_stats.show()


# Spark SQL
df.createOrReplaceTempView("trips")

result_sql = spark.sql("""
    SELECT
        VendorID,
        Count(*) as trip_count,
        ROUND(AVG(fare_amount), 2) as avg_fare
    FROM trips
    GROUP BY VendorID
    ORDER BY VendorID
""")


print("=== Spark SQL result ===")
result_sql.show()
vendor_stats.explain(True)


spark.stop()