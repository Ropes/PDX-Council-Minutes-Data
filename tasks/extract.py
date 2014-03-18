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
    date = luigi.Parameter(default=datetime.now())

    def require(self):
        pass

    def output(self):
        return luigi.LocalTarget('{}/minutes.pdf'.format(\
                                            extract_path(self.date)))

    def run(self):
        with self.output().open('w') as f_ptr:
            extract_fetch(f_ptr, self.url, self.date)

class ExtractMinuteYearPage(luigi.Task):
    date = luigi.Parameter(default=None)
    reset = luigi.Parameter(default=False)

    def require(self):
#TODO: Task to clean out files if reset is set
        pass

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
    date = luigi.Parameter(default=None)
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

