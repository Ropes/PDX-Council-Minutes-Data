from __future__ import print_function, unicode_literals

import ConfigParser
import os

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.expanduser('~/.config/postgres.ini')))

conf = config.items('luigi')
auth = { c[0]:c[1] for c in conf }

