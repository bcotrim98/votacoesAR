# Processes a PDF file containing the vote results on the different proposals
# and discussions of the Portuguese Parliament Assembly. Only files from the
# current legislature can be processed, as the format changed with it, so let's
# hope this one fulfills the 4 years
# 
# Voting archieve can be accessed through the Parliament official website:
# https://www.parlamento.pt/ArquivoDocumentacao/Paginas/Arquivodevotacoes.aspx
# 
# Bruno Cotrim, 24/02/2026

import pymupdf
import readInput
import getPropCoords
import proposalClass
import readProp
import readVotes

def readFile(pdfFName):
    pdfDoc = pymupdf.open(pdfFName)

    props = []

    for page in pdfDoc:
        input = readInput.getInput('parties.txt', 'vote_types.txt', 'col_width.txt')
        coords = getPropCoords.getCoords(page, input['voteTypes'], input['vtTypeState'])

        currProps = readProp.readText(page, coords['propCoords'], len(input['parties']))
        currProps = readVotes.getVotes(page, coords['voteCoords'], currProps,
                                    input['parties'], input['nDep'], input['colWidth'])

        props += currProps

    pdfDoc.close()

    return props
