DATA_DIR = './bbc/'

from sklearn.datasets import load_files
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pandas as pd
import json
from pymongo import MongoClient

# Generating dataset

json_data = None
with open('../../mock/mockTestData.json', encoding='utf-8') as data_file:
    lines = data_file.readlines()
    joined_lines = "[" + ",".join(lines) + "]"

    json_data = json.loads(joined_lines)

# data = pd.DataFrame(json_data)

# MongoDB connection
client = MongoClient('mongodb://root:Database2022@localhost:27018')
db = client['TweetSentimentAnalysis']
negativeTweets = db["NegativeTweets"]
positiveTweets = db["PositiveTweets"]

# Positive Tweets Dataframe
positiveDataframe = positiveTweets.find()
positiveDataframe = pd.DataFrame(positiveDataframe)
positiveDataframe['sentiment'] = 1

# Negative Tweets Dataframe
negativeDataFrame = negativeTweets.find()
negativeDataFrame = pd.DataFrame(negativeDataFrame)
negativeDataFrame['sentiment'] = 0

# Dataframes combination
frames = [positiveDataframe, negativeDataFrame]
tweetDataFrame = pd.concat(frames)


# data prep
X_train, X_test, y_train, y_test = train_test_split(tweetDataFrame.tweet, tweetDataFrame.sentiment)
print(len(X_train))
print(len(X_test))

vectorizer = TfidfVectorizer(max_features=1000, decode_error="ignore")
vectorizer.fit(X_train)

# model
cls = LinearSVC()
cls.fit(vectorizer.transform(X_train), y_train)

y_pred = cls.predict(vectorizer.transform(X_test))

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print('\n' * 4)
input()

while True:
    print('\n' * 100)
    receivedText = str(input("Insert text\n>>>"))
    text_to_analyse = [receivedText]

    predicted = cls.predict(vectorizer.transform(text_to_analyse))

    print("Predicted as: ")
    print(predicted)
    if predicted[0] == 1:
        print("Positive")
    else:
        print("Negative")
    input()