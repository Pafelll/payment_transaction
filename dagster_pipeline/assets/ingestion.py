from dagster import asset
from fetch_data import DataIngestion


@asset
def payment_transactions_gcs() -> None:
    ingestion = DataIngestion()
    df = ingestion.fetch_file()
    ingestion.upload_file(df)


@asset
def payment_description_gcs() -> None:
    ingestion = DataIngestion()
    ingestion.upload_description()