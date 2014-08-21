from __future__ import print_function, unicode_literals

import string
import re
from collections import defaultdict

from PyPDF2 import PdfFileReader
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")
stop = stopwords.words('english')
stop_set = { unicode(w) for w in stop }

def pdf_text(pdf_file):
    pdf = PdfFileReader(pdf_file)

    pages = [ p.extractText() for p in pdf.pages ]
    return '\n'.join(pages)

def remove_punctuation(text, punct=',.?!"\''):
    if type(text) is unicode:
        remove = {ord(c): None for c in punct}
        return text.translate(remove)
    elif type(text) is str:
        return unicode(text.translate(None, str(punct)))
    else:
        raise ValueError, 'Removing punctuation requires type to be str or unicode'

def stop_words(text):
    '''Index positions will be lost in string returned when it is reparsed'''
    return u' '.join([ w for w in text.split() if w.lower() not in stop ])

def stop_word_placeheld(text, placeholder=u''):
    return [ w if w.lower() not in stop_set else placeholder for w in text.split() ]

def token_index(text, split_char=' '):
    '''Create dict of tokens keyed to their list of numeric index locations
    for every occurence in the passed list.
    '''
    index = defaultdict(list)
    for i, t in enumerate(text.split(split_char)):
        index[t].append(i)  
    return dict(index)
        
def freq_dist_count(text):
    fdist = FreqDist(text)
    return [(v, k) for k, v in fdist.items()]

def freq_dist_dict(text):
    fdist = FreqDist(text) 
    return {k:v for k, v in fdist.items()}

#Stemming functionality
def stem_word(text):
    return stemmer.stem(text) 

def stem_text(text):
    return ' '.join([ stem_word(t) for t in text.split() ])

def process_text(text):
    '''Returns list of cleaned tokens'''
    text = remove_punctuation(text)
    return stop_word_placeheld(text)

def split_minutes_content(text):
    '''Split apart the minutes file header info from the conversation'''
    return text.split('\n \n \n')

def split_statements_from_discussion(text):
    '''Break conversations by speaker from the discussion text'''
    return re.findall('([a-zA-Z -]+): (.*?)\s*[a-zA-Z -]+?:', text, re.DOTALL)




