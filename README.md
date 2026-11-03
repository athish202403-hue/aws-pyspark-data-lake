# Royal Orchid Data Lake Project

An AWS S3 and PySpark data lake implementing the **Bronze → Silver → Gold** Medallion Architecture. The project transforms order and restaurant data, stores optimized Parquet datasets, and supports analytics through Amazon Athena.

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
                                                    │
                                                    v
                                               Athena SQL
```

## Pipeline layers

### Bronze — Raw data

The PySpark job reads the source datasets from:

- `s3a://athi-bronze/orders/`
- `s3a://athi-bronze/restaurant/`

### Silver — Cleaned data

The job converts `order_date` to a date, `sales_qty` to an integer, and `sales_amount` to a double. It writes the orders data as Parquet partitioned by `order_date` and writes the restaurant data as Parquet.

- Orders: `s3a://athi-silver/orders/`
- Restaurants: `s3a://athi-silver/restaurant/`

### Gold — Aggregated metrics

The job joins orders with restaurant details using `r_id`, groups by order date and restaurant attributes, and calculates `total_orders`, `total_quantity`, and `total_revenue`.

- Gold output: `s3a://athi-gold/daily_metrics/`

Gold output is written in Parquet partitioned by `order_date`.

## Repository contents

| Path | Contents |
|---|---|
| `royal_orchid_etl.py` | Uploaded PySpark ETL job |
| `data/sample/orders.csv` | Small sample orders dataset transcribed from the uploaded Spark output screenshot |
| `data/sample/restaurant.csv` | Restaurant lookup sample transcribed from the uploaded Spark output screenshot |
| `sql/` | Athena queries for previewing Gold data and analyzing daily, city, and restaurant revenue |
| `docs/athena-results.md` | Query result values visible in the uploaded Athena screenshots |

**Note about the CSV uploads:** The two original CSV attachments contained only placeholder text. The small sample CSVs in `data/sample/` were reconstructed from the actual rows visible in your uploaded Spark terminal screenshot, and are identified as samples rather than represented as the original raw files.

## Technologies

- Amazon S3
- PySpark / Apache Spark
- Python
- Apache Parquet
- Amazon Athena
- Medallion Data Lake Architecture

## Run

Run the job from a Spark environment configured with the S3A connector and access to the three S3 layers:

```bash
spark-submit royal_orchid_etl.py
```

The runtime needs compatible Hadoop AWS / S3A dependencies and AWS credentials or an attached IAM role that can read the Bronze prefixes and write the Silver and Gold prefixes.

## Athena queries

The SQL files target the table shown in the uploaded Athena screenshots: `food_analytics.daily_restaurant_metrics`.

- `sql/01_preview_gold_metrics.sql`
- `sql/02_daily_revenue.sql`
- `sql/03_city_revenue.sql`
- `sql/04_restaurant_revenue.sql`

The screenshots show completed Athena queries. Sample results are documented in [docs/athena-results.md](docs/athena-results.md).

## Important execution notes

- The script uses `mode("overwrite")`; each run replaces output at the Silver and Gold paths.
- Orders are expected to include `order_date`, `sales_qty`, `sales_amount`, and `r_id`. Restaurant records are expected to include `r_id`, `name`, `cuisine`, and `city`.
- The Athena table definition and crawler/catalog setup were not included in the files I found, so no unverified DDL or deployment steps have been added.
- Never commit AWS access keys, secret keys, or other credentials.

## Author

**Athish**
