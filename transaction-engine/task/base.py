"""
    Base Task Modules
"""
import random

from app.api import celery, sentry


def backoff(attempts):
    """ prevent hammering service with thousand retry"""
    return random.uniform(2, 4) ** attempts


def fast_backoff():
    """ retry backoff fast """
    return random.randint(1, 5)


class BaseTask(celery.Task):
    """Abstract base class for all tasks in my app."""

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        sentry.captureException(exc)
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        sentry.captureException(exc)
        # end with
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
