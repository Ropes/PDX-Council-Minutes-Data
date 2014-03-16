from __future__ import unicode_literals, print_function
import datetime
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.transform import stop_words

base_resources = '{}/tests/resources/'.format(os.getcwd())


class TestTransformOps(unittest.TestCase):

    def test_stop_words(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  
            print(stopped, file=stderr)

