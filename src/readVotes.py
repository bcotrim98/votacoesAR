# Obtains the votes casted by each party for each proposal. Votes can be
# unanimous or split.
# 
# If unanimous, the document showcases a "approved unanimously" ("Aprovado por
# unanimidade"). In case of split votes, a party can vote for or against, or
# abstain. The document displays a table with the votes, where each line
# contains the vote (for, against, or no vote) and each column the parties. A
# cross shows the vote intention. If a party splits its votes, the cross is
# maintained, with the number of "dissidents" written on its respective line.
# 
# Aditionally, deputees can fail to show up. In that case, unanimous votes can
# still happen, with their no show referenced after the vote aftermath. If votes
# are split, their column is empty
# 
# Bruno Cotrim, 24/02/2026

import pymupdf
import re
import numpy as np
import proposalClass

# When someone is away, he is usually away for the whole session. This means it
# is much faster to check that at the beginining of the document and never check
# ever again. However, not only he can be late/leave earlier, but this way we 
# also ensure certain proposals boycotts are accounted for. And we all need know
# that controversies generate popular tweets
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

def getTableVotes(prop, table, nDep, currOrder):
    for j, fullCol in enumerate(zip(*table)):
        col = fullCol[2:5]
        vtLine = -1

        for i, line in enumerate(col):
            # This assumes a non-block vote always has a cross
            # The check is also relaxed because 'XX' has been found
            if 'X' in line.upper():
                prop.addVotes(j, currOrder[i], nDep[j])
                vtLine = i
                break

        if vtLine == -1:
            prop.addVotes(j, 3, nDep[j])
            continue

        for i, line in enumerate(col):
            if (i != vtLine) and (line):
                prop.addVotes(j, i, int(line))
                prop.addVotes(j, vtLine, -int(line))

def getVotes(page, voteCoords, props, parties, nDep, currOrder, colWidth):
    colLines = [page.rect[2]*cW for cW in colWidth]

    for p, c in zip(props, voteCoords):
        rect = pymupdf.Rect(0, c[0], page.rect[2], c[1])
        unanimousVote = page.search_for('unanimidade', clip = rect)

        if unanimousVote:
            setUnanimousVote(page, p, parties, nDep, rect)
        else:
            tab = page.find_tables(clip = rect, vertical_strategy = "explicit",
                                   vertical_lines = colLines)
            getTableVotes(p, tab.tables[0].extract(), nDep, currOrder)
            propStatus = page.search_for('aprovado', clip = rect)

            if propStatus:
                p.approveProp(True)

    return props
