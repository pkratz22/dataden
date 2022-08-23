from datetime import datetime
from platform import release
from random import seed
import unittest

import pandas as pd

from dataden import dataden


class TestDateGenerator(unittest.TestCase):

    def test_generate_date_before_original(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        diff = -10
        output_date = datetime(2020, 8, 13)
        self.assertEqual(dataden.generate_date(start_date, diff=diff), output_date)
    
    def test_generate_date_equal_original(self):
        seed(17)
        test_date = datetime(2020, 8, 15)
        self.assertEqual(dataden.generate_date(test_date), test_date)

    def test_generate_date_after_original(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        diff = 10
        output_date = datetime(2020, 8, 23)
        self.assertEqual(dataden.generate_date(start_date, diff=diff), output_date)

class TestDateSeriesGenerator(unittest.TestCase):

    def test_generate_date_series_from_series_before_original(self):
        seed(17)
        input_test_series = pd.Series(
            data={
                0: datetime(2022, 1, 1),
                1: datetime(2022, 1, 10)
            },
            index=[0, 1]
        )
        output_test_series = pd.Series(
            data={
                0: datetime(2021, 12, 31),
                1: datetime(2022, 1, 8)
            },
            index=[0,1]
        )
        relative_date_range = -5
        pd.testing.assert_series_equal(dataden.generate_date_series_from_series(input_test_series, relative_date_range), output_test_series)

    def test_generate_date_series_from_series_equal_original(self):
        seed(17)
        test_series = pd.Series(
            data={
                0: datetime(2022, 1, 1),
                1: datetime(2022, 1, 10)
            },
            index=[0, 1]
        )
        relative_date_range = 0
        pd.testing.assert_series_equal(dataden.generate_date_series_from_series(test_series, relative_date_range), test_series)


    def test_generate_date_series_from_series_after_original(self):
        seed(17)
        input_test_series = pd.Series(
            data={
                0: datetime(2022, 1, 1),
                1: datetime(2022, 1, 10)
            },
            index=[0, 1]
        )
        output_test_series = pd.Series(
            data={
                0: datetime(2022, 1, 5),
                1: datetime(2022, 1, 13)
            },
            index=[0,1]
        )
        relative_date_range = 5
        pd.testing.assert_series_equal(dataden.generate_date_series_from_series(input_test_series, relative_date_range), output_test_series)

    def test_generate_date_series_from_date_before_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = -5
        series_length = 2
        output_test_series = pd.Series(
            data={
                0: datetime(2021, 12, 31),
                1: datetime(2021, 12, 30)
            },
            index=[0,1]
        )
        pd.testing.assert_series_equal(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_equal_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 0
        series_length = 2
        output_test_series = pd.Series(
            data={
                0: datetime(2022, 1, 1),
                1: datetime(2022, 1, 1)
            },
            index=[0,1]
        )
        pd.testing.assert_series_equal(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_after_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 5
        series_length = 2
        output_test_series = pd.Series(
            data={
                0: datetime(2022, 1, 5),
                1: datetime(2022, 1, 4)
            },
            index=[0,1]
        )
        pd.testing.assert_series_equal(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)