from dagster import Definitions, load_assets_from_package_module

from dagster_pipeline import assets

defs = Definitions(
    assets=load_assets_from_package_module(assets),
)
