from __future__ import unicode_literals

import requests
import lxml
from lxml.etree import HTML
import re

def get_tree(url):
    resp = requests.get(url)
    return HTML(resp.text)

def src_tree(src):
    return HTML(src)

class PDXAuditor(object):
    base = 'http://www.portlandonline.com'

    def fetch_tree(self, url=None, src=None):
        if src:
            return src_tree(src)
        if url:
            return get_tree(self.url)

class ExtractYearIndex(PDXAuditor):

    def __init__(self, url='/auditor/index.cfm?c=56676'):
        self.url = '{}{}'.format(self.base, url)
        self.src = None

    def minute_year_index(self):
        tree = self.fetch_tree(url=self.url, src=self.src)
        links = tree.xpath\
            ("//td[@class='pagecolumnmiddle  ']/table/tr/td/div//a")

        #Extract dict of <year>: <link to directory of minutes>
        return { int(re.findall('([0-9]{4})', a.text)[0]): a.attrib['href']\
                    for a in links if re.findall('([0-9]{4})', a.text) } 

class ExtractMinutesList(object):
    
    def __init__(self, url):
        self.url = url

    def minutes_year_list(self, url):
        pass


class ExtractMinutes(object):
    base = 'http://www.portlandonline.com'

    def __init__(self, url=None):
        pass

