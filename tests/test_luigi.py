from datetime import datetime
from sys import stderr
import unittest

import luigi 
from luigi.worker import Worker
from luigi import RemoteScheduler

from tasks.extract import ExtractMinutes
from tasks.transform import TransformPDF
from tasks.common import task_kick, sch

class TestLuigi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.date = datetime(2011,1,19)

    def test_extract(self):
        task = ExtractMinutes(url='http://efiles.portlandoregon.gov/webdrawer.dll/webdrawer/rec/4187324/view/',\
        date=self.date)

        task_kick(sch, task)


    def test_transform(self):
        task = TransformPDF(self.date)

        task_kick(sch, task)

