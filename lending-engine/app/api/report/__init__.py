""" 
    Package Initialization
"""
from app.api.namespace import ReportNamespace
api = ReportNamespace.api 
from app.api.report import routes
