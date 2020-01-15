""" 
    Package Initialization
"""
from app.api.namespace import HealthNamespace
api = HealthNamespace.api
from app.api.health import routes
