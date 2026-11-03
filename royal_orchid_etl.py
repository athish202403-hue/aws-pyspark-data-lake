from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum as _sum, count as _count

spark = SparkSession.builder.appName("Royal Orchid Data Lake").getOrCreate()

# Read Bronze
orders = spark.read.option("header", "true").csv("s3a://athi-bronze/orders/")
restaurants = spark.read.option("header", "true").csv("s3a://athi-bronze/restaurant/")

# Silver Transformation
orders_silver = (
    orders
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("sales_qty", col("sales_qty").cast("int"))
    .withColumn("sales_amount", col("sales_amount").cast("double"))
)

orders_silver.write.mode("overwrite").partitionBy("order_date").parquet(
    "s3a://athi-silver/orders/"
)

restaurants.write.mode("overwrite").parquet("s3a://athi-silver/restaurant/")

# Gold Layer
orders_s = spark.read.parquet("s3a://athi-silver/orders/")
restaurants_s = spark.read.parquet("s3a://athi-silver/restaurant/")

orders_enriched = (
    orders_s.alias("o")
    .join(
        restaurants_s.alias("r"),
        col("o.r_id") == col("r.r_id"),
        "left",
    )
    .select(
        col("o.order_date"),
        col("o.r_id"),
        col("o.sales_qty"),
        col("o.sales_amount"),
        col("r.name"),
        col("r.cuisine"),
        col("r.city"),
    )
)

gold = (
    orders_enriched
    .groupBy("order_date", "r_id", "name", "cuisine", "city")
    .agg(
        _count("*").alias("total_orders"),
        _sum("sales_qty").alias("total_quantity"),
        _sum("sales_amount").alias("total_revenue"),
    )
)

gold.write.mode("overwrite").partitionBy("order_date").parquet(
    "s3a://athi-gold/daily_metrics/"
)

spark.stop()
