 # -*- coding: cp932 -*-
from tkinter import Menu
from pymongo import MongoClient

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
    pass

def printPositiveTweets():
    pass

def printNegativeTweets():
    pass

def processBagOfWords():
    pass

client = MongoClient('mongodb://root:Database2022@localhost:27018')

db = client['TweetSentimentAnalysis']

negativeTweets = db["NegativeTweets"]

foundTweet = negativeTweets.find_one()

# print(foundTweet["tweet"])

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
        break