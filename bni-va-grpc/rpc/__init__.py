"""
    Flask App
    ______________________
    Package Initialization
"""
from flask import Flask

from mongoengine import connect

from rpc.config import (
    config
)


def db_connection(app):
    """ initialize connection to mongo db"""
    connect(
        host=app.config['MONGO_URI']
    )


def register_extension(app):
    """
        register flask extension via application factory
    """
    pass


def create_app(config_name):
    """
        Create flask instance
        args :
            config_name -- Configuration key used (DEV/PROD/TESTING)
    """
    app = Flask(__name__)
    app.config.from_object(config.CONFIG_BY_NAME[config_name])

    db_connection(app)
    register_extension(app)
    return app
