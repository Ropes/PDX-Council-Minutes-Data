from __future__ import unicode_literals

import requests
import lxml
from lxml.etree import HTML
import re
import urlparse

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

class ExtractMinutesList(PDXAuditor):
    base = 'http://efiles.portlandoregon.gov/'
    #'webdrawer/rec/4187317/ '
    path = 'webdrawer.dll/webdrawer/search/rec'
    
    def __init__(self):
        pass

    def minutes_list_url(self, index):
        query = {'rows': ['100'],
            'sm_ncontents': ['uri_{}'.format(index)],
            'sort1': ['rs_datecreated'],
            'template': ['reclist']}

        '''
        sm_ncontents=uri_4187317
        &sort1=rs_datecreated
        &count&template=reclist_contents&rows=150
        '''

        qstr = '&'.join(['{}={}'.format(k,v[0]) for k,v in query.iteritems()])
        return '{}{}?{}'.format(self.base, self.path, qstr)
        
    def year_minutes_list(self, index, src=None):
        query = {'rows': ['50'],
            'sm_ncontents': ['uri_{}'.format(index)],
            'sort1': ['rs_datecreated'],
            'template': ['reclist']}
        path = 'webdrawer.dll/webdrawer/search/rec/'



class ExtractMinutes(object):
    base = 'http://www.portlandonline.com'

    def __init__(self, url=None):
        pass

