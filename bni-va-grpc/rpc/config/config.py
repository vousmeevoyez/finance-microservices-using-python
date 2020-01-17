"""
    Configuration
    _______________
    This is module for storing all configuration for various environments
"""
import os


class Config:
    """ This is base class for configuration """

    DEBUG = False

    # mongodb://[username:password@]host1[:port1][,...hostN[:portN]]][/[database][?options]]
    MONGO_DBNAME = os.getenv("MONGO_DBNAME") or "db_virtual_account"
    MONGO_URI = os.getenv("MONGO_URI") or "mongodb://modana:password@localhost:27017/"

    SENTRY_CONFIG = {}


class DevelopmentConfig(Config):
    """ This is class for development configuration """

    DEBUG = True

    MONGO_DBNAME = Config.MONGO_DBNAME
    MONGO_URI = Config.MONGO_URI + MONGO_DBNAME


class TestingConfig(Config):
    """ This is class for testing configuration """

    DEBUG = True
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SENTRY_CONFIG = {}

    MONGO_DBNAME = Config.MONGO_DBNAME + "_test"
    MONGO_URI = Config.MONGO_URI + MONGO_DBNAME


class ProductionConfig(Config):
    """ This is class for production configuration """

    DEBUG = False

    MONGO_DBNAME = Config.MONGO_URI
    MONGO_URI = Config.MONGO_URI + MONGO_DBNAME

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SENTRY_CONFIG = Config.SENTRY_CONFIG
    SENTRY_CONFIG["dsn"] = os.environ.get("SENTRY_DSN")


CONFIG_BY_NAME = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
