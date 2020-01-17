import os

WORKER = {
    "MAX_RETRIES": os.getenv("WORKER_MAX_RETRY") or 5,
    "HARD_LIMIT": 15,
    "SOFT_LIMIT": 10,
    "ACKS_LATE": True,  # prevent executing task twice
}

RPC = {
    "NOTIFICATION": os.getenv("NOTIFICATION_RPC_URL") or "127.0.0.1:5001",
    "BNI_RDL": os.getenv("BNI_RDL_RPC_URL") or "127.0.0.1:5001",
    "BNI_OPG": os.getenv("BNI_OPG_RPC_URL") or "127.0.0.1:5001",
    "BNI_VA": os.getenv("BNI_VA_RPC_URL") or "127.0.0.1:5001",
}

HTTP = {
    "LENDING_ENGINE": {
        "BASE_URL": os.getenv("LENDING_ENGINE_URL") or "http://127.0.0.1:5001",
        "API": {"CALLBACK": "/api/v1/callback/transaction"},
    }
}
