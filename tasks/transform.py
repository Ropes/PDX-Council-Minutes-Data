from __future__ import print_function, unicode_literals

import luigi
from luigi import Task, Parameter, LocalTarget

from ops.transform import pdf_text
from ops.extract import extract_path
from tasks.extract import ExtractMinutes

class TransformPDF(Task):
    minutes_date = Parameter(default=None)

    def requires(self):
        return ExtractMinutes(self.minutes_date)

    def output(self):
        return LocalTarget('{}/raw.text'.format(\
                                extract_path(self.minutes_date)))

    def run(self):
        with self.input.open('r') as I:
            text = pdx_text(I)
            with self.output.open('w') as O:
                O.write(text)
            
if __name__ == '__main__':
    luigi.run()
