from pathlib import Path
import pandas as pd
from dagster import asset
from transform_pyspark import DataTransform
import constants as const


@asset(deps=["payment_transactions_gcs"])
def payment_transactions_local() -> Path:
    transform = DataTransform()
    return transform.download_from_gcs()


@asset
def dash_eu_trend_data(payment_transactions_local: Path) -> pd.DataFrame:
    transform = DataTransform()
    df = transform.read(payment_transactions_local)
    return transform.transform_eu_trend(df)


@asset
def dash_country_map_data(payment_transactions_local: Path) -> pd.DataFrame:
    transform = DataTransform()
    df = transform.read(payment_transactions_local)
    return transform.transform_country_map(df)


@asset
def dash_online_shift_data(payment_transactions_local: Path) -> pd.DataFrame:
    transform = DataTransform()
    df = transform.read(payment_transactions_local)
    return transform.transform_online_shift(df)


@asset
def dash_system_dominance_data(payment_transactions_local: Path) -> pd.DataFrame:
    transform = DataTransform()
    df = transform.read(payment_transactions_local)
    return transform.transform_system_dominance(df)


@asset
def dash_eu_trend(dash_eu_trend_data: pd.DataFrame) -> None:
    DataTransform().write_to_bq(dash_eu_trend_data, const.BQ_TABLE_EU_TREND)


@asset
def dash_country_map(dash_country_map_data: pd.DataFrame) -> None:
    DataTransform().write_to_bq(dash_country_map_data, const.BQ_TABLE_COUNTRY_MAP)


@asset
def dash_online_shift(dash_online_shift_data: pd.DataFrame) -> None:
    DataTransform().write_to_bq(dash_online_shift_data, const.BQ_TABLE_ONLINE_SHIFT)


@asset
def dash_system_dominance(dash_system_dominance_data: pd.DataFrame) -> None:
    DataTransform().write_to_bq(dash_system_dominance_data, const.BQ_TABLE_SYSTEM_DOMINANCE)