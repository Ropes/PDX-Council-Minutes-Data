from __future__ import print_function, unicode_literals

import luigi
from luigi import Task, Parameter, LocalTarget

from ops.transform import pdf_text, stop_words
from ops.extract import extract_path
from tasks.extract import ExtractMinutes

class TransformPDF(Task):
    minutes_date = Parameter(default=None)

    def requires(self):
        return ExtractMinutes(date=self.minutes_date)

    def output(self):
        return LocalTarget('{}/raw.text'.format(\
                                extract_path(self.minutes_date)))

    def run(self):
        with self.input().open('r') as I:
            text = pdf_text(I)
            with self.output().open('w') as O:
                O.write(text.encode('utf-8'))

class StopListText(luigi.Task):
    minutes_date = Parameter(default=None)

    def requires(self):
        return TransformPDF(self.minutes_date)

    def output(self):
        return LocalTarget('{}/cleaned.txt'.format(\
                                extract_path(self.minutes_date)))

    def run(self):
        with self.input().open('r') as I:
            text = stop_words(I.read())
            with self.output().open('w') as O:
                O.write(text.encode('utf-8'))

class YearList(luigi.Task):
    minutes_date = Parameter(default=None)
            
    def requires(self):
        pass

    def output(self):
        pass

    def run(self):
        pass 

if __name__ == '__main__':
    luigi.run()
