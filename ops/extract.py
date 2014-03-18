from __future__ import unicode_literals

import re
import urlparse
from datetime import datetime

import requests
import lxml
from lxml.etree import HTML

from ops.tram import minutes_data


def get_tree(url):
    resp = requests.get(url)
    return HTML(resp.text)

def src_tree(src):
    return HTML(src)

class PDXAuditor(object):

    def fetch_tree(self, url=None, src=None):
        if src:
            return src_tree(src)
        if url:
            return get_tree(self.url)

class ExtractYearIndex(PDXAuditor):
    base = 'http://www.portlandonline.com'

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

def parse_minute_row(a):
    dl_url = a.xpath('td[@class="iframe_reclist_icon_view"]/a')[0]\
                                                    .attrib['href']
    dtstr = a.xpath('td[@style="text-align:right;white-space:nowrap;"]')\
                                                    [0].text.strip()
    date = datetime.strptime(dtstr, '%m/%d/%Y')
    print('{}, {}'.format(date, dl_url))

    return date, dl_url


class ExtractMinutesList(PDXAuditor):
    base = 'http://efiles.portlandoregon.gov/'
    path = 'webdrawer.dll/webdrawer/search/rec'
    
    def __init__(self):
        self.url = None
        self.src = None

    def minutes_list_url(self, index):
        query = {'rows': ['100'],
            'sm_ncontents': ['uri_{}'.format(index)],
            'sort1': ['rs_datecreated'],
            'template': ['reclist_contents']}

        qstr = '&'.join(['{}={}'.format(k,v[0])\
                            for k,v in query.iteritems()])
        return '{}{}?{}'.format(self.base, self.path, qstr)
        
    def year_minutes_list(self, index, src=None):
        self.url = self.minutes_list_url(index)
        tree = self.fetch_tree(url=self.url, src=src)

        links = tree.xpath('/html/body/table//tr')[1:-1]

        minutes = {}
        for a in links:
            k,v = parse_minute_row(a)
            minutes.update({k:v})
        return minutes
            

def extract_index_from_url(url):
    return urlparse.urlparse(url).path.split('/')[-2]    

def extract_path(date):
    return minutes_data(date)

def extract_fetch(f_ptr, url, date):
    resp = requests.get(url)
    path = extract_path(date)

    f_ptr.write(resp.content)

