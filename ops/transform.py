from __future__ import print_function, unicode_literals

from PyPDF2 import PdfFileReader
from nltk.corpus import stopwords

def pdf_text(pdf_file):
    pdf = PdfFileReader(pdf_file)

    pages = [ p.extractText() for p in pdf.pages ]
    return '\n'.join(pages)

def stop_words(text):
    stop = stopwords.words('english')
    return ' '.join([ w for w in text.split() if w.lower() not in stop ])
