""" Configuration for FILE URL """
import os

FILE_URL = (
    os.environ.get("FILE_URL")
    or "http://147.139.134.250:11000/api/v1/report/afpi/download/{}"
)
