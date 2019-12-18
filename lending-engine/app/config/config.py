"""
    Configuration
    _______________
    This is module for storing all configuration for various environments
"""
import os
from celery.schedules import crontab
from celery import signature


class Config:
    """ This is base class for configuration """
    DEBUG = False

    #mongodb://[username:password@]host1[:port1][,...hostN[:portN]]][/[database][?options]]
    MONGO_DBNAME = os.getenv("MONGO_DBNAME") or "lending_engine"
    MONGO_PATH = os.getenv("MONGO_PATH") or "mongodb://modana:password@localhost:27017"
    MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET") or "mongo-rs"

    SENTRY_CONFIG = {}

    # FLASK RESTPLUS
    ERROR_INCLUDE_MESSAGE = False

    CELERY_BROKER_URL = os.getenv("BROKER_URL") or "amqp://guest:guest@localhost:5672"
    # REGISTER ALL KNOWN CELERY TASK HERE
    CELERY_IMPORTS = (
        "task.investor.tasks",
        "task.investment.tasks",
        "task.transaction.tasks",
        "task.utility.tasks",
        "task.virtual_account.tasks",
        "task.scheduler.tasks",
    )
    CELERY_TASK_DEFAULT_QUEUE = "default"
    # REGISTER ALL KNOWN QUEUES HERE
    CELERY_QUEUES = {
        "default": {"exchange": "default", "binding_key": "default"},
        "utility": {"exchange": "utility", "binding_key": "utility"},
        "periodic": {"exchange": "periodic", "binding_key": "periodic"},
        "investor": {"exchange": "investor", "binding_key": "investor"},
        "virtual_account": {"exchange": "virtual_account", "binding_key":
                            "virtual_account"},
        "investment": {"exchange": "investment", "binding_key": "investment"},
        "transaction": {"exchange": "transaction", "binding_key":
                        "transaction"},
    }
    CELERY_TRACK_STARTED = True
    CELERY_TIMEZONE = "Asia/Jakarta"


class DevelopmentConfig(Config):
    """ This is class for development configuration """
    DEBUG = True

    MONGO_URI = Config.MONGO_PATH + "/" + Config.MONGO_DBNAME + "?replicaSet=" + Config.MONGO_REPLICA_SET

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": MONGO_URI,
        "database": Config.MONGO_DBNAME
    }

    CELERYBEAT_SCHEDULE = {
        # for dev purpose we mark loan as over due every 5 miinutes after grace
        # period
        "check-overdues": {
            "task": "task.scheduler.tasks.calculate_overdues",
            "schedule": crontab(minute="*/5"),
            "options": {
                "queue": "periodic",
                "link": signature(
                    "task.scheduler.tasks.calculate_late_fees",
                    args=(),
                    kwargs={},
                    queue="periodic"
                )
            }
        },
        # we set sending notiifcation every 8 morning
        "remind-loan-before-due-dates": {
            "task": "task.scheduler.tasks.remind_before_due_dates",
            "schedule": crontab(hour=8, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set sending notiifcation every 15 evening
        "remind-loan-after-due-dates": {
            "task": "task.scheduler.tasks.remind_after_due_dates",
            "schedule": crontab(hour=15, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set auto cancel every midnight
        "auto-cancel-verifying-loan": {
            "task": "task.scheduler.tasks.auto_cancel_verifying_loan",
            "schedule": crontab(hour=0, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set auto cancel every midnight
        "auto-cancel-approved-loan": {
            "task": "task.scheduler.tasks.auto_cancel_approved_loan",
            "schedule": crontab(hour=0, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # execute batch every hour
        "execute-batch": {
            "task": "task.scheduler.tasks.execute_transaction_batch",
            "schedule": crontab(),
            "options": {
                "queue": "periodic",
            }
        },
    }


class TestingConfig(Config):
    """ This is class for testing configuration """
    DEBUG = True
    TESTING = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENTRY_CONFIG = {}

    MONGO_DBNAME = Config.MONGO_DBNAME + "_test"
    MONGO_URI = Config.MONGO_PATH + "/" + MONGO_DBNAME

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": Config.MONGO_PATH,
        "database": MONGO_DBNAME
    }


class ProductionConfig(Config):
    """ This is class for production configuration """
    DEBUG = False

    MONGO_URI = Config.MONGO_PATH + "/" + Config.MONGO_DBNAME + "?replicaSet="\
        + Config.MONGO_REPLICA_SET

    CELERY_RESULT_BACKEND = "mongodb"
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": MONGO_URI,
        "database": Config.MONGO_DBNAME
    }

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SENTRY_CONFIG = Config.SENTRY_CONFIG
    SENTRY_CONFIG["dsn"] = os.environ.get("SENTRY_DSN")

    CELERYBEAT_SCHEDULE = {
        "check-overdues": {
            "task": "task.scheduler.tasks.calculate_overdues",
            "schedule": crontab(minute=0, hour=0),  # daily at midnight
            "options": {
                "queue": "periodic",
                "link": signature(
                    "task.scheduler.tasks.calculate_late_fees",
                    args=(),
                    kwargs={},
                    queue="periodic"
                )
            }
        },
        # we set sending notiifcation every 8 morning
        "remind-loan-before-due-dates": {
            "task": "task.scheduler.tasks.remind_before_due_dates",
            "schedule": crontab(hour=8, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set sending notiifcation every 15 evening
        "remind-loan-after-due-dates": {
            "task": "task.scheduler.tasks.remind_after_due_dates",
            "schedule": crontab(hour=15, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set auto cancel every midnight
        "auto-cancel-verifying-loan": {
            "task": "task.scheduler.tasks.auto_cancel_verifying_loan",
            "schedule": crontab(hour=0, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # we set auto cancel every midnight
        "auto-cancel-approved-loan": {
            "task": "task.scheduler.tasks.auto_cancel_approved_loan",
            "schedule": crontab(hour=0, minute=0),
            "options": {
                "queue": "periodic",
            }
        },
        # execute batch every hour
        "execute-batch": {
            "task": "task.scheduler.tasks.execute_transaction_batch",
            "schedule": crontab(minute="*/60"),
            "options": {
                "queue": "periodic",
            }
        },
    }


CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
