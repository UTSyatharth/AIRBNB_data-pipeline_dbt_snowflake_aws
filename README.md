# Airbnb Data Pipeline — dbt + Snowflake + AWS

An end-to-end data engineering project that builds a production-style ELT pipeline for Airbnb listings, host, and booking data, using the Medallion Architecture (Bronze → Silver → Gold) on top of Snowflake, orchestrated with dbt, with raw data staged from AWS S3.

## Overview

This project simulates a real-world analytics engineering workflow: raw data lands in cloud storage, gets staged into a warehouse, and is progressively cleaned, modeled, and transformed into analysis-ready tables — with testing, documentation, and slowly changing dimensions built in along the way.

## Architecture

```
AWS S3 (raw CSVs)
      │
      ▼
Snowflake External Stage (AWS IAM integration)
      │
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BRONZE    │ ──▶ │   SILVER    │ ──▶ │    GOLD     │
│ Raw ingest  │     │ Cleaned &   │     │ Star schema │
│ (as-is)     │     │ upserted    │     │ fact + dims │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                   dbt Snapshots (SCD Type-2)
                   tracking historical changes
                   to hosts, listings, bookings
```

**Bronze layer** — raw data loaded as-is from S3 via Snowflake external stages, no transformation.

**Silver layer** — cleaned, deduplicated, and upserted using incremental dbt models with metadata-driven logic, so only new or changed records are processed on each run.

**Gold layer** — a star schema with a central fact table and supporting dimensions, built for direct use in BI tools. Includes an ephemeral layer for intermediate logic that doesn't need to persist as physical tables.

**Snapshots** — dbt snapshots implement Slowly Changing Dimension Type 2 on hosts, listings, and bookings, preserving a full history of changes over time rather than overwriting records.

## Tech stack

| Layer | Tool |
|---|---|
| Raw storage | AWS S3 |
| Cloud connectivity | AWS IAM + Snowflake Storage Integration |
| Data warehouse | Snowflake |
| Transformation | dbt (Data Build Tool) |
| Version control | Git / GitHub |
| Modeling pattern | Medallion Architecture, Kimball Star Schema, SCD Type-2 |

## Key features

- **Incremental models** — silver layer uses dbt's incremental materialization with upsert logic, avoiding full table rebuilds on every run.
- **Metadata-driven pipelines** — model behavior is parameterized through configuration rather than hardcoded, making the pipeline easier to extend to new sources.
- **Custom macros** — reusable Jinja macros (`generate_schema_name`, `multiply`, `tag`, `trimmer`) handle schema naming conventions and repeated transformation logic.
- **Data quality testing** — source and model-level tests (uniqueness, not-null, referential integrity) catch data issues before they propagate downstream.
- **SCD Type-2 snapshots** — full historical tracking of dimension changes for hosts, listings, and bookings.

## Project structure

```
aws_dbt_snowflake_project/
├── models/
│   ├── bronze/          # Raw ingestion models
│   ├── silver/          # Cleaned, incremental, upserted models
│   ├── gold/             # Star schema: fact table, ephemeral models, one-big-table
│   └── sources/         # Source table definitions
├── snapshots/            # SCD Type-2 snapshots for dimensions
├── macros/               # Custom Jinja macros
├── tests/                # Custom data quality tests
├── analyses/             # Ad-hoc exploration queries
└── dbt_project.yml       # Project configuration
```

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/UTSyatharth/AIRBNB_data-pipeline_dbt_snowflake_aws.git
   cd AIRBNB_data-pipeline_dbt_snowflake_aws/aws_dbt_snowflake_project
   ```

2. Create a Python virtual environment and install dbt
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install dbt-snowflake
   ```

3. Configure your Snowflake connection in `~/.dbt/profiles.yml` (not included in this repo — see `.gitignore`)

4. Run the pipeline
   ```bash
   dbt run
   dbt test
   dbt snapshot
   dbt docs generate
   dbt docs serve
   ```

## What this project demonstrates

This project was built to practice the core skills expected of an analytics engineer / data engineer working with modern cloud data stacks: cloud storage integration, warehouse modeling, incremental processing, dimensional modeling, historical change tracking, and automated testing — the same patterns used in production data platforms at most mid-to-large Australian enterprises currently migrating to cloud-native data stacks.

## Acknowledgements

<<<<<<< HEAD
Built while following an end-to-end data engineering tutorial covering Snowflake, dbt, and AWS, then extended with personal modifications and additional documentation.
=======
Built while following an end-to-end data engineering tutorial covering Snowflake, dbt, and AWS, then extended with personal modifications and additional documentation.
>>>>>>> 4d5e139f14180a5d1f454ae6a54a5c5f6d2f1cbf
