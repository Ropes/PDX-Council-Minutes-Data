from __future__ import print_function, unicode_literals

import ConfigParser
from os import getenv

import luigi

from . import auth
print(auth.auth)
class LoadText(luigi.Task):
    date = luigi.Parameter()


