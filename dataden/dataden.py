from random import randrange
from datetime import timedelta


def generate_date(start, end):
    """
    This function will return a random date between two dates.
    """
    try:
        delta = (end - start).days
    except ValueError():
        raise ValueError()
    random_number_days = randrange(delta)
    return start + timedelta(days=random_number_days)
