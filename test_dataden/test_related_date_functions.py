from datetime import date
from random import seed
import unittest

import pandas as pd

from dataden import related_date_functions


class TestDateGenerator(unittest.TestCase):

    def test_generate_date_before_original(self):
        seed(17)
        start_date = date(2020, 8, 15)
        diff = -10
        output_date = date(2020, 8, 13)
        self.assertEqual(related_date_functions.generate_date(start_date, diff=diff), output_date)

    def test_generate_date_equal_original(self):
        seed(17)
        test_date = date(2020, 8, 15)
        diff = 0
        self.assertEqual(related_date_functions.generate_date(test_date, diff=diff), test_date)

    def test_generate_date_after_original(self):
        seed(17)
        start_date = date(2020, 8, 15)
        diff = 10
        output_date = date(2020, 8, 23)
        self.assertEqual(related_date_functions.generate_date(start_date, diff=diff), output_date)

    def test_generate_date_no_diff(self):
        seed(17)
        test_date = date(2020, 8, 15)
        self.assertEqual(related_date_functions.generate_date(test_date), test_date)


class TestDateSeriesGenerator(unittest.TestCase):

    def test_generate_date_series_from_series_before_original(self):
        seed(17)
        input_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        relative_date_range = -5
        output_dates = [date(2021, 12, 31), date(2022, 1, 8)]

        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range),
                         output_dates)

    def test_generate_date_series_from_series_equal_original(self):
        seed(17)
        input_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        output_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        relative_date_range = 0
        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range),
                         output_dates)

    def test_generate_date_series_from_series_after_original(self):
        seed(17)
        input_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        output_dates = [date(2022, 1, 5), date(2022, 1, 13)]
        relative_date_range = 5
        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range),
                         output_dates)

    def test_generate_date_series_from_date_before_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = -5
        series_length = 2
        output_test_series = [date(2021, 12, 31), date(2021, 12, 30)]
        self.assertEqual(
            related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length),
            output_test_series)

    def test_generate_date_series_from_date_equal_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = 0
        series_length = 2
        output_test_series = [date(2022, 1, 1), date(2022, 1, 1)]
        self.assertEqual(
            related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length),
            output_test_series)

    def test_generate_date_series_from_date_after_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = 5
        series_length = 2
        output_test_series = [date(2022, 1, 5), date(2022, 1, 4)]
        self.assertEqual(
            related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length),
            output_test_series)


class TestDataNullification(unittest.TestCase):

    def test_nullify_rows_date_cols(self):
        input_dates = [
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)],
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)]
        ]
        col_null_fraction = [.5, .5, .5]
        output_dates = [
            [pd.NaT, pd.NaT, pd.NaT],
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)]
        ]
        self.assertEqual(related_date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8),
                         output_dates)

    def test_col_null_percent_decreasing_error(self):
        input_dates = [
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)],
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)]
        ]
        col_null_fraction = [.5, .6, .4]
        with self.assertRaises(related_date_functions.ColNullPercentageDecreasingError):
            related_date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8)