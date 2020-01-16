"""
    Routes
    ___________
    this is where our flask app define all url
"""
from flask_restplus import Resource
from celery import chain
from flask import request

from app.api.health import api
from app.api.health.modules.services import HealthServices


@api.route("/check")
class HealthCheckRoutes(Resource):
    """
        /health/check
    """

    def get(self):
        response = HealthServices().check()
        return response
