BUCKET_NAME = "transaction-payments-485019"
BASE_URL = "https://data-api.ecb.europa.eu/service/data/PST?format=csvdata"

CREDENTIALS_FILE = "gcp-finance-secret-key.json"
TRANSACTION_FILE_NAME = "payment_transactions.parquet"
CHUNK_SIZE = 8 * 1024 * 1024

DTYPES = {
    'KEY': 'string',
    'FREQ': 'string',
    'REF_AREA': 'string',
    'COUNT_AREA': 'string',
    'TYP_INFO': 'string',
    'TYP_TRNSCTN': 'string',
    'INTTN_CHNNL': 'string',
    'PYMNT_SYSTM': 'string',
    'TRANSFORMATION': 'string',
    'UNIT_MEASURE': 'string',
    'CURRENCY_TRANS': 'string',
    'TIME_PERIOD': 'string',
    'OBS_VALUE': 'float64',
    'OBS_STATUS': 'string',
    'CONF_STATUS': 'string',
    'PRE_BREAK_VALUE': 'float64',
    'COMMENT_OBS': 'string',
    'TIME_FORMAT': 'string',
    'BREAKS': 'string',
    'COMMENT_TS': 'string',
    'COMPILING_ORG': 'string',
    'DISS_ORG': 'string',
    'TIME_PER_COLLECT': 'string',
    'COVERAGE': 'string',
    'DATA_COMP': 'string',
    'DECIMALS': 'int32',
    'METHOD_REF': 'string',
    'TITLE': 'string',
    'TITLE_COMPL': 'string',
    'UNIT': 'string',
    'UNIT_MULT': 'int32'
}