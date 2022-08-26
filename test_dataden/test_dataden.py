import csv
from datetime import datetime
from random import seed
import os
import unittest

import pandas as pd

from dataden import dataden, date_functions, non_date_functions


class TestDateGenerator(unittest.TestCase):

    def test_generate_date_before_original(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        diff = -10
        output_date = datetime(2020, 8, 13)
        self.assertEqual(date_functions.generate_date(start_date, diff=diff), output_date)
    
    def test_generate_date_equal_original(self):
        seed(17)
        test_date = datetime(2020, 8, 15)
        diff = 0
        self.assertEqual(date_functions.generate_date(test_date, diff=diff), test_date)

    def test_generate_date_after_original(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        diff = 10
        output_date = datetime(2020, 8, 23)
        self.assertEqual(date_functions.generate_date(start_date, diff=diff), output_date)

    def test_generate_date_no_diff(self):
        seed(17)
        test_date = datetime(2020, 8, 15)
        self.assertEqual(date_functions.generate_date(test_date), test_date)

class TestDateSeriesGenerator(unittest.TestCase):

    def test_generate_date_series_from_series_before_original(self):
        seed(17)
        input_dates = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        relative_date_range = -5
        output_dates = [datetime(2021, 12, 31), datetime(2022, 1, 8)]
        
        self.assertEqual(date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_series_equal_original(self):
        seed(17)
        input_dates = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        output_dates = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        relative_date_range = 0
        self.assertEqual(date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_series_after_original(self):
        seed(17)
        input_dates = [datetime(2022, 1, 1), datetime(2022, 1, 10)]
        output_dates = [datetime(2022, 1, 5), datetime(2022, 1, 13)]
        relative_date_range = 5
        self.assertEqual(date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_date_before_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = -5
        series_length = 2
        output_test_series = [datetime(2021, 12, 31), datetime(2021, 12, 30)]
        self.assertEqual(date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_equal_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 0
        series_length = 2
        output_test_series = [datetime(2022, 1, 1), datetime(2022, 1, 1)]
        self.assertEqual(date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_after_original(self):
        seed(17)
        test_date = datetime(2022, 1, 1)
        relative_date_range = 5
        series_length = 2
        output_test_series = [datetime(2022, 1, 5), datetime(2022, 1, 4)]
        self.assertEqual(date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

class TestDataNullification(unittest.TestCase):

    def test_nullify_rows_date_cols(self):
        input_dates = [
            [datetime(2022, 1, 1), datetime(2022, 1, 1), datetime(2022, 1, 1)],
            [datetime(2022, 1, 1), datetime(2022, 1, 1), datetime(2022, 1, 1)]
        ]
        col_null_fraction = [.5, .5, .5]
        output_dates = [
            [pd.NaT, pd.NaT, pd.NaT],
            [datetime(2022, 1, 1), datetime(2022, 1, 1), datetime(2022, 1, 1)]
        ]
        self.assertEqual(date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8), output_dates)

    def test_col_null_percent_decreasing_error(self):
            input_dates = [
                [datetime(2022, 1, 1), datetime(2022, 1, 1), datetime(2022, 1, 1)],
                [datetime(2022, 1, 1), datetime(2022, 1, 1), datetime(2022, 1, 1)]
            ]
            col_null_fraction = [.5, .6, .4]
            with self.assertRaises(date_functions.ColNullPercentageDecreasingError):
                date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8)

class TestCreateOutput(unittest.TestCase):
    
    def test_create_date_output(self):    
        starting_date = datetime(2022, 1, 1)
        series_length = 10
        col_differences = [10, 10]
        col_null_fraction = [.2, .5]
        seed = 17
        output = [
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 7, 0, 0), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 6, 0, 0), datetime(2022, 1, 10, 0, 0)], 
            [datetime(2022, 1, 5, 0, 0), datetime(2022, 1, 13, 0, 0)], 
            [datetime(2022, 1, 3, 0, 0), datetime(2022, 1, 8, 0, 0)], 
            [datetime(2022, 1, 9, 0, 0), datetime(2022, 1, 15, 0, 0)], 
            [datetime(2022, 1, 5, 0, 0), datetime(2022, 1, 7, 0, 0)], 
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 0, 0)],
        ]
        self.assertEqual(dataden.create_date_output(starting_date, series_length, col_differences, col_null_fraction, seed=seed), output)
    
    def test_export_output(self):
        input_data = [
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 7, 0, 0), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 6, 0, 0), datetime(2022, 1, 10, 0, 0)], 
            [datetime(2022, 1, 5, 0, 0), datetime(2022, 1, 13, 0, 0)], 
            [datetime(2022, 1, 3, 0, 0), datetime(2022, 1, 8, 0, 0)], 
            [datetime(2022, 1, 9, 0, 0), datetime(2022, 1, 15, 0, 0)], 
            [datetime(2022, 1, 5, 0, 0), datetime(2022, 1, 7, 0, 0)], 
            [pd.NaT, pd.NaT], 
            [datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 0, 0)],
        ]
        output_filename = 'test.csv'
        output_data = [
            ['NaT', 'NaT'], 
            ['2022-01-07 00:00:00', 'NaT'], 
            ['NaT', 'NaT'], 
            ['2022-01-06 00:00:00', '2022-01-10 00:00:00'], 
            ['2022-01-05 00:00:00', '2022-01-13 00:00:00'], 
            ['2022-01-03 00:00:00', '2022-01-08 00:00:00'], 
            ['2022-01-09 00:00:00', '2022-01-15 00:00:00'], 
            ['2022-01-05 00:00:00', '2022-01-07 00:00:00'], 
            ['NaT', 'NaT'], 
            ['2022-01-01 00:00:00', '2022-01-01 00:00:00'],
        ]
        try:
            dataden.export_output(input_data, output_filename)
            with open(output_filename) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename)
        self.assertEqual(contents, output_data)

class TestCreateNonDateCol(unittest.TestCase):

    def test_create_non_date_col_lowercase_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'nuyhtsrcaj',
            'tgniwykzbv',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17), test_output)
    
    def test_create_non_date_col_uppercase_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'NUYHTSRCAJ',
            'TGNIWYKZBV',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=False, upper_allowed=True), test_output)

    def test_create_non_date_col_mixed_case_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'BPXpNKIfbt',
            'MnAqSXuZdQ',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True), test_output)
    
    def test_create_non_date_col_numeric_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            '5892776103',
            '7253894908',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=False, numeric_allowed=True), test_output)
    
    def test_create_non_date_col_alphanumeric_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'GY7rVRPgbx',
            'UpFt06y9dY',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True, numeric_allowed=True), test_output)
    
    def test_create_non_date_col_all_char_types_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'M7#v40WibC',
            '3sLx!,D?e8',
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True, numeric_allowed=True, special_allowed=True), test_output)
    
    def test_create_non_date_col_all_char_types_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            None,
            None,
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_allowed=False), test_output)
    
    def test_create_non_date_col_int(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            66,
            53,
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_bound=0, upper_bound = 100), test_output)
    
    def test_create_non_date_col_int_upper_below_lower(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            66,
            53,
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_bound=100, upper_bound = 0), test_output)
    
    def test_create_non_date_col_int_upper_equal_lower(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            100,
            100,
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17, lower_bound=100, upper_bound = 100), test_output)
    
    def test_create_non_date_col_int_no_bounds_provided(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            datetime(2022, 8, 8),
            datetime(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            0,
            0,
            None,
        ]
        self.assertEqual(non_date_functions.create_non_date_col(test_datatype, test_col_relation, seed=17), test_output)