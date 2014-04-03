from __future__ import print_function, unicode_literals

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

def stop_words(text):
    return ' '.join([ w for w in text.split() if w.lower() not in stop ])

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

