from __future__ import unicode_literals, print_function
import datetime
import json
from pprint import pformat
import os
import six
from sys import stderr
import unittest

from ops.loading import *
from ops.transform import (stop_words, freq_dist_count, stem_text,\
                freq_dist_dict, remove_punctuation, token_index,\
                stop_word_placeheld)

base_resources = '{}/tests/resources/'.format(os.getcwd())
target_out = '{}/tests/target/'.format(os.getcwd())

class TestLoadingOps(unittest.TestCase):
    max_num = 10
    min_num = 0
    small_text = "The quick brown fox jumps over the lazy dog which looks like a fox so we can quickly jump to get repeated words."

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
            text = remove_punctuation(text)
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

    def test_single_index(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            text = remove_punctuation(text)
            stopped = stop_words(text)  

            token_list = stopped.split()
            i = 2
            distance = 5

            token_indexes = find_indexes(i, token_list, distance)
            links = [ create_link(token_list[i], token_list[ti], i, ti-i)  for ti in token_indexes ]
            print(token_list[i])
            print(pformat(links))
            dist_map = { i['distance']: i for i in links }
            self.assertEqual(dist_map[-2]['target'], 'Lebowski')
            self.assertEqual(dist_map[2]['target'], 'hell')
            self.assertEqual(dist_map[3]['source'], 'jesus')



    def test_proto_links(self):
        text = self.small_text #f.read().decode('utf-8')
        text = remove_punctuation(text)
        stopped = stop_words(text)  
        token_list = stopped.split()

        token_list = stop_word_placeheld(text)

        tl = link_op(token_list, distance=3)
        print(token_list)
        print(pformat(tl))
        print(len(token_list))

        foxes = [ f for f in tl if f['source'] == 'fox' ]
        print(pformat(foxes))
        expected_targets = {'quick', 'brown', 'jumps', 'looks', 'like'}
        fox_targets = { f['target'] for f in foxes }
        self.assertEqual(expected_targets, fox_targets)

    def test_create_nodes(self):
        text = self.small_text #f.read().decode('utf-8')
        text = remove_punctuation(text)
        print(text)
        x = create_nodes(text.split())
        print(x)

        self.assertEqual(x['fox'], 2)
        self.assertEqual(x['dog'], 1)


    def test_create_large_nodes(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read()
            text = remove_punctuation(text)
            text = stop_word_placeheld(text)
            nodes = create_nodes(text)
            #print(pformat(nodes))
            self.assertEqual(nodes['parking'],  28)

            links = link_op(text, 3)
            #print(pformat(links))

            json_out = {'nodes': nodes, 'links': links}
            with open('{}/{}'.format(target_out, 'nodes_n_links.json'), 'w')\
                as out_file:
                out_file.write(json.dumps(json_out, indent=4 ))

