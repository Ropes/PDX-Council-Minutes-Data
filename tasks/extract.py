from luigi import Task, Parameter, LocalTarget

from ops.extract import (extract_path, extract_fetch)

class ExtractYearsList(Task):
    pass

class ExtractMinutes(Task):
    url = Parameter()
    date = Parameter()

    def require(self):
        pass

    def output(self):
        return LocalTarget(extract_path(self.date))

    def run(self):
        with self.output.open('w') as f_ptr:
            extract_fetch(f_ptr, self.url, self.date)
