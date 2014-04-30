from __future__ import print_function, unicode_literals

from datetime import date
import string
from collections import defaultdict

from ops.transform import (stop_word_placeheld, token_index, freq_dist_dict)

from py2neo import neo4j, node, rel, ogm, cypher

def clamp(i, max_num, min_num):
    return max(min(i, max_num), min_num)

def create_link(source, target, index, distance, date=None):
    d = dict()
    d.update({'source': source, 'target': target, 'index': index,\
        'distance': distance})
    if date:
        d.update({'date': date})
    return d

def create_node(token, count):
    return {'token': token, 'count': count}

def find_indexes(index, token_list, dist):
    '''Finds list of indexes from the token_list which spread out the 
    defined distance from the index both forward and behind.
    '''
    target_indexes = range(index-dist, index+dist+1)

    clamped = map(lambda x: min(len(token_list)-1, max(0, x)), target_indexes)
    unique = list(set(clamped))
    unique.remove(index)
    return unique

def link_op(token_list, distance=10,):
    '''Taking the token list as input build all the JSON links to related tokens if not placeholders.

        Params:
        token_list -- iterable list of tokens

        Keyword arguments:
        distance -- Spread of how many tokens should be
            linked to current index.
    '''
    links = []
    for i,t in enumerate(token_list):
        if t != '':
            token_indexes = find_indexes(i, token_list, distance)
            links.extend([ create_link(t, token_list[ti], i, ti-i)  for ti in token_indexes if token_list[ti] != '' ]) 
    return links

def create_nodes(text):
    nodes = {}
    freq_dist = freq_dist_dict(text)
    return freq_dist
        
def token_link_text(text, spread=10):
    '''Combine token frequency and token links together into a single JSON
    format.'''
    text = remove_punctuation(text)
    token_list = stop_word_placeheld(text)

    links = link_op(token_list, distance=spread)

class TokenNode(object):
    def __init__(self, token, count, date=None):
        self.token = token
        self.name = self.token
        self.count = count
        self.date = date

class TokenLink(object):
    def __init__(self, source, target, index, distance):
        self.source = source
        self.target = target
        self.index = index
        self.distance = distance

def neo4j_db(host='localhost', db='data'):
    return neo4j.GraphDatabaseService("http://{host}:7474/db/{db}/"\
                                        .format(host=host, db=db))

def neo4j_store(graph_db):
    return ogm.Store(graph_db)

def neo4j_cypher(host='localhost'):
    return cypher.Session('http://{host}:7474'.format(host=host))

