from random import randrange
from datetime import timedelta


def generate_date(start, **kwargs):
    """
    This function will return a random date between two dates.
    """
    end = kwargs.get('end', None)
    if end is None:
        return start
    try:
        delta = (end - start).days
    except ValueError():
        raise ValueError()
    random_number_days = randrange(delta)
    return start + timedelta(days=random_number_days)
