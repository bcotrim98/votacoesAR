# 
# 
# 

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
