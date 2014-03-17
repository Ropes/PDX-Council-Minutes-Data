from __future__ import unicode_literals, print_function
import datetime
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.transform import stop_words, freq_dist_count

base_resources = '{}/tests/resources/'.format(os.getcwd())


class TestTransformOps(unittest.TestCase):

    def test_stop_words(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stopped = stop_words(text)  
            #print(stopped, file=stderr)
            self.assertGreater(len(stopped.split()), 50)
            self.assertNotEqual(text, stopped)

    def test_stop_words_decode_fail(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read()
            self.assertRaises(UnicodeDecodeError, stop_words, text)

    def test_freq_dist(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stopped = stop_words(text)  

            freq_dist = freq_dist_count(stopped.split()) 
            print(pformat(freq_dist), file=stderr)

