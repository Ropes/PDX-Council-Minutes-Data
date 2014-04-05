from __future__ import print_function, unicode_literals

from datetime import date
import string
from collections import defaultdict

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
    target_indexes.remove(index)

    clamped = map(lambda x: min(len(token_list)-1, max(0, x)), target_indexes)

    return list(set(clamped))


