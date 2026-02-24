# This module contains the functions that obtain the coordinates of the text of
# each proposal and respective votes
# 
# The documents are organised in a consistent way: Proposal type (e.g. general
# vote, deliberation), proposes with votes until a new proposal appears
# 
# For example: General vote -> proposal and vote 1 -> proposal and vote 2 ->
# Deliberation -> proposal and vote 3 -> General vote -> proposal and vote 4
# 
# Every vote has an associated table. This module thus do:
#    1. look for all proposal types
#    2. Discards the ones which aren't to be read
#    3. Gets the coordinates of all tables
#    4. Organises all the coordinates
# 
# Bruno Cotrim, 19/02/2026

import pymupdf

# This function excludes vote types contained in the others. So, if we have
# "Votação" and "Votação geral", we need to exclude the coordinates of "Votação"
# that have already been found in "Votação geral". Note that the vote types are
# already organised such as that "Votação geral" always comes before "Votação"
def excludeContVtType(vtTpCont, coord, foundCoords):
    if not vtTpCont:
        return False
    
    for vID in vtTpCont:
        for fC in foundCoords:
            if vID != (abs(fC[0]) - 1):
                continue

            if (coord > (fC[1] - 1e-6)) and (coord < (fC[2] + 1e-6)):
                return True

    return False

def getPropTypeCoords(page, voteTypes, vtTypeState):
    blockCoords = []
    foundCoords = []

    # Get all vote types coordinates
    for i, (vtTp, vtTpSt) in enumerate(zip(voteTypes, vtTypeState)):
        vtTypeCoords = page.search_for(vtTp)

        for coords in vtTypeCoords:
            if excludeContVtType(vtTpSt[1], coords.y0, foundCoords):
                continue

            if vtTpSt[0]:
                foundCoords.append([i+1, coords.y0, coords.y1])
            else:
                foundCoords.append([-i-1, coords.y0, coords.y1])

    # Get search areas
    foundCoords = sorted(foundCoords, key = lambda x: x[1])
    blockCoords = [] # Apparently it is faster than to pre-allocating?

    for i in range(len(foundCoords)):
        if foundCoords[i][0] < 0:
            continue
        elif i == (len(foundCoords) - 1):
            blockCoords.append([foundCoords[i][0]-1, foundCoords[i][2], page.rect[3]])
            break

        blockCoords.append([foundCoords[i][0]-1, foundCoords[i][2], foundCoords[i+1][1]])

    return blockCoords

# TODO: Older documents are slightly different: Unanimously approved documents
# are not inside boxes, so word search is needed
def getTabCoords(page, blockCoords):
    if not blockCoords:
        return [], []
    
    # So, if someone is away, they are mentioned after the votes when unanimous
    voteTabsCoords = []

    for b in blockCoords:
        rect = pymupdf.Rect(0, b[1], page.rect[2], b[2])
        voteTabs = page.find_tables(clip = rect) # This function works consistently within these documents
        unanimityAway = page.search_for('(Com ausência', clip = rect) # Baldas...
        n = 0
    
        for i, tab in enumerate(voteTabs):
            # Everyone came, taxpayers are happy
            if not unanimityAway:
                voteTabsCoords.append([tab.bbox[1], tab.bbox[3]])
            # The last vote is unanimous and someone did not come: no next table
            elif (i == (len(voteTabs.tables) - 1)):
                voteTabsCoords.append([tab.bbox[1], unanimityAway[n].y1])
            elif (unanimityAway[n].y0 > tab.bbox[3]) and (unanimityAway[n].y0 < voteTabs[i+1].bbox[1]):
                voteTabsCoords.append([tab.bbox[1], unanimityAway[n].y1])
                n += 1

                if n == len(unanimityAway):
                    unanimityAway = []
            else:
                voteTabsCoords.append([tab.bbox[1], tab.bbox[3]])

    blockCoords.extend([[-1, v[0], v[1]] for v in voteTabsCoords])
    blockCoords = sorted(blockCoords, key = lambda x: x[1])

    return blockCoords, voteTabsCoords

def organiseBlocks(blockCoords):
    if not blockCoords:
        return [], []
    
    currType = blockCoords[0][0]

    propTypes = []
    propCoords = []

    for i in range(len(blockCoords) - 1):
        if blockCoords[i+1][0] != -1: # If next is vote type
            continue
        elif blockCoords[i][0] != -1: # If current is vote type
            currType = blockCoords[i][0]
            propCoords.append([blockCoords[i][1], blockCoords[i+1][1]])
        else: # Then next is table
            propCoords.append([blockCoords[i][2], blockCoords[i+1][1]])
        
        propTypes.append(currType)

    return propCoords, propTypes

def getCoords(page, voteTypes, contVoteTypes):
    blockCoords = getPropTypeCoords(page, voteTypes, contVoteTypes)
    blockCoords, voteCoords = getTabCoords(page, blockCoords)
    propCoords, propTypes = organiseBlocks(blockCoords)

    out = {
        'propTypes' : propTypes,
        'propCoords' : propCoords,
        'voteCoords' : voteCoords
    }

    return out
