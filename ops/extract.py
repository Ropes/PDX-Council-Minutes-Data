from __future__ import unicode_literals, print_function

import requests
import lxml

def get_tree( url):
    resp = requests.get(url)
    return lxml.etree.HTML(resp.text)

class PDXAuditor(object):
    base = 'http://www.portlandonline.com'

class ExtractYearIndex(PDXAuditor):

    def __init__(self, url='/auditor/index.cfm?c=56676'):
        self.url = '{}{}'.format(self.base, url)

    def minute_year_index(self):
        tree = get_tree(self.url)
        links = tree.xpath\
            ("//td[@class='pagecolumnmiddle  ']/table/tr/td/div//a")

        #Extract dict of <year>: <link to directory of minutes>
        return { int(re.findall('([0-9]{4})', a.text)[0]): a.attrib['href']\
                    for a in links if re.findall('([0-9]{4})', a.text) } 


class ExtractMinutesList(object):
    
    def __init__(self, url):
        self.url = url

    def minutes_year_list(self, url):


class ExtractMinutes(object):
    base = 'http://www.portlandonline.com'

    def __init__(self, url=None):
        pass

    def 

    
