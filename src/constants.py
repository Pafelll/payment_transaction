BASE_URL = "https://data-api.ecb.europa.eu/service/data/PST?format=csvdata"

TRANSACTION_FILE_NAME = "payment_transactions.parquet"
CHUNK_SIZE = 8 * 1024 * 1024

BQ_TABLE_EU_TREND = "dash_eu_trend"
BQ_TABLE_COUNTRY_MAP = "dash_country_map"
BQ_TABLE_ONLINE_SHIFT = "dash_online_shift"
BQ_TABLE_SYSTEM_DOMINANCE = "dash_system_dominance"

DTYPES = {
    "KEY": "string",
    "FREQ": "string",
    "REF_AREA": "string",
    "COUNT_AREA": "string",
    "TYP_INFO": "int64",
    "TYP_TRNSCTN": "string",
    "INTTN_CHNNL": "string",
    "PYMNT_SYSTM": "string",
    "TRANSFORMATION": "string",
    "UNIT_MEASURE": "string",
    "CURRENCY_TRANS": "string",
    "TIME_PERIOD": "string",
    "OBS_VALUE": "float64",
    "OBS_STATUS": "string",
    "CONF_STATUS": "string",
    "PRE_BREAK_VALUE": "float64",
    "COMMENT_OBS": "string",
    "TIME_FORMAT": "string",
    "BREAKS": "float64",
    "COMMENT_TS": "float64",
    "COMPILING_ORG": "float64",
    "DISS_ORG": "float64",
    "TIME_PER_COLLECT": "string",
    "COVERAGE": "float64",
    "DATA_COMP": "float64",
    "DECIMALS": "int64",
    "METHOD_REF": "string",
    "TITLE": "string",
    "TITLE_COMPL": "string",
    "UNIT": "string",
    "UNIT_MULT": "int64",
}
