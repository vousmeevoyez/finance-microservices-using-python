"""
    Configuration
    ______________
    define all configuration used on provider
"""
import os

LOGGING = {"TIMEOUT": 15}

BNI_ECOLLECTION = {
    "BASE_URL": os.getenv("BNI_VA_URL") or "https://apibeta.bni-ecollection.com/",
    "DEBIT_SECRET_KEY": os.getenv("BNI_VA_DEBIT_SECRET_KEY")
    or "920b0241ba29bdc1e09246847af7f876",
    "DEBIT_CLIENT_ID": os.getenv("BNI_VA_DEBIT_CLIENT_ID") or "99097",
    "CREDIT_SECRET_KEY": os.getenv("BNI_VA_CREDIT_SECRET_KEY")
    or "0281c0c18992b97ae79efb2ac99ef529",
    "CREDIT_CLIENT_ID": os.getenv("BNI_VA_CREDIT_CLIENT_ID") or "99096",
    "CREDIT_VA_EXPIRE": os.getenv("BNI_VA_CREDIT_EXPIRE") or "435000", # hours
    "VA_PREFIX": os.getenv("BNI_VA_PREFIX") or "988",
    "VA_LENGTH": 16,
    "UPDATE": "updatebilling",
    "INQUIRY": "inquirybilling",
}

CUSTOM_PREFIX = {
    "REPAYMENT": os.getenv("REPAYMENT_PREFIX") or "11",
    "INVESTMENT": os.getenv("INVESTMENT_PREFIX") or "12",
}
