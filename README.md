# Royal Orchid Data Lake Project

AWS S3 and PySpark data lake implementing the **Bronze → Silver → Gold** architecture.

## Project overview

The project processes orders and restaurant CSV data through three data lake layers. The PySpark job reads the raw files from Amazon S3, applies type conversions, stores the Silver datasets in Parquet, enriches orders with restaurant information, and produces aggregated daily metrics in the Gold layer.

## Architecture

```text
Orders CSV ───────┐
                  ├──> S3 Bronze ──> PySpark ETL ──> S3 Silver (Parquet)
Restaurant CSV ───┘                                  │
                                                    v
                                         Join + daily aggregations
                                                    │
                                                    v
                                         S3 Gold (daily metrics)
```

## Medallion layers

### Bronze — Raw data

The job reads the source CSV datasets from:

- `s3a://athi-bronze/orders/`
- `s3a://athi-bronze/restaurant/`

### Silver — Cleaned data

The orders dataset is standardized by converting `order_date` to a date, `sales_qty` to an integer, and `sales_amount` to a double. Orders are written as Parquet partitioned by `order_date`. Restaurant data is also written as Parquet.

Output locations:

- `s3a://athi-silver/orders/`
- `s3a://athi-silver/restaurant/`

### Gold — Aggregated metrics

The pipeline joins Silver orders with Silver restaurant data using `r_id`, then groups by order date and restaurant attributes. It calculates:

- `total_orders`
- `total_quantity`
- `total_revenue`

The Gold output is written as Parquet partitioned by `order_date` to:

- `s3a://athi-gold/daily_metrics/`

## Source code

- [`royal_orchid_etl.py`](royal_orchid_etl.py) — uploaded PySpark ETL pipeline.

## Technologies used

- Amazon S3
- PySpark
- Python
- Apache Parquet
- Partitioning
- Medallion Data Lake Architecture

## Run the pipeline

Run the script from a Spark environment configured with access to the S3 locations and the S3A connector:

```bash
spark-submit royal_orchid_etl.py
```

The Spark environment must have compatible Hadoop AWS / S3A dependencies and AWS credentials or an IAM role that can access the Bronze, Silver, and Gold prefixes.

## Important notes

- The script writes output using `mode("overwrite")`, so existing data at the Silver and Gold output paths will be replaced on each run.
- The source files must contain the columns referenced by the script: orders (`order_date`, `sales_qty`, `sales_amount`, `r_id`) and restaurants (`r_id`, `name`, `cuisine`, `city`).
- This repository contains the uploaded script and project documentation. Dataset files and execution screenshots were not present among the project files I located.
- Never commit AWS access keys, secret keys, or private datasets.

## Author

Athish
