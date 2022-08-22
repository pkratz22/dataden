from datetime import datetime
from random import seed
import unittest

from dataden import dataden


class TestDateGenerator(unittest.TestCase):

    def test_generate_date_proper_input(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        end_date = datetime(2020, 8, 30)
        output_date = datetime(2020, 8, 23)
        self.assertEqual(dataden.generate_date(start_date, end_date), output_date)
    
    def test_generate_date(self):
        seed(17)
        start_date = datetime(2020, 8, 15)
        end_date = datetime(2020, 8, 1)
        self.assertRaises(ValueError, dataden.generate_date, start_date, end_date)