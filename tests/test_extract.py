from __future__ import unicode_literals, print_function
import unittest
from sys import stderr
from pprint import pformat

from ops.extract import (ExtractYearIndex, ExtractMinutesList)

base_resources = 'tests/resources/'

class TestExtract(unittest.TestCase):

    def test_minutes_of_year(self):
        path = base_resources+'index.cfm?c=56676'
        eyi = ExtractYearIndex()

        with open(path, 'r') as f:
            src = f.read()
            eyi.url=None
            eyi.src = src

            d = eyi.minute_year_index()
            print(pformat(d), file=stderr)
            self.assertIn(2011, d)
            self.assertIn(1999, d)
            self.assertEqual(d[2006],\
            'http://efiles.portlandoregon.gov/webdrawer/rec/3029951/')


    def test_minutes_list_query(self):
        eml = ExtractMinutesList()
        x = eml.minutes_list_url(4187317)
        print(x, file=stderr)

