from datetime import datetime
from sys import stderr
import unittest

import luigi 
from luigi.worker import Worker
from luigi import RemoteScheduler

from tasks.transform import TransformPDF 
from tasks.common import task_kick

class TestLuigi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def test_transfrom(self):
        date = datetime(2011,1,12)
        task = TransformPDF(date)
        task_kick(task)

