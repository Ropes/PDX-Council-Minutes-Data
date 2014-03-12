from luigi import Task, Parameter, LocalTarget

from ops.transform import pdx_text

class TransformPDF(Task):
    date = Parameter()

    def requires(self):
        pass 

    def output(self):
        pass

    def run(self):
        with self.input.open('r') as I:
            text = pdx_text(I)
            with self.output.open('w') as O:
                O.write(text)
            

