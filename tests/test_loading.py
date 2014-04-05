from __future__ import unicode_literals, print_function
import datetime
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.loading import *
from ops.transform import (stop_words, freq_dist_count, stem_text,\
                freq_dist_dict, remove_punctuation, token_index)

base_resources = '{}/tests/resources/'.format(os.getcwd())
target_out = '{}/tests/target/'.format(os.getcwd())

class TestLoadingOps(unittest.TestCase):
    max_num = 10
    min_num = 0

    def test_create_link(self):
        pass


    def test_clamp_max(self):
        i = 11
        self.assertEqual(10, clamp(i, self.max_num, self.min_num))

    def test_clamp_min(self):
        i = -1
        self.assertEqual(0, clamp(i, self.max_num, self.min_num))

    def test_clamp_norm(self):
        i = 5
        self.assertEqual(5, clamp(i, self.max_num, self.min_num))
    

    def test_indexes(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  

            token_list = stopped.split()

            fl = find_indexes(10, token_list, 5)
            print(pformat(fl))
            self.assertEqual(len(fl), 10)


    def test_indexes_low(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  

            token_list = stopped.split()

            index = 2
            fl = find_indexes(index, token_list, 5)
            print(pformat(fl))
            self.assertEqual(token_list[min(fl)], 'Lebowski')
            self.assertNotIn(index, fl)

    def test_indexes_zero(self):
        tl = range(0,10)
        fl = find_indexes(0, tl, 5)

        assumed = set([1, 2, 3, 4, 5])
        print(assumed)
        print(fl)
        self.assertEqual(set(fl), assumed)

    def test_indexes_high(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  

            token_list = stopped.split()

            index = len(token_list)-3
            fl = find_indexes(index, token_list, 5)
            print(token_list)
            print(len(token_list))
            self.assertEqual('eyeball.', token_list[max(fl)])
            self.assertNotIn(index, fl)

    def test_indexes_last(self):
        tl = range(0,10)
        fl = find_indexes(9, tl, 5)
        assumed = {8, 7, 6, 5, 4}

        self.assertEqual(set(fl), assumed)



