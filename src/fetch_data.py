import json
import logging
import os
from io import BytesIO

import pandas as pd
from google.cloud import storage

import constants as const

logger = logging.getLogger()


class DataIngestion:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        self.bucket_name = os.getenv("TF_VAR_gcs_bucket_name")
        self.bucket = self.client.bucket(self.bucket_name)
        self.filename = const.TRANSACTION_FILE_NAME
        self.url = const.BASE_URL
        self.dtypes = const.DTYPES

    def fetch_file(self) -> pd.DataFrame:
        return pd.read_csv(
            self.url, dtype=self.dtypes, na_values=["", "NULL", "null", "NA", "N/A"], keep_default_na=True
        )

    def upload_to_gcs(self, file_path, blob_name, max_retries=3) -> None:
        blob = self.bucket.blob(blob_name)

        for attempt in range(max_retries):
            try:
                logger.info(f"Uploading {file_path} to {self.bucket_name} (Attempt {attempt + 1})...")
                blob.upload_from_file(file_path)
                logger.info(f"Uploaded: gs://{self.bucket_name}/{blob_name}")

                if self.verify_gcs_upload(blob_name):
                    logger.info(f"Verification successful for {blob_name}")
                    return
                else:
                    logger.info(f"Verification failed for {blob_name}, retrying...")
            except Exception as e:
                logger.error(f"Failed to upload {file_path} to GCS: {e}")
        logger.info(f"Giving up on {file_path} after {max_retries} attempts.")

    def verify_gcs_upload(self, blob_name) -> bool:
        return storage.Blob(bucket=self.bucket, name=blob_name).exists(self.client)

    def upload_file(self, data) -> None:
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        buffer.seek(0)
        self.upload_to_gcs(buffer, self.filename)

    def upload_description(self, description_path: str = "payment_description.json") -> None:
        with open(description_path, encoding="utf-8") as f:
            data = json.load(f)

        rows = [
            {"column_name": col, "code": entry["code"], "description": entry["description"]}
            for col, entries in data.items()
            for entry in entries
        ]
        df = pd.DataFrame(rows, columns=["column_name", "code", "description"])
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        self.upload_to_gcs(buffer, "payment_description.parquet")
