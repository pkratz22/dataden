from datetime import datetime
from random import seed
import unittest

from dataden import dataden


class TestDateGenerator(unittest.TestCase):

    def test_generate_date_start_before_end(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        end_date = datetime(2020, 8, 30)
        output_date = datetime(2020, 8, 23)
        self.assertEqual(dataden.generate_date(start_date, end=end_date), output_date)
    
    def test_generate_date_no_end_date(self):
        seed(17)
        test_date = datetime(2020, 8, 15)
        self.assertEqual(dataden.generate_date(test_date), test_date)

    def test_generate_date_start_after_end(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        end_date = datetime(2020, 8, 1)
        self.assertRaises(ValueError, dataden.generate_date, start_date, end=end_date)
    