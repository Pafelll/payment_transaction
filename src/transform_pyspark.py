import logging
import os
from pathlib import Path

import pandas as pd
from google.cloud import bigquery, storage
from pyspark.conf import SparkConf
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

import constants as const

logger = logging.getLogger()


class DataTransform:
    def __init__(self):
        self.credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.bucket_name = os.getenv("TF_VAR_gcs_bucket_name")
        self.bq_dataset = os.getenv("TF_VAR_bq_dataset_name")
        self.project_id = os.getenv("TF_VAR_project")

        conf = SparkConf().setMaster("local[*]").setAppName("pst_transform")

        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()
        self.spark.sparkContext.setLogLevel("WARN")

    def download_from_gcs(self, local_dir: str = "data/local") -> Path:
        client = storage.Client.from_service_account_json(self.credentials)
        bucket = client.bucket(self.bucket_name)
        blob = bucket.blob(const.TRANSACTION_FILE_NAME)

        local_path = Path(local_dir) / const.TRANSACTION_FILE_NAME
        local_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(local_path)
        logger.info(f"Downloaded to {local_path}")
        return local_path

    def read(self, local_path: Path) -> DataFrame:
        return self.spark.read.parquet(str(local_path))

    def write_to_bq(self, pdf: pd.DataFrame, table_name: str) -> None:
        destination = f"{self.project_id}.{self.bq_dataset}.{table_name}"
        logger.info(f"Writing to BigQuery: {destination}")
        client = bigquery.Client.from_service_account_json(self.credentials)
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = client.load_table_from_dataframe(pdf, destination, job_config=job_config)
        job.result()
        logger.info(f"Written {job.output_rows} rows to {destination}")

    def transform_eu_trend(self, df: DataFrame) -> pd.DataFrame:
        return (
            df.filter(F.col("OBS_VALUE").isNotNull())
            .groupBy("TIME_PERIOD", "TYP_TRNSCTN", "UNIT_MEASURE")
            .agg(F.sum("OBS_VALUE").alias("total_value"))
            .orderBy("TIME_PERIOD", "TYP_TRNSCTN")
            .toPandas()
        )

    def transform_country_map(self, df: DataFrame) -> pd.DataFrame:
        return (
            df.filter(F.col("OBS_VALUE").isNotNull())
            .groupBy("REF_AREA", "TIME_PERIOD", "UNIT_MEASURE")
            .agg(F.sum("OBS_VALUE").alias("total_value"))
            .orderBy("TIME_PERIOD", "REF_AREA")
            .toPandas()
        )

    def transform_online_shift(self, df: DataFrame) -> pd.DataFrame:
        base = (
            df.filter(F.col("OBS_VALUE").isNotNull())
            .groupBy("TIME_PERIOD", "INTTN_CHNNL", "UNIT_MEASURE")
            .agg(F.sum("OBS_VALUE").alias("channel_value"))
        )

        total = base.groupBy("TIME_PERIOD", "UNIT_MEASURE").agg(F.sum("channel_value").alias("total_value"))

        return (
            base.join(total, on=["TIME_PERIOD", "UNIT_MEASURE"])
            .withColumn("share_pct", F.round(F.col("channel_value") / F.col("total_value") * 100, 2))
            .orderBy("TIME_PERIOD", "INTTN_CHNNL")
            .toPandas()
        )

    def transform_system_dominance(self, df: DataFrame) -> pd.DataFrame:
        base = (
            df.filter(F.col("OBS_VALUE").isNotNull())
            .groupBy("TIME_PERIOD", "PYMNT_SYSTM", "UNIT_MEASURE")
            .agg(F.sum("OBS_VALUE").alias("system_value"))
        )

        total = base.groupBy("TIME_PERIOD", "UNIT_MEASURE").agg(F.sum("system_value").alias("total_value"))

        return (
            base.join(total, on=["TIME_PERIOD", "UNIT_MEASURE"])
            .withColumn("share_pct", F.round(F.col("system_value") / F.col("total_value") * 100, 2))
            .orderBy("TIME_PERIOD", "PYMNT_SYSTM")
            .toPandas()
        )
