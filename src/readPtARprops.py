# This Python project obtains, processes and publishes on social media (BlueSky,
# in this case) the various votes casted for the different proposals on the
# Portuguese Assembly by the different elected parties and deputees
# 
# Bruno Cotrim, 24/02/2026

import argparse
import datetime
import getFiles
import readPDF
import proposalClass

def getDate(dateString):
    try:
        return datetime.strptime(dateString, '%Y-%m-%d').date()
    except ValueError:
        argparse.ArgumentTypeError('Please provide date as \'YYYY-MM-DD\'')

def getUserInput():
    descriptText = ('This Python project obtains, processes and publishes on ' +
    'social media (BlueSky, in this case) the various votes casted for the ' +
    'different proposals on the Portuguese Assembly by the different elected ' +
    'parties and deputees\n\nInput arguments:\tOutput file name\n\t--dates:\n' +
    '\t\tEmpty argument assumes today\n\t\tOne argument assumes from that day ' +
    'to today\n\t\tTwo arguments assumes from furthest to closest day')

    parser = argparse.ArgumentParser(description = descriptText,
                                     epilog = 'Bruno Cotrim, 24/02/2026')
    
    parser.add_argument('outFile', help = 'Proposals tweets output file name')
    # parser.add_argument('date0

    parser.add_argument('--dates', type = getDate, nargs = '+', help = 
                             'Introduce up to two dates in \'YYYY-MM-DD\' format')
    
    args = parser.parse_args()

    if args.dates:
        if len(args.dates) > 2:
            parser.error('Please include up to two dates')

    return args

def getProps(date):
    fname = getFiles.getPDFName(date)
    props = readPDF.readFile(fname)

    return props

if __name__ == '__main__':
    userInput = getUserInput()
    props = getProps()

    with open(userInput['outFName'], 'w', encoding = 'utf8') as f:
        for p in props:
            f.write('---------------------\n')
            f.write(p.writeTweetProp())
            f.write('\n')
            f.write(p.writeTweetVotes())
            f.write('\n')
            f.write(p.writeTweetWebLink())
            f.write('---------------------\n\n\n')
