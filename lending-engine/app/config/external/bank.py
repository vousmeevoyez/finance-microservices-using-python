import os

BNI_ECOLLECTION = {
    "CREDIT_SECRET_KEY": os.getenv("BNI_VA_CREDIT_SECRET_KEY")
    or "0281c0c18992b97ae79efb2ac99ef529",
    "CREDIT_CLIENT_ID": os.getenv("BNI_VA_CREDIT_CLIENT_ID") or "99096",
    "VA_PREFIX": os.getenv("BNI_VA_PREFIX") or "988",
    "VA_LENGTH": 16,
    "INVESTMENT_PREFIX": os.getenv("INVESTMENT_PREFIX") or "12",
    "REPAYMENT_PREFIX": os.getenv("REPAYMENT_PREFIX") or "11",
}

# BNI RDL  CONFIG
BNI_RDL = {
    "COMPANY": os.getenv("BNI_RDL_COMPANY") or "b4c71336-f68d-49b5-969d-1533de629f61",
    "SECRET_API_KEY": os.getenv("BNI_RDL_SECRET_API_KEY")
    or "0ee540db-7cfb-48c7-9228-47068031d3f8"
}

MODANAKU = {
    "API_KEY": os.getenv("MODANAKU_API_KEY") or "modanaku-api-key"
}

# MASTER ACCOUNT
MASTER_ACCOUNT = {
    "ESCROW": {
        "account_name": os.environ.get("ESCROW_ACC_NAME") or "PT Amanah Escrow",
        "account_no": os.environ.get("ESCROW_ACC_NO") or "0115476117",
        "account_type": os.environ.get("ESCROW_ACC_TYPE") or "BANK_ACCOUNT",
        "bank_name": os.environ.get("ESCROW_BANK_NAME") or "BNI",
    },
    "ESCROW_VA": {
        "account_name": os.environ.get("ESCROW_VA_ACC_NAME") or "PT Amanah Escrow",
        "account_type": os.environ.get("ESCROW_VA_ACC_TYPE") or
        "VIRTUAL_ACCOUNT",
        "bank_name": os.environ.get("ESCROW_VA_BANK_NAME") or "BNI",
    },
    "PROFIT": {
        "account_name": os.environ.get("PROFIT_ACC_NAME") or "PT Amanah Profit",
        "account_no": os.environ.get("PROFIT_ACC_NO") or "0115471119",
        "account_type": os.environ.get("PROFIT_ACC_TYPE") or "BANK_ACCOUNT",
        "bank_name": os.environ.get("PROFIT_BANK_NAME") or "BNI",
    }
}
