from __future__ import print_function, unicode_literals

from datetime import date
import string
from collections import defaultdict

from ops.transform import (stop_word_placeheld, token_index, 
        freq_dist_dict, remove_punctuation)
from orm.tables import Token, Tokenlink

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

class TokenNode(object):
    token = ''
    date = ''
    count = 0
    indexes = []
    pass

class TokenLink(object):
    source = ''
    date = ''
    target = ''
    distance = 0
    

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

def create_tokens(text):
    text = remove_punctuation(text)
    text = stop_word_placeheld(text)
    return create_nodes(text)
        
def load_tokens_to_db(session, tokens, meeting_date):
    '''Create list of tokens from processed text and meeting date
    then insert into Tokens table via the session object.
    Args
    session: SQLA Session object
    tokens: FrequencyDist eict of tokens(keys) and their doc count(value)
    meeting_date: MeetingDate orm object queried from DB

    Returns: Nothing 
    '''
    for k,v in tokens.items():
        if k:
            t = Token(token=k, count=v)
            t.MeetingDate = meeting_date
            session.add(t) 
    session.commit()

def create_links(processed_text, link_dist=25):
    return link_op(processed_text, link_dist) 

def load_token_links_to_db(session, links, meeting_date):
    '''Create Token Links within document and store data within database
    via ORM Tokenlink objects to the TokenLinks table.

    Args
    session: SQLA Session object
    links: List of link dicts containing: distance, index, source,and target
    Return: Nothing
    '''
    for l in links:
        source = session.query(Token)\
                .filter(Token.token==l['source']).all()[0]
        target = session.query(Token)\
                .filter(Token.token==l['target']).all()[0]

        tl = Tokenlink(distance=l['distance'], index=l['index'])
        tl.Token = source
        tl.Token1 = target
        tl.MeetingDate = meeting_date
        session.add(tl)

    session.commit()

