# Processes a PDF file containing the vote results on the different proposals
# and discussions of the Portuguese Parliament Assembly. Only files from the
# current legislature can be processed, as the format changed with it, so let's
# hope this one fulfills the 4 years
# 
# Voting archieve can be accessed through the Parliament official website:
# https://www.parlamento.pt/ArquivoDocumentacao/Paginas/Arquivodevotacoes.aspx
# 
# Bruno Cotrim, 24/02/2026

import re
import pymupdf
import readInput
import getPropCoords
import proposalClass
import readProp
import readVotes

def getDate(fname):
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', fname)
    voteDate = dates[1] if len(dates) > 1 else None
    voteDate = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', voteDate) # DD-MM-YYYY

    return voteDate

# Apparently, votes order in the tables in not always the same - somtimes 'for'
# comes first, other times 'against' comes first...
# The voting class assumes the order 'for', 'against', 'no vote', 'no show'
def getVoteOrder(page):
    forText = page.search_for('A FAVOR')
    againstText = page.search_for('CONTRA')
    noVoteText = page.search_for('ABSTENÇÃO')

    if not (forText and againstText and noVoteText):
        return None
    
    if not ((len(forText) == len(againstText)) and (len(forText) == len(againstText))):
        return None
    
    foundOrder = [forText[0].y1, againstText[0].y1, noVoteText[0].y1]
    voteOrder = sorted(range(len(foundOrder)), key = lambda i: foundOrder[i])

    return voteOrder

def readFile(pdfFiles):
    input = readInput.getInput('input_files/parties.txt', 'input_files/vote_types.txt',
                                'input_files/col_width.txt')
    
    props = []

    for f in pdfFiles:
        pdfDoc = pymupdf.open(f)
        date = getDate(f)

        voteOrder = None

        for page in pdfDoc:
            voteOrder = getVoteOrder(page)

            if voteOrder:
                break

        for page in pdfDoc:
            coords = getPropCoords.getCoords(page, input['voteTypes'], input['vtTypeState'])
            currProps = readProp.readText(page, coords['propCoords'], len(input['parties']), date)
            currProps = readVotes.getVotes(page, coords['voteCoords'], currProps,
                                        input['parties'], input['nDep'], voteOrder, input['colWidth'])

            props += currProps

        pdfDoc.close()

    return props, input['parties']
