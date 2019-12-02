""" 
    Package Initialization
"""
from app.api.namespace import InvestmentNamespace
api = InvestmentNamespace.api 
from app.api.investment import routes
