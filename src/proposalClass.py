# Defines the classes of the documents proposed by the various entities
# (parties, government, institutions, etc). It contains the main class, Document
# which the classes Proposal and Other (for requirements, final texts, etc)
# inherit.
# 
# The Document class contains the text, the status and its status
# (approved/rejected). It contains a general function to write the tweets and
# breaks them down if it is over the character limit.
# 
# The Proposal class identifies the entity proposing and the type of proposal
# (law or resolution project)
# 
# The Other class is simpler, as it prints the full non-processed text. It
# extracts all html links from it to provide it in the tweet
# 
# Bruno Cotrim, 07/02/2026

import numpy as np

# TODO: Respect character limit
class Document:
    def __init__(self, text, nParties):
        self._text = text
        
        self._status = 'Rejeitado \U0001F534\n\n' # \u274c
        
        # As parties may sometimes not vote as a block, we need to actually count how many deputees vote for each proposal
        # Line order: for, against, absent, no show
        self._votes = np.zeros((4, nParties), dtype = int)

    def approveProp(self, propStatus):
        self._status = 'Aprovado \U0001F7E2\n\n' # \u2705'
            
    def setLink(self, propURL):
        pass

    def setVotes(self, propVotes):
        self._votes = propVotes

    def addVotes(self, partyID, vote, nVotes):
        self._votes[vote, partyID] += nVotes

    def getCurrTweetLine(self, vtType, parties):
        partiesIn = []

        for i, (p, nV) in enumerate(zip(parties, self._votes[vtType])):
            if nV == 0:
                continue

            currParty = f'{p}'

            # If a party splits votes
            if self._votes[:, i].sum() != nV:
                currParty += f' ({nV})'

            partiesIn.append(currParty)

        currLine = ', '.join(partiesIn)

        return currLine
    
    def writeTweetProp(self):
        pass

    def writeTweetVotes(self, parties):
        tweet = ''

        # Unanimous vote
        if self._votes[1].sum() + self._votes[2].sum() == 0:
            tweet += 'Aprovado com unanimidade \U0001F7E2' # \u2705'

            if self._votes[3].sum() == 0:
                return tweet

            # No shows still count for unanimity, apparently
            tweet += f'\nAusentes: {self.getCurrTweetLine(3, parties)}'

            return tweet

        # Non-unanimous vote
        tweet += self._status

        voteActions = ('Votos a favor', 'Votos contra', 'Abstenção', 'Ausentes')
        partyActions = [''] * 4

        for i, line in enumerate(self._votes):
            if line.sum() == 0:
                continue

            partyActions[i] += self.getCurrTweetLine(i, parties)
            tweet += f'{voteActions[i]}: {partyActions[i]}\n'

        return tweet
    
    def writeTweetWebLink(self):
        pass

class Proposal(Document):
    def __init__(self, text, nParties):
        super().__init__(text, nParties)
        self._type = ''
        self._party = ''
        self._link = '' # web link for the proposal

    def setType(self, propType):
        self._type = propType

    def setParty(self, propParty):
        self._party = propParty

    def setLink(self, propURL):
        self._link = propURL[0][0]

    def writeTweetProp(self):
        return f'{self._type} ({self._party}) – {self._text}\n\n'
    
    def writeTweetWebLink(self):
        return [f'Link para a proposta: {self._link}']

# Requirements, final texts, etc
class Other(Document):
    def __init__(self, text, nParties):
        super().__init__(text, nParties)
        self._link = []

    def setLink(self, propURL):
        self._link = propURL

    def writeTweetProp(self):
        return f'{self._text}\n\n'
    
    def writeTweetWebLink(self):
        tweet = []

        for currLink in self._link:
            tweet.append(f'{currLink[1]}: {currLink[0]}\n')

        return tweet
