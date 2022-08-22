from random import randrange
from datetime import timedelta


def generate_date(start, end):
    """
    This function will return a random date between two dates.
    """
    delta = (end - start).days
    random_number_days = randrange(delta)
    return start + timedelta(days=random_number_days)
