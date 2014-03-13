from datetime import datetime
from sys import stderr
import unittest

import luigi 
from luigi.worker import Worker
from luigi import RemoteScheduler

from tasks.extract import ExtractMinutes
from tasks.common import task_kick, sch

class TestLuigi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def test_transfrom(self):
        date = datetime(2011,1,12)
        task = ExtractMinutes(date)
        task_kick(sch, task)

