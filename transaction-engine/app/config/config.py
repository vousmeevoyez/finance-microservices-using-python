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
    MONGO_DBNAME = os.getenv("MONGO_DBNAME") or "transaction_engine"
    MONGO_PATH = os.getenv("MONGO_PATH") or "mongodb://modana:password@localhost:27017"
    MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET") or "mongo-rs"

    SENTRY_CONFIG = {}

    # FLASK RESTPLUS
    ERROR_INCLUDE_MESSAGE = False

    CELERY_BROKER_URL = os.getenv("BROKER_URL") or "amqp://guest:guest@localhost:5672"
    # REGISTER ALL KNOWN CELERY TASK HERE
    CELERY_IMPORTS = ("task.transaction.tasks", "task.external.tasks")
    CELERY_TASK_DEFAULT_QUEUE = "default"
    # REGISTER ALL KNOWN QUEUES HERE
    CELERY_QUEUES = {
        "default": {"exchange": "default", "binding_key": "default"},
        "transaction": {"exchange": "transaction", "binding_key": "transaction"},
        "externnal": {"exchange": "external", "binding_key": "external"},
    }
    CELERY_TRACK_STARTED = True


class DevelopmentConfig(Config):
    """ This is class for development configuration """

    DEBUG = True

    MONGO_URI = (
        Config.MONGO_PATH
        + "/"
        + Config.MONGO_DBNAME
        + "?replicaSet="
        + Config.MONGO_REPLICA_SET
        + "&retryWrites=true"
    )

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": MONGO_URI,
        "database": Config.MONGO_DBNAME,
    }


class TestingConfig(Config):
    """ This is class for testing configuration """

    DEBUG = True
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENTRY_CONFIG = {}

    MONGO_DBNAME = Config.MONGO_DBNAME + "_test"
    MONGO_URI = (
        Config.MONGO_PATH
        + "/"
        + Config.MONGO_DBNAME
        + "?replicaSet="
        + Config.MONGO_REPLICA_SET
        + "&retryWrites=true"
    )

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": Config.MONGO_PATH + "/",
        "replicaSet": Config.MONGO_REPLICA_SET,
        "database": Config.MONGO_DBNAME,
    }


class ProductionConfig(Config):
    """ This is class for production configuration """

    DEBUG = False

    MONGO_URI = (
        Config.MONGO_PATH
        + "/"
        + Config.MONGO_DBNAME
        + "?replicaSet="
        + Config.MONGO_REPLICA_SET
        + "&retryWrites=true"
    )

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": MONGO_URI,
        "database": Config.MONGO_DBNAME,
    }

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SENTRY_CONFIG = Config.SENTRY_CONFIG
    SENTRY_CONFIG["dsn"] = os.environ.get("SENTRY_DSN")


CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
