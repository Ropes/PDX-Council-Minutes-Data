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
    pass

def tranverse_tokens(index):
    pass

def find_indexes(index, token_list, dist):

    target_indexes = range(index-dist, index+dist+1)
    target_indexes.remove(index)

    return target_indexes


