from __future__ import unicode_literals, print_function
import unittest
from sys import stderr
import datetime
from pprint import pformat

from ops.tram import minutes_data


class TestDirectoryData(unittest.TestCase):

    def test_minutes(self):
        dt = datetime.datetime.now()
        minutes_data(dt)

    

