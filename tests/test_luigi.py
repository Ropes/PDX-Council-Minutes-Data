from datetime import datetime
from sys import stderr
import unittest

import luigi 
from luigi.worker import Worker
from luigi import RemoteScheduler

from tasks.extract import (ExtractMinutes, ExtractMinuteYearPage,\
                    ExtractMinuteURLs, )
from tasks.transform import (TransformPDF, CreateTokens, CreateTokenLinks,
        SplitBody, SplitHeader, ParseStatements, DumpStatements)
from tasks.common import task_kick, sch

class TestLuigi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.date = datetime(2011,1,19)

    def test_extract(self):
        task = ExtractMinutes(url='http://efiles.portlandoregon.gov/webdrawer.dll/webdrawer/rec/4187324/view/',\
        date=self.date)

        task_kick(task)

    def test_extract_minutes_wo_url(self):
        dt = datetime(2011, 2, 2)
        task = ExtractMinutes(date=dt)
        task_kick(task)

    def test_year_index(self):
        task = ExtractMinuteYearPage(date=self.date)
        task_kick(task)

    def test_minutes_list(self):
        task = ExtractMinuteURLs(date=self.date) 
        task_kick(task)


    def test_transform(self):
        task = TransformPDF(self.date)
        task_kick(task)

    def test_split_header(self):
        task = SplitHeader(self.date)
        task_kick(task)

    def test_split_body(self):
        task = SplitBody(self.date)
        task_kick(task)

    def test_parse_stmts(self):
        task = ParseStatements(self.date)
        task_kick(task)

    def test_dump_stmts(self):
        task = DumpStatements(self.date)
        task_kick(task)



