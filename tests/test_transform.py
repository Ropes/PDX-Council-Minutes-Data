from __future__ import unicode_literals, print_function
import datetime
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.transform import (stop_words, freq_dist_count, stem_text,\
                freq_dist_dict, remove_punctuation)

base_resources = '{}/tests/resources/'.format(os.getcwd())
target_out = '{}/tests/target/'.format(os.getcwd())


class TestTransformOps(unittest.TestCase):
    ick_str = 'adams: wat, badcat. x:cat.'
    good_str = 'adams wat badcat xcat'

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
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(len(freq_dist), 50)

    def test_stemming(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stemmed = stem_text(text)
            #print('Stemmed:\n'+stemmed, file=stderr)
            self.assertGreater(len(stemmed.split()), 50)
            
    
    def test_stop_words_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  
            with open('{}{}'.format(target_out, '2011-1-19stopped'), 'w')\
            as out_file:
                out = ''.join(stopped)
                out_file.write(out.encode('utf8'))
        

    def test_freq_dist_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            assert type(text) == unicode
            stopped = stop_words(text)  
            freq_dist = freq_dist_count(stopped.split()) 
            #print(pformat(freq_dist), file=stderr)
            with open('{}{}'.format(target_out, '2011-1-19freq_dist_count'), 'w')\
            as out_file:
                out_file.write(pformat(freq_dist))


    def test_freq_dist_dict_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  
            freq_dist = freq_dist_dict(stopped.split()) 
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(freq_dist[u'year'], 8)
            self.assertLess(freq_dist[u'year'], 12)

            text = remove_punctuation(text)
            stopped = stop_words(text)  
            freq_dist = freq_dist_dict(stopped.split())
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(freq_dist[u'year'], 16)

            with open('{}{}'.format(target_out, '2011-1-19freq_dist_dict'),\
            
            'w') as out_file:
                out_file.write(pformat(freq_dist))

    def test_punctuation_removal_str(self):
        x = str(self.ick_str)
        out = remove_punctuation(x)
        self.assertEqual(out, self.good_str)
        #print(type(out), file=stderr)

    def test_punctuation_removal_unicode(self):
        x = unicode(self.ick_str)  
        out = remove_punctuation(x)
        self.assertEqual(out, unicode(self.good_str))
        #print(type(out), file=stderr)

