""" 
    Package Initialization
"""
from app.api.namespace import InvestorNamespace

api = InvestorNamespace.api
from app.api.investor import routes
