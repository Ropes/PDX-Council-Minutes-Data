from __future__ import print_function, unicode_literals

import ConfigParser
from os import getenv

import luigi
from tasks.transform import StopListText
from orm.transform import process_text

from . import auth

class LoadText(luigi.Task):
    date = luigi.Parameter()
    
    def requires(self):
        return StopListText(self.date)

    def output(self):
        pass

    def run(self):
        with self.input().open('r') as I:
            raw_text = I.read()

            tokens_counted = create_tokens(raw_text)

            
            #TODO: Generate token data

            #TODO: Create token_links

            
