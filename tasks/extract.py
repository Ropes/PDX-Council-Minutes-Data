from __future__ import print_function, unicode_literals
from datetime import datetime

import luigi

from ops.extract import (extract_path, extract_fetch)

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

if __name__ == '__main__':
    luigi.run()

