from __future__ import unicode_literals, print_function
import datetime
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.extract import (ExtractYearIndex, ExtractMinutesList,\
                         extract_path, extract_fetch, extract_index_from_url)

base_resources = '{}/tests/resources/'.format(os.getcwd())

class TestExtract(unittest.TestCase):

    def test_minutes_of_year(self):
        path = base_resources+'index.cfm?c=56676'
        eyi = ExtractYearIndex()

        with open(path, 'r') as f:
            src = f.read()
            eyi.url=None
            eyi.src = src

            d = eyi.minute_year_index()
            #print(pformat(d), file=stderr)
            self.assertIn(2011, d)
            self.assertIn(1999, d)
            self.assertEqual(d[2006],\
            'http://efiles.portlandoregon.gov/webdrawer/rec/3029951/')


    def test_minutes_list_query(self):
        eml = ExtractMinutesList()
        x = eml.minutes_list_url(4187317)
        print(x)
        self.assertEqual(x, 'http://efiles.portlandoregon.gov/webdrawer.dll/webdrawer/search/rec?sort1=rs_datecreated&rows=100&sm_ncontents=uri_4187317&template=reclist_contents')


    def test_minutes_list_files(self):
        index = 4187317
        eml = ExtractMinutesList()

        path = base_resources+'minutes_list.html'
        with open(path, 'r') as f:
            src = f.read()
            eml.url = None
            x = eml.year_minutes_list(index, src=src)
            #print(pformat(x), file=stderr)
            self.assertGreater(len(x), 10)
            self.assertIn(datetime.datetime(2011, 12, 21, 0, 0), x)


    def test_extract_path(self):
        dt = datetime.datetime(2011, 1, 12)
        path = extract_path(dt)
        #print(path, file=stderr)
        target_out = '{}'.format(os.getcwd())
        self.assertEqual(target_out, path)

    def test_fetch_minutes(self):
        dt = datetime.datetime(2011, 1, 12)
        path = extract_path(dt)
        url = 'http://efiles.portlandoregon.gov/webdrawer.dll/webdrawer/rec/4187324/view/'

        with open('{}neh.pdf'.format(base_resources), 'wb') as f:
            extract_fetch(f, url, dt)

    def test_extract_index_from_url(self):
        x = 'http://efiles.portlandoregon.gov/webdrawer/rec/3029951/'
        index = extract_index_from_url(x)
        self.assertEqual(index, '3029951')



