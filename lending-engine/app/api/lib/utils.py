import random

def backoff(attempts):
    """ prevent hammering service with exponential retry based on attempts """
    """ worst case is 6 ** 5 == 7776 seconds """
    return random.uniform(2, 6) ** attempts
