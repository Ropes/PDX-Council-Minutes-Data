from __future__ import print_function, unicode_literals

import string
from collections import defaultdict

from PyPDF2 import PdfFileReader
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")
stop = stopwords.words('english')

def pdf_text(pdf_file):
    pdf = PdfFileReader(pdf_file)

    pages = [ p.extractText() for p in pdf.pages ]
    return '\n'.join(pages)

def remove_punctuation(text):
    punct = ',:.?!"\''
    if type(text) is unicode:
        remove = {ord(c): None for c in punct}
        return text.translate(remove)
    elif type(text) is str:
        return text.translate(None, str(punct))
    else:
        raise ValueError, 'Removing punctuation requires type to be str or unicode'

def stop_words(text):
    return ' '.join([ w for w in text.split() if w.lower() not in stop ])

def token_index(text, split_char=' '):
    print(text)
    index = defaultdict(list)
    for i, t in enumerate(text.split(split_char)):
        index[t].append(i)  
    return dict(index)
        
def freq_dist_count(text):
    fdist = FreqDist(text) 
    return [ (v, k) for k,v in fdist.iteritems() ]

def freq_dist_dict(text):
    fdist = FreqDist(text) 
    return { k:v for k,v in fdist.iteritems() }


def stem_word(text):
    return stemmer.stem(text) 

def stem_text(text):
    return ' '.join([ stem_word(t) for t in text.split() ])

