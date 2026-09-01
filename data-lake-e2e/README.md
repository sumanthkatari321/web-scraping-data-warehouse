# LakeFlow — End-to-End Data Lake

LakeFlow is a locally runnable, medallion-style data lake project for retail order analytics. It generates transactional events, lands immutable raw JSON in S3-compatible object storage, transforms data with Python into partitioned Parquet, validates quality rules, and makes curated data queryable through Trino.

## Architecture

```text
Retail events -> Python producer -> MinIO /bronze (JSON)
                                    |
                              transform + quality checks
                                    v
                           MinIO /silver (Parquet)
                                    |
                              aggregate
                                    v
                            MinIO /gold (Parquet) -> Trino
```

| Layer | Format | Contents |
| --- | --- | --- |
| Bronze | JSON | Immutable generated order events, partitioned by ingestion date |
| Silver | Parquet | Validated, typed, de-duplicated order lines |
| Gold | Parquet | Daily product sales metrics |

## Run it

```bash
cd data-lake-e2e
docker compose up -d minio create-buckets trino
docker compose run --rm lake-jobs --records 1000
```

The job prints bronze, silver, and gold object locations. Open the MinIO console at `http://localhost:9001` (credentials: `minioadmin` / `minioadmin`). Trino is available on port `8081`.

## Operational design

- Run identifiers make each bronze landing immutable and traceable.
- A manifest records record count, schema version, checksum, and timestamp for every landing.
- Invalid monetary values, missing IDs, malformed timestamps, and duplicate order lines are rejected before silver publication.
- Parquet partitions (`event_date`) limit scan cost and make retention policies straightforward.

## Production path

Replace MinIO with S3/ADLS/GCS, schedule `src.pipeline` using Airflow or a managed orchestrator, use Spark/Glue for large volumes, and register Iceberg/Delta tables in a catalog. Keep the bronze/silver/gold contracts unchanged.
