from __future__ import unicode_literals, print_function

from datetime import datetime
from sys import stderr

import luigi 

HOST = '127.0.0.1'
PORT = 8082
sch = luigi.RemoteScheduler(HOST, PORT)

def task_kick(sched, task):
    worker = luigi.worker.Worker(scheduler=sched)
    worker.add(task)
    worker.run()

