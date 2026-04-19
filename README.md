# ECB Payment Transaction Statistics Pipeline

An end-to-end batch data pipeline that ingests, transforms, and visualizes European payment transaction statistics published by the European Central Bank (ECB).

> **Quick start:** The project can be run using `make` commands (see [Makefile](#makefile)) or manually step by step (see [Setup](#setup)).

## Problem Description

The ECB publishes the **PST (Payment Statistics) dataset** — semi-annual data on payment transactions processed across European payment systems (T2 and retail/large-value systems) reported by National Central Banks of EU member states. The data covers volumes and values of transactions broken down by country, transaction type, payment channel, currency, and payment system — available from 2000 onwards.

This project answers two questions:
- **How has the volume of different transaction types evolved in the EU over time?**
- **Which countries dominate European payment systems?**

## Architecture

```
ECB API (CSV)
     │
     ▼
[ fetch_data.py ]
     │  pandas → Parquet
     ▼
Google Cloud Storage (raw)
     │
     ▼
[ transform_pyspark.py ]
     │  PySpark aggregations → pandas → BigQuery
     ▼
BigQuery (aggregated dashboard tables)
     │
     ▼
Metabase (dashboards)
```

**Orchestration:** Dagster manages the full pipeline as a graph of assets.

**Infrastructure as Code:** Terraform provisions GCS bucket and BigQuery dataset.

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | Google Cloud Platform |
| IaC | Terraform |
| Data Lake | Google Cloud Storage |
| Data Warehouse | BigQuery |
| Transformation | PySpark (local) |
| Orchestration | Dagster |
| Visualization | Metabase (Docker) |

## Dashboards

### 1. EU Transaction Volume by Type Over Time
Line chart showing how transaction volumes for each `TYP_TRNSCTN` (e.g. credit transfers, card payments, direct debits) evolved across semi-annual periods. Filter by `UNIT_MEASURE = PN` (pure number) to compare transaction counts.

### 2. Top Countries by Transaction Volume
Horizontal bar chart ranking countries (`REF_AREA`) by total transaction volume, sorted descending. Shows which EU member states dominate European payment systems.

## Makefile

After configuring `.env` (step 2 below), you can use `make` shortcuts:

```bash
make setup          # install uv, Python 3.13, venv and all dependencies
make install-java   # install OpenJDK 17 (optional, if Java is not present)
make infra-init     # terraform init
make infra-apply    # provision GCS + BigQuery
make metabase-up    # start Metabase
make pipeline       # start Dagster UI
make run            # infra-apply + metabase-up + pipeline
make infra-destroy  # tear down infrastructure
```

## Prerequisites

- Python 3.13+
- Java 21 (required by PySpark — tested with OpenJDK 21.0.10)
- Docker & Docker Compose
- Terraform
- GCP project with a service account that has roles: `Storage Admin`, `BigQuery Admin`

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd payment_transaction
make setup
```

This will install `uv` (if missing), Python 3.13, create a virtual environment and install all dependencies.

### 2. Configure environment

Copy `.env_example` to `.env` and fill in your values:

```bash
cp .env_example .env
```

```env
TF_VAR_project="your-gcp-project-id"
TF_VAR_gcs_bucket_name="your-unique-bucket-name"
TF_VAR_bq_dataset_name="payment_transaction_dataset"
GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

Load environment variables:

```bash
set -a && source .env && set +a
```

### 3. Provision infrastructure

```bash
cd terraform
terraform init
terraform apply
cd ..
```

This creates a GCS bucket and BigQuery dataset in `europe-central2`.

### 4. Start Metabase

```bash
docker compose up -d
```

Metabase will be available at `http://localhost:3000`.

### 5. Run the pipeline

Start Dagster:

```bash
dagster dev
```

Open `http://localhost:3000` (or the port shown in logs if 3000 is taken) and materialize all assets.

**Asset execution order:**
1. `payment_transactions_gcs` — fetches ECB data and uploads to GCS
2. `payment_description_gcs` — uploads column descriptions to GCS
3. `payment_transactions_local` — downloads parquet locally for PySpark
4. `dash_eu_trend_data`, `dash_country_map_data` — PySpark transformations
5. `dash_eu_trend`, `dash_country_map` — writes aggregated tables to BigQuery

### 6. Connect Metabase to BigQuery

In Metabase: **Settings → Databases → Add database → BigQuery**

- Project ID: value of `TF_VAR_project`
- Dataset ID: value of `TF_VAR_bq_dataset_name`
- Service account JSON: paste contents of your credentials file

## Project Structure

```
├── fetch_data.py            # DataIngestion: ECB API → GCS
├── transform_pyspark.py     # DataTransform: GCS → PySpark → BigQuery
├── constants.py             # Shared constants (URLs, table names, dtypes)
├── parse_description.py     # One-time script: payment_description.md → JSON
├── dagster_pipeline/
│   ├── assets/
│   │   ├── ingestion.py     # Dagster ingestion assets
│   │   └── transformation.py # Dagster transformation + BQ write assets
│   └── definitions.py       # Dagster Definitions entry point
├── terraform/               # GCS bucket + BigQuery dataset
├── docker-compose.yml       # Metabase
├── dagster.yaml             # Dagster logs configuration
└── .env_example             # Environment variables template
```