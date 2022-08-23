from random import randrange, seed
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_date(start: datetime, **kwargs):
    """
    This function will return a random date between two dates.
    """
    diff = kwargs.get('diff', None)
    if diff is None:
        return start
    elif diff < 0:
        random_number_of_days = randrange(diff, 0)
    elif diff > 0:
        random_number_of_days = randrange(0, diff)
    else:
        return start  
    return start + timedelta(days=random_number_of_days)


def generate_date_series_from_series(original_series: pd.Series, relative_date_range: int):
    """
    This function will generate a Series of random dates, relative 
    to another series of dates.
    """
    if relative_date_range == 0:
        new_series = original_series.apply(generate_date)
    else:
        new_series = original_series.apply(generate_date, diff=relative_date_range)
    return new_series


def generate_date_series_from_date(baseline_date: datetime, relative_date_range: int, series_length: int):
    """
    This will generate a series of a specified length relative to a date.
    """
    date_list = pd.Series([baseline_date] * series_length)
    return generate_date_series_from_series(date_list, relative_date_range)
