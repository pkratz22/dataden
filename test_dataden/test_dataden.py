import csv
from datetime import date
from random import seed
import os
import unittest

import pandas as pd

from dataden import dataden, related_date_functions, separate_column_functions


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
        
        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_series_equal_original(self):
        seed(17)
        input_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        output_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        relative_date_range = 0
        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_series_after_original(self):
        seed(17)
        input_dates = [date(2022, 1, 1), date(2022, 1, 10)]
        output_dates = [date(2022, 1, 5), date(2022, 1, 13)]
        relative_date_range = 5
        self.assertEqual(related_date_functions.generate_date_series_from_series(input_dates, relative_date_range), output_dates)

    def test_generate_date_series_from_date_before_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = -5
        series_length = 2
        output_test_series = [date(2021, 12, 31), date(2021, 12, 30)]
        self.assertEqual(related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_equal_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = 0
        series_length = 2
        output_test_series = [date(2022, 1, 1), date(2022, 1, 1)]
        self.assertEqual(related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

    def test_generate_date_series_from_date_after_original(self):
        seed(17)
        test_date = date(2022, 1, 1)
        relative_date_range = 5
        series_length = 2
        output_test_series = [date(2022, 1, 5), date(2022, 1, 4)]
        self.assertEqual(related_date_functions.generate_date_series_from_date(test_date, relative_date_range, series_length), output_test_series)

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
        self.assertEqual(related_date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8), output_dates)

    def test_col_null_percent_decreasing_error(self):
            input_dates = [
                [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)],
                [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)]
            ]
            col_null_fraction = [.5, .6, .4]
            with self.assertRaises(related_date_functions.ColNullPercentageDecreasingError):
                related_date_functions.nullify_rows_date_cols(input_dates, col_null_fraction, seed=8)

class TestCreateOutput(unittest.TestCase):
    
    def test_create_date_output(self):    
        starting_date = date(2022, 1, 1)
        series_length = 10
        col_differences = [10, 10]
        col_null_fraction = [.2, .5]
        seed = 17
        output = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        self.assertEqual(dataden.create_date_output(starting_date, series_length, col_differences, col_null_fraction, seed=seed), output)
    
    def test_export_output(self):
        input_data = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        output_filename = 'test.csv'
        output_data = [
            ['NaT', 'NaT'], 
            ['2022-01-07', 'NaT'], 
            ['NaT', 'NaT'], 
            ['2022-01-06', '2022-01-10'], 
            ['2022-01-05', '2022-01-13'], 
            ['2022-01-03', '2022-01-08'], 
            ['2022-01-09', '2022-01-15'], 
            ['2022-01-05', '2022-01-07'], 
            ['NaT', 'NaT'], 
            ['2022-01-01', '2022-01-01'],
        ]
        try:
            dataden.export_output(input_data, output_filename)
            with open(output_filename) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename)
        self.assertEqual(contents, output_data)

class TestSeparateCol(unittest.TestCase):

    def test_create_individual_col_lowercase_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'nuyhtsrcaj',
            'tgniwykzbv',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17), test_output)
    
    def test_create_individual_col_uppercase_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'NUYHTSRCAJ',
            'TGNIWYKZBV',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=False, upper_allowed=True), test_output)

    def test_create_individual_col_mixed_case_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'BPXpNKIfbt',
            'MnAqSXuZdQ',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True), test_output)
    
    def test_create_individual_col_numeric_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            '5892776103',
            '7253894908',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=False, numeric_allowed=True), test_output)
    
    def test_create_individual_col_alphanumeric_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'GY7rVRPgbx',
            'UpFt06y9dY',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True, numeric_allowed=True), test_output)
    
    def test_create_individual_col_all_char_types_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            'M7#v40WibC',
            '3sLx!,D?e8',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=True, upper_allowed=True, numeric_allowed=True, special_allowed=True), test_output)
    
    def test_create_individual_col_all_char_types_string(self):
        test_datatype = 'string'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            None,
            None,
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_allowed=False), test_output)
    
    def test_create_individual_col_int(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            66,
            53,
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=0, upper_bound = 100), test_output)
    
    def test_create_individual_col_int_upper_below_lower(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            66,
            53,
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=100, upper_bound = 0), test_output)
    
    def test_create_individual_col_int_upper_equal_lower(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            100,
            100,
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=100, upper_bound = 100), test_output)
    
    def test_create_individual_col_int_no_bounds_provided(self):
        test_datatype = 'int'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_output = [
            None,
            0,
            0,
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17), test_output)

    def test_create_individual_col_list(self):
        test_datatype = 'list'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_list = ['Apple', 'Banana', 'Carrot']
        test_output = [
            None,
            'Carrot',
            'Banana',
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, item_list=test_list), test_output)

    def test_create_individual_col_date_start_after_end(self):
        test_datatype = 'date'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_upper_bound = date(1950, 1, 1)
        test_lower_bound = date(1970, 1, 1)
        test_output = [
            None,
            date(1961, 9, 16),
            date(1959, 4, 16),
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=test_lower_bound, upper_bound=test_upper_bound), test_output)
    
    def test_create_individual_col_date_start_equal_end(self):
        test_datatype = 'date'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_upper_bound = date(1950, 1, 1)
        test_lower_bound = date(1950, 1, 1)
        test_output = [
            None,
            date(1950, 1, 1),
            date(1950, 1, 1),
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=test_lower_bound, upper_bound=test_upper_bound), test_output)
    
    
    def test_create_individual_col_date_start_before_end(self):
        test_datatype = 'date'
        test_col_relation = [
            pd.NaT,
            date(2022, 8, 8),
            date(2022, 8, 5),
            None,
        ]
        test_lower_bound = date(1950, 1, 1)
        test_upper_bound = date(1970, 1, 1)
        test_output = [
            None,
            date(1961, 9, 16),
            date(1959, 4, 16),
            None,
        ]
        self.assertEqual(separate_column_functions.create_individual_col(test_datatype, test_col_relation, seed=17, lower_bound=test_lower_bound, upper_bound=test_upper_bound), test_output)
    

