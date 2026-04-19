from dagster_pipeline.assets.ingestion import payment_transactions_gcs, payment_description_gcs
from dagster_pipeline.assets.transformation import (
    payment_transactions_local,
    dash_eu_trend_data,
    dash_country_map_data,
    dash_online_shift_data,
    dash_system_dominance_data,
    dash_eu_trend,
    dash_country_map,
    dash_online_shift,
    dash_system_dominance,
)