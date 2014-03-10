from __future__ import unicode_literals, print_function
import unittest
import os
from sys import stderr
import datetime
from pprint import pformat

from ops.tram import minutes_data


class TestDirectoryData(unittest.TestCase):

    def test_minutes(self):
        dt = datetime.datetime.now()
        path = minutes_data(dt, pre_path='tests')
        self.assertTrue(os.path.isdir(path))

    

