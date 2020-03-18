import os

SERVER = {
    "HOST": os.environ.get("AFPI_FTP_HOST") or "149.129.234.48",
    "USERNAME": os.environ.get("AFPI_FTP_USERNAME") or "FTP_USERNAME",
    "PASSWORD": os.environ.get("AFPI_FTP_PASSWORD") or "FTP_PASSWORD",
    "ZIP_PASSWORD": os.environ.get("AFPI_ZIP_PASSWORD") or "ZIP_PASSWORD",
    "ENVIRONMENT": os.environ.get("AFPI_ENVIRONMENT") or "TESTING"
}
