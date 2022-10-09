import csv
from datetime import date
from random import seed
import os
import unittest

import pandas as pd

from dataden import dataden, related_date_functions, separate_column_functions


class TestCreateRelatedDateOutput(unittest.TestCase):

    def test_create_related_date_output(self):
        starting_date = date(2022, 1, 1)
        series_length = 10
        col_differences = [10, 10]
        col_null_fraction = [.2, .5]
        seed = 17
        output = [
            [pd.NaT, pd.NaT],
            ['2022-01-07', pd.NaT],
            [pd.NaT, pd.NaT],
            ['2022-01-06', '2022-01-10'],
            ['2022-01-05', '2022-01-13'],
            ['2022-01-03', '2022-01-08'],
            ['2022-01-09', '2022-01-15'],
            ['2022-01-05', '2022-01-07'],
            [pd.NaT, pd.NaT],
            ['2022-01-01', '2022-01-01'],
        ]
        dd_test = dataden.dataden()
        dd_test.create_related_date_output(starting_date, series_length, col_differences, col_null_fraction, seed=seed)
        self.assertEqual(dd_test.data, output)

    def test_create_related_date_output_change_format(self):
        starting_date = date(2022, 1, 1)
        series_length = 10
        col_differences = [10, 10]
        col_null_fraction = [.2, .5]
        seed = 17
        output = [
            [pd.NaT, pd.NaT],
            ['Jan 7, 2022', pd.NaT],
            [pd.NaT, pd.NaT],
            ['Jan 6, 2022', 'Jan 10, 2022'],
            ['Jan 5, 2022', 'Jan 13, 2022'],
            ['Jan 3, 2022', 'Jan 8, 2022'],
            ['Jan 9, 2022', 'Jan 15, 2022'],
            ['Jan 5, 2022', 'Jan 7, 2022'],
            [pd.NaT, pd.NaT],
            ['Jan 1, 2022', 'Jan 1, 2022'],
        ]
        dd_test = dataden.dataden()
        dd_test.create_related_date_output(starting_date, series_length, col_differences, col_null_fraction, date_format='%b %-d, %Y', seed=seed)
        self.assertEqual(dd_test.data, output)

class TestExportOutput(unittest.TestCase):

    def test_export_output_no_headers_no_subsetting(self):
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
        dd_test = dataden.dataden(input_data)
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
            dd_test.export_output(output_filename)
            with open(output_filename) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename)
        self.assertEqual(contents, output_data)

    def test_export_output_headers_no_subsetting(self):
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
        dd_test = dataden.dataden(input_data)
        dd_test.create_headers(['col 1', 'col 2'])
        output_filename = 'test.csv'
        output_data = [
            ['col 1', 'col 2'],
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
            dd_test.export_output(output_filename)
            with open(output_filename) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename)
        self.assertEqual(contents, output_data)

    def test_export_output_headers_no_subsetting_multiple_runs(self):
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
        dd_test = dataden.dataden(input_data)
        dd_test.create_headers(['col 1', 'col 2'])
        output_filename1 = 'test1.csv'
        output_filename2 = 'test2.csv'
        output_data = [
            ['col 1', 'col 2'],
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
            print('run 1')
            dd_test.export_output(output_filename1)
            print('run 2')
            dd_test.export_output(output_filename2)
            with open(output_filename2) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename1)
            os.remove(output_filename2)
        self.assertEqual(contents, output_data)

    def test_export_output_headers_subsetting(self):
        input_data = [
            [pd.NaT, pd.NaT, pd.NaT],
            [date(2022, 1, 7), pd.NaT, date(2022, 1, 5)],
            [pd.NaT, pd.NaT, pd.NaT],
            [date(2022, 1, 6), date(2022, 1, 10), date(2022, 1, 8)],
            [date(2022, 1, 5), date(2022, 1, 13), date(2022, 1, 11)],
            [date(2022, 1, 3), date(2022, 1, 8), date(2022, 1, 6)],
            [date(2022, 1, 9), date(2022, 1, 15), date(2022, 1, 13)],
            [date(2022, 1, 5), date(2022, 1, 7), date(2022, 1, 5)],
            [pd.NaT, pd.NaT, pd.NaT],
            [date(2022, 1, 1), date(2022, 1, 1), date(2022, 1, 1)],
        ]
        subset = [0,2]
        dd_test = dataden.dataden(input_data)
        dd_test.create_headers(['col 1', 'col 2', 'col 3'])
        output_filename = 'test.csv'
        output_data = [
            ['col 1', 'col 3'],
            ['NaT', 'NaT'],
            ['2022-01-07', '2022-01-05'],
            ['NaT', 'NaT'],
            ['2022-01-06', '2022-01-08'],
            ['2022-01-05', '2022-01-11'],
            ['2022-01-03', '2022-01-06'],
            ['2022-01-09', '2022-01-13'],
            ['2022-01-05', '2022-01-05'],
            ['NaT', 'NaT'],
            ['2022-01-01', '2022-01-01'],
        ]
        try:
            dd_test.export_output(output_filename, subset=subset)
            with open(output_filename) as f:
                contents = list(csv.reader(f))
        finally:
            os.remove(output_filename)
        self.assertEqual(contents, output_data)
        


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
        dd_test = dataden.dataden(input_list)
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
        self.assertEqual(dd_test.get_column(position_to_extract), output)

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
        dd_test = dataden.dataden(input_list)
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
        self.assertEqual(dd_test.get_column(position_to_extract), output)

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
        dd_test = dataden.dataden(input_list)
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
        self.assertEqual(dd_test.get_column(position_to_extract), output)

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
        dd_test = dataden.dataden(input_list)
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
        dd_test.insert_column(new_list, insert_pos)
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
        self.assertEqual(dd_test.data, output)

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
        dd_test = dataden.dataden(input_list)
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
        dd_test.insert_column(new_list, insert_pos)
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
        self.assertEqual(dd_test.data, output)

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
        dd_test = dataden.dataden(input_list)
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
        dd_test.insert_column(new_list, insert_pos)
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
        self.assertEqual(dd_test.data, output)

    def test_insert_column_empty_list(self):
        dd_test = dataden.dataden()
        new_list = [
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
        ]
        insert_pos = 0
        output = [
            'asfdasdfas',
            'asfdasdfas',
            'asfdasdfas',
        ]
        dd_test.insert_column(new_list, insert_pos)
        self.assertEqual(dd_test.data, output)

