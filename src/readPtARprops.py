# This Python project obtains, processes and publishes on social media (BlueSky,
# in this case) the various votes casted for the different proposals on the
# Portuguese Assembly by the different elected parties and deputees
# 
# Bruno Cotrim, 24/02/2026

import readPDF
import getFiles
import proposalClass

def getProps(date):
    fname = getFiles.getPDFName(date)
    props = readPDF.readFile(fname)

    return props

if __name__ == '__main__':
    props = getProps()

    with open(outFile, 'w', encoding = 'utf8') as f:
        for p in props:

