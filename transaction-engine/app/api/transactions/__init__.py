"""
    Package Initialization
"""
from app.api.namespace import TransactionNamespace

api = TransactionNamespace.api
from app.api.transactions import routes
