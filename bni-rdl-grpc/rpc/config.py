"""
    Configuration
    ______________
    define all configuration used on provider
"""
import os

LOGGING = {"TIMEOUT": 15}

# BNI RDL  CONFIG
BNI_RDL = {
    "MASTER_ACCOUNT": os.getenv("BNI_RDL_MASTER_ACCOUNT") or "114487109",
    "BASE_URL": os.getenv("BNI_RDL_URL") or "https://apidev.bni.co.id",
    "PORT": os.getenv("BNI_RDL_PORT") or "8066",
    "CLIENT_NAME": os.getenv("BNI_RDL_CLIENT_NAME") or "MODANA",
    "USERNAME": os.getenv("BNI_RDL_USERNAME") or "b4c71336-f68d-49b5-969d-1533de629f61",
    "PASSWORD": os.getenv("BNI_RDL_PASSWORD") or "a98de724-5dfc-4f1c-a4c1-08b098a08320",
    "API_KEY": os.getenv("BNI_RDL_API_KEY") or "f1bd00a9-5512-43c2-83f7-1e2b407eb74c",
    "SECRET_API_KEY": os.getenv("BNI_RDL_SECRET_API_KEY")
    or "0ee540db-7cfb-48c7-9228-47068031d3f8",
    "COMPANY": os.getenv("BNI_RDL_COMPANY") or "MODANA",
    "PARENT_COMPANY": os.getenv("BNI_RDL_PARENT_COMPANY") or "INDONUSA",
    "ROUTES": {
        "GET_TOKEN": "/api/oauth/token",
        "REGIST_INVESTOR": "/p2pl/register/investor",
        "REGIST_INVESTOR_ACC": "/p2pl/register/investor/account",
        "INQUIRY_ACC": "/p2pl/inquiry/account/info",
        "INQUIRY_BALANCE": "/p2pl/inquiry/account/balance",
        "INQUIRY_HISTORY": "/p2pl/inquiry/account/history",
        "PAYMENT_TRANSFER": "/p2pl/payment/transfer",
        "PAYMENT_STATUS": "/p2pl/inquiry/payment/status",
        "CLEARING_TRANSFER": "/p2pl/payment/clearing",
        "RTGS_TRANSFER": "/p2pl/payment/rtgs",
        "INTERBANK_INQUIRY": "/p2pl/inquiry/interbank/account",
        "INTERBANK_TRANSFER": "/p2pl/payment/interbank",
    },
}
