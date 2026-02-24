# 

import pymupdf
import re
import numpy as np
import proposalClass

# While normally when someone is away, he is away for the whole voting session,
# he can be late/leave earlier. More importantly, this way, we ensure it can
# account for the boycott of certain proposals
def getAway(parties, page, rect):
    text = page.get_text('text', clip = rect)

    # I do not know how it is written when multiple parties are away, as far as
    # I know, it has yet to happen with these documents format. I am assuming it
    # is by ',' and by 'e', the Portuguese word for "and"
    awayParties = re.search(r'\(Com ausência d[a|e|o] (.+?)\)', text)

    if not awayParties:
        return []

    awayParties = awayParties.group(1)
    awayParties = re.split(r',\s*|\s+e\s+', awayParties)
    awayPartiesIndex = [parties.index(p) for p in parties if p in awayParties]
    
    return awayPartiesIndex

def setUnanimousVote(page, prop, parties, nDep, rect):
    prop.approveProp(True) # The idea of a proposal being so bad its own party votes against would be funny, though
    awayPartiesIndex = getAway(parties, page, rect)

    for i, aI in enumerate(awayPartiesIndex):
        prop.addVotes(aI, 3, nDep[i])
        # Should I consider when a single member of a party does not
        # show up? I do not think that has happened yet

def getTableVotes(prop, table, nDep):
    for j, fullCol in enumerate(zip(*table)):
        col = fullCol[2:5]
        vtLine = -1

        for i, line in enumerate(col):
            # This assumes a non-block vote always has a cross
            if line.upper() == 'X':
                prop.addVotes(j, i, nDep[j])
                vtLine = i
                break

        if vtLine == -1:
            prop.addVotes(j, 3, nDep[j])
            continue

        for i, line in enumerate(col):
            if (i != vtLine) and (line):
                prop.addVotes(j, i, int(line))
                prop.addVotes(j, vtLine, -int(line))

def getVotes(page, voteCoords, props, parties, nDep, colWidth):
    colLines = [page.rect[2]*cW for cW in colWidth]

    for p, c in zip(props, voteCoords):
        rect = pymupdf.Rect(0, c[0], page.rect[2], c[1])
        unanimousVote = page.search_for('unanimidade', clip = rect)

        if unanimousVote:
            setUnanimousVote(page, p, parties, nDep, rect)
        else:
            tab = page.find_tables(clip = rect, vertical_strategy = "explicit",
                                   vertical_lines = colLines)
            getTableVotes(p, tab.tables[0].extract(), nDep)
            propStatus = page.search_for('aprovado', clip = rect)

            if propStatus:
                p.approveProp(True)

    return props