class TestInsertIndividualColumn(unittest.TestCase):

    def test_insert_individual_column_original_not_empty(self):
        current_list = [
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
            'hello',
        ]
        dd_test = dataden.dataden(current_list)
        position_of_column_to_match_nulls = 0
        position_to_insert = 0
        num_rows = 10
        datatype = 'string'
        dd_test.insert_individual_columns(position_of_column_to_match_nulls, position_to_insert, num_rows, datatype, seed=17)
        output = [
            ['nuyhtsrcaj', 'hello'],
            ['tgniwykzbv', 'hello'],
            ['wdsoyfowqi', 'hello'],
            ['cymzdvvxaj', 'hello'],
            ['btjyjuwgoy', 'hello'],
            ['njgufpoodr', 'hello'],
            ['xiixphatjm', 'hello'],
            ['hqsibzxaor', 'hello'],
            ['ktypkfgdcf', 'hello'],
            ['vnuxvbycuv', 'hello'],
        ]
        self.assertEqual(dd_test.data, output)

    def test_insert_individual_column_original_empty(self):
        dd_test = dataden.dataden()
        position_of_column_to_match_nulls = 0
        position_to_insert = 0
        num_rows = 10
        datatype = 'string'
        output = [
            'nuyhtsrcaj',
            'tgniwykzbv',
            'wdsoyfowqi',
            'cymzdvvxaj',
            'btjyjuwgoy',
            'njgufpoodr',
            'xiixphatjm',
            'hqsibzxaor',
            'ktypkfgdcf',
            'vnuxvbycuv',
            ]
        dd_test.insert_individual_columns(position_of_column_to_match_nulls, position_to_insert, num_rows, datatype, seed=17)
        self.assertEqual(dd_test.data, output)

class TestCreateHeaders(unittest.TestCase):

    def test_insert_headers_headers_not_list(self):
        dd_test = dataden.dataden(data=[[1],[1],[1]])
        with self.assertRaises(dataden.InputTypeError):
            dd_test.create_headers('fake_header')

    def test_insert_headers_bad_length(self):
        dd_test = dataden.dataden(data=[[1,1,1]])
        with self.assertRaises(dataden.InputLogicError):
            dd_test.create_headers(['test'])

    def test_insert_headers(self):
        dd_test = dataden.dataden(data=[[1,1,1]])
        header_cols = ['col 1', 'col 2', 'col 3']
        dd_test.create_headers(header_cols)
        self.assertEquals(dd_test.headers, header_cols)
