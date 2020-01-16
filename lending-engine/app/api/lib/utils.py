import random

from app.config.config import Config


def backoff(attempts):
    """ prevent hammering service with exponential retry based on attempts """
    """ worst case is 6 ** 5 == 7776 seconds """
    return random.uniform(2, 6) ** attempts


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )
