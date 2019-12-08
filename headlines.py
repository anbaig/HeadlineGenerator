import praw
import re
from collections import defaultdict
import random
import os
import tweepy

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                        client_secret=os.environ['CLIENT_SECRET'],
                        password=os.environ['PASSWORD'],
                        user_agent='USERAGENT',
                        username=os.environ['USERNAME'])

startSet = set()
wordMap = defaultdict(list)
endSet = set()

#Initializing data from Reddit
for submission in reddit.subreddit('news').hot(limit=1000):
    line = submission.title
    words = line.split()
    startSet.add(words[0])
    endSet.add(words[len(words)-1])
    for i in range(len(words)-1):
        wordMap[words[i]].append(words[i+1])

#generating a sentence to Tweet based on aggregated data from Reddit
def generateSentence(startSet, wordMap, endSet, sentence, currentWord):
    if(sentence==""):
        sentence = random.sample(startSet, 1)[0]
        return generateSentence(startSet, wordMap, endSet, sentence, sentence)
    else:
        nextWordList= wordMap.get(currentWord)
        randomNextWord = random.sample(nextWordList, 1)[0]
        sentence = sentence + " " + randomNextWord
        if(randomNextWord in endSet):
            return sentence
        return generateSentence(startSet, wordMap, endSet, sentence, randomNextWord)

finalSentence = generateSentence(startSet, wordMap, endSet, "", None)

#Tweet finalSentence
# authentication of consumer key and secret
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])

# authentication of access token and secret
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

# update the status
api.update_status(status =finalSentence)
