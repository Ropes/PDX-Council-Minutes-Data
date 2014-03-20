from __future__ import unicode_literals, print_function

from datetime import datetime
from os import getenv
from sys import stderr

import luigi 

HOST = getenv('LUIGI_IP','127.0.0.1')
PORT = getenv('LUIGI_PORT', 8082)

sch = luigi.RemoteScheduler(HOST, PORT)

def task_kick(task):
    worker = luigi.worker.Worker(scheduler=sch)
    worker.add(task)
    worker.run()

