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


def generate_date_series_from_series(original_series: list, relative_date_range: int):
    """
    This function will generate a Series of random dates, relative 
    to another series of dates.
    """
    if relative_date_range == 0:
        new_series = [generate_date(element) for element in original_series]
    else:
        new_series = [generate_date(element, diff=relative_date_range) for element in original_series]
    return new_series


def generate_date_series_from_date(baseline_date: datetime, relative_date_range: int, series_length: int):
    """
    This will generate a series of a specified length relative to a date.
    """
    date_list = [baseline_date] * series_length
    return generate_date_series_from_series(date_list, relative_date_range)

def nullify_rows(df: pd.DataFrame, col_null_fraction: dict, cols_matching_nullity: dict, **kwargs):
    """
    This function will ensure columns match a percentage null.
    It will also aligns columns that need the same rows to
    be null or not null.
    Having rows in columns match on null values takes precedence.
    """
    seed = kwargs.get('seed', None)

    cols_to_skip = cols_matching_nullity.values()
    cols_to_iterate = list(set(df.columns) - set(cols_to_skip))

    for col in cols_to_iterate:
        fraction = col_null_fraction.get(col)
        df.loc[df.sample(frac=fraction, random_state=seed).index, col] = None
    for key, value in cols_matching_nullity.items():
        df.loc[df[key].isnull(), value] = pd.NaT
    return df

