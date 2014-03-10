from __future__ import unicode_literals, print_function
import unittest
from sys import stderr
from pprint import pformat

from ops.extract import ExtractYearIndex


class TestExtract(unittest.TestCase):
    
    def test_minutes_of_year(self):
        eyi = ExtractYearIndex()

        d = eyi.minute_year_index()
        print(pformat(d))
        self.assertIn(2011, d)
        self.assertIn(1999, d)



