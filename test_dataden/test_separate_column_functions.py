from datetime import date
import unittest

import pandas as pd

from dataden import separate_column_functions


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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=False,
                upper_allowed=True,
            ),
            test_output,
        )

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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=True,
                upper_allowed=True,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=False,
                numeric_allowed=True,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=True,
                upper_allowed=True,
                numeric_allowed=True,
            ),
            test_output,
        )
    
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
            'M6#v3ZWibC',
            '2sKx9.D?e7',
            None,
        ]
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=True,
                upper_allowed=True,
                numeric_allowed=True,
                special_allowed=True,
            ),
            test_output,
        )
    
    def test_create_individual_col_all_char_types_string_no_char_types_allowed(self):
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_allowed=False,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=0,
                upper_bound=100,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=100,
                upper_bound=0,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=100,
                upper_bound=100,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
            ),
            test_output,
        )

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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                item_list=test_list,
            ),
            test_output,
        )

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
            '1961-09-16',
            '1959-04-16',
            None,
        ]
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=test_lower_bound,
                upper_bound=test_upper_bound,
            ),
            test_output,
        )
    
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
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=test_lower_bound,
                upper_bound=test_upper_bound,
            ),
            test_output,
        )
     
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
            '1961-09-16',
            '1959-04-16',
            None,
        ]
        self.assertEqual(
            separate_column_functions.create_individual_col(
                test_datatype,
                test_col_relation,
                seed=17,
                lower_bound=test_lower_bound,
                upper_bound=test_upper_bound,
            ),
            test_output,
        )