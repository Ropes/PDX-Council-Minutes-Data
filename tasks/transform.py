from __future__ import print_function, unicode_literals

import pickle
import luigi
from luigi import Task, Parameter, LocalTarget

from ops.loading import create_tokens, token_link_text
from ops.transform import pdf_text, split_minutes_content, stop_word_placeheld
from ops.extract import extract_path
from tasks.extract import ExtractMinutes

class TransformPDF(Task):
    date = Parameter(default=None)

    def requires(self):
        return ExtractMinutes(date=self.date)

    def output(self):
        return LocalTarget('{}/raw.text'.format(\
                                extract_path(self.date)))

    def run(self):
        with self.input().open('r') as I:
            text = pdf_text(I)
            with self.output().open('w') as O:
                O.write(text.encode('utf-8'))

class SplitHeader(luigi.Task):
    date = Parameter(default=None)

    def requires(self):
        return TransformPDF(self.date)

    def output(self):
        return LocalTarget("{}/header.txt".format(extract_path(self.date)))

    def run(self):
        with self.input().open("r") as I:
            text = I.read()
            text = text.decode('utf8')
            text = ''.join(text)

            split_doc = split_minutes_content(text)
            with self.output().open("w") as O:
                O.write(split_doc[0].encode("utf8"))
            
class SplitBody(luigi.Task):
    date = Parameter(default=None)

    def requires(self):
        return TransformPDF(self.date)

    def output(self):
        return LocalTarget("{}/body.txt".format(extract_path(self.date)))

    def run(self):
        with self.input().open("r") as I:
            text = I.read()
            text = text.decode('utf8')
            text = ''.join(text)


            split_doc = split_minutes_content(text)
            trans_table = dict.fromkeys(map(ord, u"\n"), None)
            sp_text = split_doc[1].translate(trans_table)

            with self.output().open("w") as O:
                O.write(sp_text.encode('utf8'))

class ParseStatements(luigi.Task):
    date = Parameter(default=None)

    def requires(self):
        pass

    def output(self):
        pass

    def run(self):
        pass

class StopListText(luigi.Task):
    date = Parameter(default=None)

    def requires(self):
        return TransformPDF(self.date)

    def output(self):
        return LocalTarget('{}/cleaned.txt'.format(\
                                extract_path(self.date)))

    def run(self):
        with self.input().open('r') as I:
            src = I.read()
            print('Src type: {}'.format(type(src)))
            tokens = stop_word_placeheld(src)
            with self.output().open('w') as O:
                pickle.dump(tokens, O)


class CreateTokens(luigi.Task):
    date = luigi.Parameter()
    
    def requires(self):
        return StopListText(self.date)

    def output(self):
        return LocalTarget('{}/tokens.pkl'.format(\
                            extract_path(self.date)))

    def run(self):
        with self.input().open('r') as I:
            raw_text = I.read()

            tokens_counted = create_tokens(raw_text)
            with self.output().open('w') as O:
                pickle.dump(tokens_counted, O)
                

class CreateTokenLinks(luigi.Task):
    date = luigi.Parameter()

    def requires(self):
        return StopListText(self.date)

    def output(self):
        return LocalTarget('{}/token_links.pkl'.format(\
                        extract_path(self.date)))

    def run(self):
        with self.input().open('r') as I:
            raw_text = I.read()
            links = token_link_text(raw_text, distance=25)
            with self.output().open('w') as O:
                pickle.dump(links, O)


class YearList(luigi.Task):
    date = Parameter(default=None)
            
    def requires(self):
        pass

    def output(self):
        pass

    def run(self):
        pass 

if __name__ == '__main__':
    luigi.run()
