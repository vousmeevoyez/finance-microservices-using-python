"""
    Flask App
    ______________________
    Package Initialization
"""
from flask import Flask
from celery import Celery

from pymongo import MongoClient
from umongo import PyMongoInstance
from flask_marshmallow import Marshmallow

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
# import logging config immediately
from app.config import (
    logging,
    config
)

ma = Marshmallow()
sentry = sentry_sdk
celery = Celery(__name__, broker=config.Config.CELERY_BROKER_URL)
instance = PyMongoInstance()


def register_extension(app):
    """
        register flask extension via application factory
    """
    # marshmallow
    ma.init_app(app)
    # connect mongo
    connection = MongoClient(app.config["MONGO_URI"], connect=False)
    db = connection[app.config["MONGO_DBNAME"]]

    app.db = db
    app.connection = connection
    instance.init(db)

    celery.conf.update(app.config)  # update celery with flask application configuration

    # setup sentry only for production build
    if not app.testing and not app.debug:
        sentry_sdk.init(integrations=[FlaskIntegration(), CeleryIntegration()])


def create_app(config_name):
    """
        Create flask instance
        args :
            config_name -- Configuration key used (DEV/PROD/TESTING)
    """
    app = Flask(__name__)
    app.config.from_object(config.CONFIG_BY_NAME[config_name])

    register_extension(app)
    return app
