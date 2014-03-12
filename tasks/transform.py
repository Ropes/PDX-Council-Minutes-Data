from luigi import Task, Parameter, LocalTarget

from ops.transform import pdx_text
from tasks.extract import ExtractMinutes

class TransformPDF(Task):
    date = Parameter()

    def requires(self):
        return ExtractMinutes(self.date)

    def output(self):
        return LocalTarget('{}/raw.text'.format(\
                                extract_path(self.date)))

    def run(self):
        with self.input.open('r') as I:
            text = pdx_text(I)
            with self.output.open('w') as O:
                O.write(text)
            

