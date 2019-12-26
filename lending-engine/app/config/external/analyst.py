import os

ANALYST_BE = {
    "BASE_URL": os.environ.get("ANALYST_BASE_URL") or "http://localhost:8000/",
    "ENDPOINTS": {
        "LOGIN": "/v1/login",
        "CREATE_REPORT": "/v1/reports/ojk/{}/csv?file={}"
    },
    "USERNAME": os.environ.get("ANALYST_USERNAME") or "ANALYST_USERNAME",
    "PASSWORD": os.environ.get("ANALYST_PASSWORD") or "ANALYST_PASSWORD",
}
