from random import randrange, seed, random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


class ColNullPercentageDecreasingError(Exception):
    def __init__(self):
        message = "Col Null Percentage decreases between consecutive column. Columns that have a decrease in null percentage will be treated as the previous column's null percentage."
        super().__init__(message)


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


def nullify_rows_date_cols(data_list: list, col_null_fraction: list, **kwargs):
    """
    This function will ensure columns match a percentage null.
    It will also aligns columns that need the same rows to
    be null or not null.
    This will run on columns sequentially. If a row in one column
    is null, then it will be null in subsequent columns.
    This is because the goal of this is to create mock data of
    dates in a sequential process.
    """
    seed_number = kwargs.get('seed', None)
    if seed_number is not None:
        seed(seed_number)

    if not all(i <= j for i, j in zip(col_null_fraction, col_null_fraction[1:])):
        raise ColNullPercentageDecreasingError

    col_null_percentage_increases = [j-i for i, j in zip(col_null_fraction[:-1], col_null_fraction[1:])]
    col_null_percentage_increases.insert(0, col_null_fraction[0])

    for col in range(len(data_list[0])):
        for row in range(len(data_list)):
            if col > 0 and pd.isnull(data_list[row][col-1]):
                data_list[row][col] = pd.NaT
            else:
                if random() < col_null_percentage_increases[col]:
                    data_list[row][col] = pd.NaT
    return data_list
