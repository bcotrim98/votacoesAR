# 
# 
# 

import argparse
import getpass
from atproto import Client, client_utils
import time
from math import ceil
import readPtARprops

def getLoginInfo():
    descriptText = ('This module posts on BlueSky the proposals that went to ' +
                    'vote in the Portuguese assembly\n\nInput argument:\t ' +
                    'Account username')

    parser = argparse.ArgumentParser(description = descriptText,
                                     epilog = 'Bruno Cotrim, 26/02/2026')
    
    parser.add_argument('username', help = 'Account username')
    args = parser.parse_args()

    args.password = getpass.getpass(prompt = 'Password: ')

    return args

def loginBlueSky(loginInfo):
    client = Client()

    try:
        client.login(loginInfo.username, loginInfo.password)
        return client
    except Exception as e:
        print(f'Login failed: {e}')
        return None

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

    links = prop.getTweetWebLink()

    return tweet, links

def postTweets(tweet, links, client):
    try:
        currTweet = client.send_post(text = tweet[0], langs = ['pt'])
        mainTweetRef = {'uri': currTweet.uri, 'cid': currTweet.cid}
        lastTweetRef = mainTweetRef

        if len(tweet) > 1:
            for t in tweet[1:]:
                time.sleep(2)
                currTweet = client.send_post(
                    text = t,
                    reply_to = {
                        'root' : mainTweetRef,
                        'parent' : lastTweetRef
                    },
                    langs = ['pt']
                )

                lastTweetRef = {'uri': currTweet.uri, 'cid': currTweet.cid}
        
        # We need to build links for them to be clickable and for them to have a
        # preview
        for l in links:
            time.sleep(2)
            tweetText = client_utils.TextBuilder()
            tweetText.text(l[0]).link(l[1], l[1])
            currTweet = client.send_post(
                text = tweetText,
                reply_to = {
                    'root' : mainTweetRef,
                    'parent' : lastTweetRef
                },
                langs = ['pt']
            )

            lastTweetRef = {'uri': currTweet.uri, 'cid': currTweet.cid}

    except Exception as e:
        print(f'Error when posting: {e}\n{tweet[0]}')

if __name__ == '__main__':
    props, parties = readPtARprops.getProps('')
    loginInfo = getLoginInfo()
    client = loginBlueSky(loginInfo)

    if not client:
        exit()

    for p in props:
        tweet, links = getTweet(p, parties, 300)
        postTweets(tweet, links, client)
        time.sleep(10)
