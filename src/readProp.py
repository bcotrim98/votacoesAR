# Reads the text associated to which proposal.
# 
# For each proposal's set o coordinates, all the text is extracted. The text is
# then processed, depending on if it's a "regular proposal" or a "special case"
# (requirements, special texts, etc).
# 
# If we have a "regular proposal", the project type, party/organisation
# proposing, the text and its html link in the parliament website are extracted
# 
# If we have a special case, the text and all found html links are extracted
# 
# Note 1 (OUTDATED) - two hyphen types: long dash '–' (separates proposals), and
# normal hyphen '-' (compound words)
# 
# Note 1 - two hyphen types: long dash '–' and normal hyphen '-'. From the
# original note, you can see that I was a hopeful man, but these files are
# apperently written by hand and so typos might happen. Gemini helped improving
# the original Regex expression, now it considers all types of hyphenes
# 
# Note 2 - this document doesn't follow correct Portuguese translineation rules.
# Not only translineation does not happen, as evidenced in some phrases being
# more spaced out than others, but also by the fact that compound words do not
# start with an hyphen after a line break. This is not a rant (maybe a bit),
# it's an important detail
# 
# Bruno Cotrim, 08/02/2026

import pymupdf
import re
import proposalClass

def getType():
    pass

# Removes spaces and line breaks
def cleanText(text):
    text = re.sub(r'^\s*\n\s*', '', text)
    text = re.sub(r'\s*\n\s*$', '', text)
    text = re.sub(r'\-\s*\n\s*', '-', text) # See note 2 on top
    text = re.sub(r'\s*\n\s*', ' ', text)

    return text

def getProp(text, nParties):
    # r'^(Projeto [\w\s]+) n\.º .+ \((\w+)\) - (.+)'
    type = re.search(r'^((?:Projeto|Proposta) .+?) n\.º .+ \((.+?)\) [\-\u2010-\u2015] (.+)', text)

    if not type:
        currProp = proposalClass.Other(text, nParties)
        
        return currProp

    currProp = proposalClass.Proposal(type.group(3), nParties)
    currProp.setType(type.group(1))
    currProp.setParty(type.group(2))

    return currProp

# The links obtained are ordered, at least I am assuming it
def getLinks(links, rect, n):
    propLinks = []
    linkFound = False # If we skip proposals

    for i in range(n, len(links)):
        if rect.intersects(links[i]['from']):
            propLinks.append(links[i])
            linkFound = True

        elif not linkFound:
            continue
        
        else:
            n = i
            return propLinks, n

    return propLinks, n

def getUrlText(page, links):
    propUrl = []

    for currLink in links:
        tempText = page.get_text('text', clip = currLink.get('from'))
        propUrl.append([currLink.get('uri'), tempText.strip()])

    return propUrl

def readText(page, coords, nParties):
    out = []
    links = page.get_links() # There's no clip for links
    n = 0

    for c in coords:
        rect = pymupdf.Rect(0, c[0], page.rect.width, c[1])

        text = page.get_text('text', clip = rect)
        text = cleanText(text)
        currProp = getProp(text, nParties)

        propLink, n = getLinks(links, rect, n)
        propUrl = getUrlText(page, propLink)
        currProp.setLink(propUrl)

        out.append(currProp)

    return out
