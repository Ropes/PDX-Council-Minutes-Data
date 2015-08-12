from __future__ import unicode_literals, print_function

from datetime import datetime
import re
from sys import stderr
import urlparse

import lxml
from lxml.etree import HTML
import requests

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

def parse_minute_row(row):
    try:
        dl_url = row.xpath('//a[@title="Download File"]')[0].attrib['href']
        dtstr = row.xpath('./td[5]')[0].text.strip()
        date = datetime.strptime(dtstr, '%m/%d/%Y')
    except Exception as err:
        print("Error Parsing Document Row {}".format(err))
        date = None
        dl_url = None

    return date, dl_url


class ExtractMinutesList(PDXAuditor):
    #'http://efiles.portlandoregon.gov/Record?q=recContainer%3A3029951&nb=true&pageSize=500'
    base = 'http://efiles.portlandoregon.gov/'
    path = 'Record'
    
    def __init__(self):
        self.url = None
        self.src = None

    def minutes_list_url(self, index):
        query = {'pageSize': ['500'],
            'q': ["recContainer%3A{}".format(index)],
            'nb': ["true"]}

        qstr = '&'.join(['{}={}'.format(k,v[0])\
                            for k,v in query.iteritems()])
        return '{}{}?{}'.format(self.base, self.path, qstr)
        
    def year_minutes_list(self, index, src=None):
        self.url = self.minutes_list_url(index)
        tree = self.fetch_tree(url=self.url, src=src)
        links = tree.xpath('/html/body/table/tbody/*')
        #print("links: {}".format(links), file=stderr)

        minutes = {}
        #[ print(l.xpath("string()"),file=stderr) for l in links ]
          
        links = links[1:]
        for a in links:
            #print(a, file=stderr)
            k,v = parse_minute_row(a)
            minutes.update({k:v})
        return minutes
            

def extract_index_from_url(url):
    return urlparse.urlparse(url).path.split('/')[-2]    

def extract_path(date):
    return minutes_data(date)

def extract_fetch(f_ptr, url, date):
    #print(url, file=stderr)
    resp = requests.get(url)
    path = extract_path(date)

    f_ptr.write(resp.content)

