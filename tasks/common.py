from datetime import datetime
from sys import stderr

import luigi 
from luigi.worker import Worker
from luigi import RemoteScheduler
from luigi.scheduler import CentralPlannerScheduler

HOST = '127.0.0.1'
PORT = 8082

#scheduler = RemoteScheduler(HOST, PORT)
scheduler = CentralPlannerScheduler()

def task_kick(task):
    print(scheduler)
    worker = Worker(scheduler=scheduler)
    print(worker)
    worker.add(task)
    worker.run()


if __name__ == '__main__':
    from tasks.transform import TransformPDF
    d = datetime(2011,1,12)
    t = TransformPDF(d)
    print(t)
    task_kick(t)
    print('wat')


