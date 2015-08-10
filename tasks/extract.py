from __future__ import print_function, unicode_literals
from datetime import datetime
from sys import stderr
from pprint import pformat
import pickle

import luigi


from ops.tram import build_path, home
from ops.extract import (extract_path, extract_fetch,ExtractYearIndex,
                            ExtractMinutesList, extract_index_from_url)

class ExtractMinutes(luigi.Task):
    url = luigi.Parameter(default=None)
    date = luigi.DateIntervalParameter(default=datetime.now())
    base_url = luigi.Parameter(default='http://efiles.portlandoregon.gov')
   
    def requires(self):
        if self.url is None:
            return ExtractMinuteURLs(date=self.date)

    def output(self):
        return luigi.LocalTarget('{}/minutes.pdf'.format(\
                                            extract_path(self.date)))

    def run(self):
        if not self.url is None:
            with self.output().open('w') as f_ptr:
                extract_fetch(f_ptr, self.url, self.date)
        else:
            with self.input().open('r') as I:
                minutes_index = pickle.load(I) 
                url = minutes_index[self.date]
                url = '{}{}'.format(self.base_url, url)
                with self.output().open('w') as O:
                    extract_fetch(O, url, self.date)
                 

class ExtractMinuteYearPage(luigi.Task):
    '''Get list of years which can be queried searched for minutes data'''
    date = luigi.DateIntervalParameter(default=None)
    reset = luigi.Parameter(default=False)

    def output(self):
        dpl = ['data']
        path = build_path(dpl, prefix_path=home)
        return luigi.LocalTarget('{}/year_urls.pkl'.format(path))

    def run(self):
        eyi = ExtractYearIndex()
        minute_year_index = eyi.minute_year_index()
        with self.output().open('w') as O:
            pickle.dump(minute_year_index, O)
            

class ExtractMinuteURLs(luigi.Task):
    '''Get URLs for all of the minutes files available for defined year'''
    date = luigi.DateIntervalParameter(default=None)
    reset = luigi.Parameter(default=False)

    def requires(self):
        return ExtractMinuteYearPage(date=self.date)

    def output(self):
        dpl = ['data', unicode(self.date.year)]
        path = build_path(dpl, prefix_path=home)
        return luigi.LocalTarget('{}/date_urls.pkl'.format(path))

    def run(self):
        eml = ExtractMinutesList() 
        with self.input().open('r') as I:
            minute_year_index = pickle.load(I)

            index = extract_index_from_url(minute_year_index[self.date.year])

            minutes_url_map = eml.year_minutes_list(index)
            with self.output().open('w') as O:
                pickle.dump(minutes_url_map, O)


if __name__ == '__main__':
    luigi.run()

