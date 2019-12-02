"""
    Package Initialization
"""

from flask_restplus import Api

from flask import Blueprint

from app.api.transactions import api as trx_ns


blueprint = Blueprint("api", __name__)
# intialize API
api = Api(blueprint, contact="kelvindsmn@gmail.com")  # register blueprint
api.add_namespace(trx_ns, path="/transaction")
