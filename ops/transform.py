from __future__ import print_function, unicode_literal

from PyPDF2 import PdfFileReader

def pdf_text(pdf_file):
    pdf = PdfFileReader(pdf_file)

    pages = [ p.extractText() for p in pdf.pages ]
    return '\n'.join(pages)



