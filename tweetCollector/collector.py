 # -*- coding: cp932 -*-
from pymongo import MongoClient
from api_secrets import Secrets
import tweepy
import sys

# MongoDB connection
client = MongoClient('mongodb://root:Database2022@localhost:27018')
db = client['TweetSentimentAnalysis']
negativeTweets = db["NegativeTweets"]
positiveTweets = db["PositiveTweets"]

# Twitter API connection
CONSUMER_KEY=Secrets.CONSUMER_KEY
CONSUMER_SECRET=Secrets.CONSUMER_SECRET
ACCESS_TOKEN=Secrets.ACCESS_TOKEN
ACCESS_TOKEN_SECRET=Secrets.ACCESS_TOKEN_SECRET

auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

if(not api):
    print("- TWITTER AUTH FAILED -")
    sys.exit(-1)

def mainMenu():
    menuSize = 50
    print('\n' * 100)
    print('-' * menuSize)
    print('TWEET COLLECTOR')
    print('-' * menuSize)
    print('CHOOSE OPTION:')
    print('[1] - COLLECT TWEETS')
    print('[2] - SHOW POSITIVE TWEETS IN DATABASE')
    print('[3] - SHOW NEGATIVE TWEETS IN DATABASE')
    print('[4] - PROCESS BAG OF WORDS')
    print('[5] - EXIT')
    print('-' * menuSize)
    option = int(input('>>> '))
    return option

def collectTweets():
    while True:
        # Ask for a keyword
        print('\n' * 100)
        print('Enter a keyword:')
        keyword = input('>>> ')

        # Show the tweet
        print('\n' * 100)
        collectedTweet = findTweetBasedOnKeyword(keyword)
        print('Collected tweet:\n')
        print(collectedTweet)
        print('\n\n')

        # Ask for classification (positive/negative)
        print('[1] - Classify as POSITIVE')
        print('[2] - Classify as NEGATIVE')
        print('[3] - Skip this tweet')
        option = int(input('>>> '))

        print('\n' * 100)
        if option != 3:
            # Store into the database
            if option == 1:
                print('Storing tweet in POSITIVE collection...')
                tweetToSave = {
                    "tweet": collectedTweet
                }
                dbResponse = positiveTweets.insert_one(tweetToSave)
                print('Tweet stored with id: ')
                print(dbResponse.inserted_id)
            elif option == 2:
                print('Storing tweet in NEGATIVE collection...')
                tweetToSave = {
                    "tweet": collectedTweet
                }
                dbResponse = negativeTweets.insert_one(tweetToSave)
                print('Tweet stored with id: ')
                print(dbResponse.inserted_id)
        else:
            print('Tweet skipped')
        print('\n')

        # Ask if continue or stops
        print('Continue collecting tweets?')
        print('[1] - Yes')
        print('[2] - No')
        option = int(input('>>> '))

        if option == 2:
            break

def findTweetBasedOnKeyword(keyword):
    tweets = api.search_tweets(q=keyword + ' -filter:retweets', lang="pt", count=1, result_type="recent", tweet_mode='extended')
    return tweets[0].full_text

def printPositiveTweets():
    tweets = positiveTweets.find()
    for tweet in tweets:
        print('TWEET - ' + tweet['tweet'] + '\n')
    input('\n\npress enter to continue...')

def printNegativeTweets():
    tweets = negativeTweets.find()
    for tweet in tweets:
        print('TWEET - ' + tweet['tweet'] + '\n')
    input('\n\npress enter to continue...')

def processBagOfWords():
    pass

while True:
    option = mainMenu()
    if option == 1:
        collectTweets()
    elif option == 2:
        printPositiveTweets()
    elif option == 3:
        printNegativeTweets()
    elif option == 4:
        processBagOfWords()
    elif option == 5:
        sys.exit(-1)