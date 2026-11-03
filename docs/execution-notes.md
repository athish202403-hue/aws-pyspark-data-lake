# Execution Notes and Evidence

These notes summarize the uploaded Spark terminal, S3 console, and Athena screenshots.

## Spark processing steps shown

1. Started a Spark session for the Royal Orchid Data Lake job.
2. Read the orders and restaurant datasets from the Bronze layer.
3. Reviewed the orders DataFrame and its schema.
4. Converted `order_date` to a date, `sales_qty` to an integer, and `sales_amount` to a double.
5. Wrote the Silver orders dataset as Parquet partitioned by `order_date`.
6. Wrote the restaurant dataset to the Silver layer as Parquet.
7. Joined the Silver orders and restaurant datasets using `r_id`.
8. Grouped the enriched data by date and restaurant fields and calculated order count, quantity, and revenue.
9. Wrote Gold daily metrics as partitioned Parquet.

## S3 locations in the pipeline

| Layer | S3 prefix |
|---|---|
| Bronze orders | `s3a://athi-bronze/orders/` |
| Bronze restaurants | `s3a://athi-bronze/restaurant/` |
| Silver orders | `s3a://athi-silver/orders/` |
| Silver restaurants | `s3a://athi-silver/restaurant/` |
| Gold daily metrics | `s3a://athi-gold/daily_metrics/` |

The uploaded S3 console screenshots show the Bronze, Silver, and Gold data locations and date-partitioned output.

## Athena table and query evidence

The Athena screenshots show successful queries against:

`food_analytics.daily_restaurant_metrics`

The demonstrated analyses include:
- Previewing the Gold metrics table.
- Aggregating revenue by city.
- Aggregating revenue by restaurant.
- Calculating daily revenue.

The result values transcribed from those screenshots are documented in [athena-results.md](athena-results.md). The corresponding SQL files are in the [sql directory](../sql/).

## Source-file note

The uploaded `orders.csv` and `restaurant.csv` attachments contained placeholder text, not the actual records. The sample files under `data/sample/` were therefore transcribed from the rows visible in the Spark terminal screenshot. They are examples reconstructed from the screenshot, not byte-for-byte copies of the original source files.
