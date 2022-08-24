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
        input = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        relative_date_range = -5
        output = [datetime(2021, 12, 31), datetime(2022, 1, 8)]
        
        self.assertEqual(dataden.generate_date_series_from_series(input, relative_date_range), output)

    def test_generate_date_series_from_series_equal_original(self):
        seed(17)
        input = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        output = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        relative_date_range = 0
        self.assertEqual(dataden.generate_date_series_from_series(input, relative_date_range), output)

    def test_generate_date_series_from_series_after_original(self):
        seed(17)
        input = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        output = [datetime(2022, 1, 5), datetime(2022, 1, 13)]
        relative_date_range = 5
        self.assertEqual(dataden.generate_date_series_from_series(input, relative_date_range), output)

    def test_generate_date_series_from_date_before_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = -5
        series_length = 2
        output_test_series = [datetime(2021, 12, 31), datetime(2021, 12, 30)]
        self.assertEqual(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_equal_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 0
        series_length = 2
        output_test_series = [datetime(2022, 1, 1), datetime(2022, 1, 1)]
        self.assertEqual(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_after_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 5
        series_length = 2
        output_test_series = [datetime(2022, 1, 5), datetime(2022, 1, 4)]
        self.assertEqual(dataden.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

class TestDataNullification(unittest.TestCase):

    def test_nullify_rows(self):
        test_input_df = pd.DataFrame(data={
            'date_col1': [datetime(2022, 1, 1), datetime(2022, 1, 1)],
            'date_col2': [datetime(2022, 1, 1), datetime(2022, 1, 1)]
            }
        )
        col_null_fraction = {
            'date_col1': .5,
            'date_col2': .5
        }
        cols_matching_nullity = {}
        test_output_df = pd.DataFrame(data={
            'date_col1': [None, datetime(2022, 1, 1)],
            'date_col2': [None, datetime(2022, 1, 1)]
            }
        )
        pd.testing.assert_frame_equal(dataden.nullify_rows(test_input_df, col_null_fraction, cols_matching_nullity, seed=17), test_output_df)

    def test_nullify_rows_with_col_matching(self):
        test_input_df = pd.DataFrame(data={
            'date_col1': [datetime(2022, 1, 1), datetime(2022, 1, 1)],
            'date_col2': [datetime(2022, 1, 1), datetime(2022, 1, 1)],
            'date_col3': [datetime(2022, 1, 1), datetime(2022, 1, 1)]
            }
        )
        col_null_fraction = {
            'date_col1': 0,
            'date_col2': .5
        }
        cols_matching_nullity = {
            'date_col2': 'date_col3'
        }
        test_output_df = pd.DataFrame(data={
            'date_col1': [datetime(2022, 1, 1), datetime(2022, 1, 1)],
            'date_col2': [None, datetime(2022, 1, 1)],
            'date_col3': [None, datetime(2022, 1, 1)]
            }
        )
        pd.testing.assert_frame_equal(dataden.nullify_rows(test_input_df, col_null_fraction, cols_matching_nullity, seed=17), test_output_df)