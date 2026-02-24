# Gets the current parties and the dictionary of possible vote types.
# 
# For the vote types, it also gets which ones are of interest and which ones are
# not, so no non-relevant tweets are written.
# 
# It also organises the vote types in a way that strings contained in others
# come later. For example:
#    'general votes', 'votes', 'actual general votes' ->
#    'actual general votes', 'general votes', 'votes'
# 
# Bruno Cotrim, 20/02/2026

from graphlib import TopologicalSorter

# Remember that parties change not only after elections, but also when deputees
# dissociate themselves from the parties, for example, for stealing luggage on
# an airport. Thus, it is important we can change easily change who is
# associated with each party.
# This is also faster than checking the vote tables, as we read page by page
def getParties(inFile):
    parties = []
    nDep = []

    with open(inFile, 'r', encoding = 'utf-8') as f:
        for line in f:
            lineData = line.split(',')
            parties.append(lineData[0].strip())
            nDep.append(int(lineData[1]))

    parties = tuple(parties)
    nDep = tuple(nDep)

    return parties, nDep

# We need to make sure contained strings are searched after the main strings are
# found
def organiseVtTypes(voteTypes, vtTypeState):
    containedStrings = {s: [] for s in voteTypes}
    tempMap = dict(zip(voteTypes, vtTypeState))

    # Find dependencies
    for vtA in voteTypes:
        for vtB in voteTypes:
            if (vtA != vtB) and (vtA in vtB):
                containedStrings[vtA].append(vtB)
        
    # Sort from non-contained to contained
    ts = TopologicalSorter(containedStrings)
    voteTypes = list(ts.static_order())
    vtTypeState = [tempMap[nv] for nv in voteTypes]

    # Check when contained
    for i, vtA in enumerate(voteTypes):
        currContained = []

        for j, vtB in enumerate(voteTypes):
            if (i != j) and (vtA in vtB):
                currContained.append(j)
            
        vtTypeState[i][1] = currContained
        
    return tuple(voteTypes), tuple(vtTypeState)

def getVoteTypes(inFile):
    voteTypes = []
    vtTypeState = []

    with open(inFile, 'r', encoding = 'utf-8') as f:
        for line in f:
            lineData = line.split('-')
            vtTypeState.append([bool(int(lineData[0])), []])
            voteTypes.append(lineData[1].strip())

    voteTypes, vtTypeState = organiseVtTypes(voteTypes, vtTypeState)

    return voteTypes, vtTypeState

# This is to get the column width. It requires the documents to be out after a
# reshuffle of parties, which is, not ideal. This is needed, however, as reading
# tables with PyMuPDF is not working as expected. Let's pray no big scandals
# occur until this gets improved (wishful thinking)
def getColWidth(inFile):
    colWidth = []

    with open(inFile, 'r', encoding = 'utf-8') as f:
        for line in f:
            colWidth.append(float(line))

    return colWidth


def getInput(partiesFile, vtTypesFile, colWidthFile):
    parties, nDep = getParties(partiesFile)
    voteTypes, vtTypeState = getVoteTypes(vtTypesFile)
    colWidth = getColWidth(colWidthFile)

    out = {
        'parties' : parties,
        'nDep' : nDep,
        'voteTypes' : voteTypes,
        'vtTypeState' : vtTypeState,
        'colWidth' : colWidth
    }

    return out
