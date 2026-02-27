# 
# 
# 

import argparse
from atproto import Client
from math import ceil
import readPtARprops

def getLoginInfo():
    descriptText = ('This module posts on BlueSky the proposals that went to ' +
                    'vote in the Portuguese assembly\n\nInput arguments:\t ' +
                    'Account username\n\tAccount password')

    parser = argparse.ArgumentParser(description = descriptText,
                                     epilog = 'Bruno Cotrim, 26/02/2026')
    
    parser.add_argument('username', help = 'Account username')
    parser.add_argument('password', help = 'Account password')
    
    args = parser.parse_args()

    return args

def getLastSpace(tempString):
    idSpace = tempString.rfind(' ')
    idLBreak = tempString.rfind('\n')

    return max(idSpace, idLBreak)

def breakTweet(tweetText, charLimit):
    currPt = 0
    splitID = [0]
    tweet = []

    while True:
        idSplit = getLastSpace(tweetText[currPt:(currPt + charLimit - 5)])

        if idSplit <= 0:
            break

        splitID.append(currPt + idSplit)
        currPt += idSplit

    if splitID[-1] - splitID[-2] < 50:
        idSplit = getLastSpace(tweetText[:(splitID[-2]-50)])
        splitID[-2] = idSplit
    
    for i in range(len(splitID) - 1):
        tweet.append(f'{i+1}/{len(splitID)-1}. {tweetText[splitID[i]:splitID[i+1]].strip()}')

    return tweet

def getTweet(prop, parties, charLimit):
    tweetText = prop.writeTweetProp()
    tweetVotes = prop.writeTweetVotes(parties)

    if len(tweetText) + len(tweetVotes) < charLimit:
        tweet = [tweetText + tweetVotes]
    elif len(tweetText) < charLimit:
        tweet = [tweetText, tweetVotes]
    else:
        tweet = breakTweet(tweetText, charLimit)
        tweet.append(tweetVotes)

    tweet.extend(prop.writeTweetWebLink())
    
    return tweet

def postTweets(tweet):
    pass

if __name__ == '__main__':
    props, parties = readPtARprops.getProps('')
    loginInfo = getLoginInfo()
    # Log in

    for p in props:
        tweet = getTweet(p, parties, 300)
        postTweets(tweet)
        # wait
