from __future__ import print_function, unicode_literals

import ConfigParser
from os import getenv

import luigi

from . import auth

class LoadText(luigi.Task):
    date = luigi.Parameter()
    
    def requires(self):
        pass

    def output(self):
        pass

    def run(self):