class TestGetColumn(unittest.TestCase):

    def test_get_column_standard(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        position_to_extract = 0
        output = [
            pd.NaT,
            date(2022, 1, 7),
            pd.NaT,
            date(2022, 1, 6),
            date(2022, 1, 5),
            date(2022, 1, 3),
            date(2022, 1, 9),
            date(2022, 1, 5),
            pd.NaT,
            date(2022, 1, 1),
        ]
        self.assertEqual(dataden.get_column(input_list, position_to_extract), output)
    
    def test_get_column_above_start(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        position_to_extract = 10
        output = [
            pd.NaT,
            pd.NaT,
            pd.NaT,
            date(2022, 1, 10),
            date(2022, 1, 13),
            date(2022, 1, 8),
            date(2022, 1, 15),
            date(2022, 1, 7),
            pd.NaT,
            date(2022, 1, 1),
        ]
        self.assertEqual(dataden.get_column(input_list, position_to_extract), output)
    
    def test_get_column_below_start(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        position_to_extract = -5
        output = [
            pd.NaT,
            date(2022, 1, 7),
            pd.NaT,
            date(2022, 1, 6),
            date(2022, 1, 5),
            date(2022, 1, 3),
            date(2022, 1, 9),
            date(2022, 1, 5),
            pd.NaT,
            date(2022, 1, 1),
        ]
        self.assertEqual(dataden.get_column(input_list, position_to_extract), output)

class TestInsertColumn(unittest.TestCase):

    def test_insert_column_standard(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        new_list = [
            None,
            'asfdasdfas',
            None,
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            None,
            'asfdasdfas',
        ]
        insert_pos = 2
        output = [
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 7), pd.NaT, 'asfdasdfas'], 
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 6), date(2022, 1, 10), 'asfdasdfas'], 
            [date(2022, 1, 5), date(2022, 1, 13), 'asfdasdfas'], 
            [date(2022, 1, 3), date(2022, 1, 8), 'asfdasdfas'], 
            [date(2022, 1, 9), date(2022, 1, 15), 'asfdasdfas'], 
            [date(2022, 1, 5), date(2022, 1, 7), 'asfdasdfas'], 
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 1), date(2022, 1, 1), 'asfdasdfas'],
        ]
        self.assertEqual(dataden.insert_column(input_list, new_list, insert_pos), output)

    def test_insert_column_high_insert_pos(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        new_list = [
            None,
            'asfdasdfas',
            None,
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            None,
            'asfdasdfas',
        ]
        insert_pos = 5
        output = [
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 7), pd.NaT, 'asfdasdfas'], 
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 6), date(2022, 1, 10), 'asfdasdfas'], 
            [date(2022, 1, 5), date(2022, 1, 13), 'asfdasdfas'], 
            [date(2022, 1, 3), date(2022, 1, 8), 'asfdasdfas'], 
            [date(2022, 1, 9), date(2022, 1, 15), 'asfdasdfas'], 
            [date(2022, 1, 5), date(2022, 1, 7), 'asfdasdfas'], 
            [pd.NaT, pd.NaT, None], 
            [date(2022, 1, 1), date(2022, 1, 1), 'asfdasdfas'],
        ]
        self.assertEqual(dataden.insert_column(input_list, new_list, insert_pos), output)

    def test_insert_column_low_insert_pos(self):
        input_list = [
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 7), pd.NaT], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 6), date(2022, 1, 10)], 
            [date(2022, 1, 5), date(2022, 1, 13)], 
            [date(2022, 1, 3), date(2022, 1, 8)], 
            [date(2022, 1, 9), date(2022, 1, 15)], 
            [date(2022, 1, 5), date(2022, 1, 7)], 
            [pd.NaT, pd.NaT], 
            [date(2022, 1, 1), date(2022, 1, 1)],
        ]
        new_list = [
            None,
            'asfdasdfas',
            None,
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
            None,
            'asfdasdfas',
        ]
        insert_pos = -6
        output = [
            [None, pd.NaT, pd.NaT], 
            ['asfdasdfas', date(2022, 1, 7), pd.NaT], 
            [None, pd.NaT, pd.NaT], 
            ['asfdasdfas', date(2022, 1, 6), date(2022, 1, 10)], 
            ['asfdasdfas', date(2022, 1, 5), date(2022, 1, 13)], 
            ['asfdasdfas', date(2022, 1, 3), date(2022, 1, 8)], 
            ['asfdasdfas', date(2022, 1, 9), date(2022, 1, 15)], 
            ['asfdasdfas', date(2022, 1, 5), date(2022, 1, 7)], 
            [None, pd.NaT, pd.NaT], 
            ['asfdasdfas', date(2022, 1, 1), date(2022, 1, 1)],
        ]
        self.assertEqual(dataden.insert_column(input_list, new_list, insert_pos), output)
