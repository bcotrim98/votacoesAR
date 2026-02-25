# Gets the PDF files with the votes, stores them in the "documents" folder and
# retrieves their name to the main module.
# 
# As of today, only retrieveing the names is implemented
# 
# Bruno Cotrim, 25/02/2026

import os

def getPDFName(date):
    # TODO: Get PDFs

    filesFound = os.listdir('documents/')
    fname = [('documents/' + f) for f in filesFound if f.endswith('.pdf')]

    return fname
