from sklearn import svm
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
from itertools import count
from sys import prefix
from sklearn.datasets import make_classification
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd
import json
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from pymongo import MongoClient
import tweepy
import sys

# MongoDB Connection
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

# TRAINING PHASE: SUPPORT VECTOR MACHINE
vectorizer = TfidfVectorizer(max_features=1000, decode_error="ignore")
vectorizer.fit(X_train)

# model
svm_classifier = LinearSVC().fit(vectorizer.transform(X_train), y_train)

# TRAINING PHASE: LOGISTIC REGRESSION
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(tweetDataFrame['tweet'])

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

logistic_regression_classifier = LogisticRegression().fit(X_train_tfidf, tweetDataFrame['sentiment'])

# TRAINING PHASE: NAIVE BAYES
WORD = 0
POSITIVE_OCCURRENCES = 1
NEGATIVE_OCCURRENCES = 2
TOTAL_OCCURRENCES = 3
POSITIVE_TENDENCY = 4
NEGATIVE_TENDENCY = 5
bag_of_words = list()
SENTIMENT = 1

# Creating the list
training_set = []

for tweet in X_train:
    training_set.append([tweet, ''])

i = 0
for classification in y_train:
    if classification == 1:
        training_set[i][1] = 'positive'
    else:
        training_set[i][1] = 'negative'
    i = i + 1

for text in training_set:

    text_words = text[WORD].split()
    word_was_already_registered = False
    index_of_already_registered_word = -1
    
    for word in text_words:
        for registered_word in bag_of_words:
            if word.upper() == registered_word[WORD]:
                word_was_already_registered = True
                index_of_already_registered_word = bag_of_words.index(registered_word)

        if word_was_already_registered == False:
            if text[SENTIMENT] == 'positive':
                bag_of_words.append([word.upper(), 1, 0, 1, 0, 0])
            else:
                bag_of_words.append([word.upper(), 0, 1, 1, 0, 0])

        else:
            bag_of_words[index_of_already_registered_word][TOTAL_OCCURRENCES] += 1
            
            if text[SENTIMENT] == 'positive':
                bag_of_words[index_of_already_registered_word][POSITIVE_OCCURRENCES] += 1
            else:
                bag_of_words[index_of_already_registered_word][NEGATIVE_OCCURRENCES] += 1

# Calculating the initial guess
positive_count = negative_count = 0
total = len(training_set)

for text in training_set:
    if(text[SENTIMENT] == 'positive'):
        positive_count += 1
    else:
        negative_count += 1

positive_initial_guess = positive_count / total
negative_initial_guess = negative_count / total

# Add the blackbox
for registered_word in bag_of_words:
    registered_word[POSITIVE_OCCURRENCES] += 1
    registered_word[NEGATIVE_OCCURRENCES] += 1
    registered_word[TOTAL_OCCURRENCES] += 1

# Calculating the probability of each word
total_positive_words_registered = total_negative_word_registered = 0
for registered_word in bag_of_words:
    total_positive_words_registered += registered_word[POSITIVE_OCCURRENCES]
    total_negative_word_registered += registered_word[NEGATIVE_OCCURRENCES]

for registered_word in bag_of_words:
    registered_word[POSITIVE_TENDENCY] = registered_word[POSITIVE_OCCURRENCES] / total_positive_words_registered
    registered_word[NEGATIVE_TENDENCY] = registered_word[NEGATIVE_OCCURRENCES] / total_negative_word_registered

# INITIAL SCREEN - SHOWS EACH CLASSIFIER METRICS
print('\n' * 50)
print('ENSEMBLEE CLASSIFIER - SVM - LOGISTIC REGRESSION - NAIVE BAYES')
print('\nPRESS ENTER TO SEE THE METRICS')
input()

print("-" * 50)
print("SVM METRICS:")
y_pred = svm_classifier.predict(vectorizer.transform(X_test))
print("Accuracy score: ", end="")
print(accuracy_score(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print("PRESS ENTER TO CONTINUE...")
input()

print("-" * 50)
print("LOGISTIC REGRESSION METRICS:")
X_new_counts = count_vect.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
y_pred = logistic_regression_classifier.predict(X_new_tfidf)
print("Accuracy score: ", end="")
print(accuracy_score(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print("PRESS ENTER TO CONTINUE...")
input()

print("-" * 50)
print("NAIVE BAYES METRICS:")
# TODO ADD NAIVE BAYES METRICS CALCULATION
correct_predictions = 0
incorrect_predictions = 0

nb_test_list = []
for tweet in X_test:
    nb_test_list.append([tweet, -1])

i = 0
for classification in y_test:
    if classification == 1:
        nb_test_list[i][1] = 1
    else:
        nb_test_list[i][1] = 0
    i = i + 1

for tweet in nb_test_list:
    positive_probability = positive_initial_guess
    negative_probability = negative_initial_guess

    for word in tweet[0].upper().split():
        for registered_word in bag_of_words:
            if word == registered_word[WORD]:
                positive_probability = positive_probability * registered_word[POSITIVE_TENDENCY]
                negative_probability = negative_probability * registered_word[NEGATIVE_TENDENCY]

    naive_bayes_prediction = -1

    if positive_probability > negative_probability:
        naive_bayes_prediction = 1
    elif negative_probability > positive_probability:
        naive_bayes_prediction = 0
    
    if naive_bayes_prediction == tweet[1]:
        correct_predictions = correct_predictions + 1
    else:
        incorrect_predictions = incorrect_predictions + 1

total_predictions = correct_predictions + incorrect_predictions
naive_bayes_accuracy = correct_predictions / total_predictions

print("Accuracy score: ", end="")
print(naive_bayes_accuracy)
print("PRESS ENTER TO CONTINUE...")
input()

while True:
    print('\n' * 50)
    print('Tweet Sentiment Analyzer - Ensemblee')

    # ASKS FOR TEXT INPUT
    text_to_analyse = str(input('\nInsert text to classify\n>>>'))
    text_to_analyse_svm = [text_to_analyse]
    text_to_analyse_lr = [text_to_analyse]
    # INITIALIZE PREDICTION VECTOR
    predictions = []

    # PREDICT PHASE: SUPPORT VECTOR MACHINE
    svm_prediction = svm_classifier.predict(vectorizer.transform(text_to_analyse_svm))

    predictions.append(svm_prediction[0])

    # PREDICT PHASE: LOGISTIC REGRESSION
    X_new_counts = count_vect.transform(text_to_analyse_lr)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    logistic_regression_prediction = logistic_regression_classifier.predict(X_new_tfidf)

    predictions.append(logistic_regression_prediction[0])

    # PREDICT PHASE: NAIVE BAYES
    positive_probability = positive_initial_guess
    negative_probability = negative_initial_guess

    for word in text_to_analyse.upper().split():
        for registered_word in bag_of_words:
            if word == registered_word[WORD]:
                positive_probability = positive_probability * registered_word[POSITIVE_TENDENCY]
                negative_probability = negative_probability * registered_word[NEGATIVE_TENDENCY]

    naive_bayes_prediction = -1

    if positive_probability > negative_probability:
        naive_bayes_prediction = 1
    elif negative_probability > positive_probability:
        naive_bayes_prediction = 0

    predictions.append(naive_bayes_prediction)

    # SHOW EACH CLASSIFIER PREDICTION
    print("SVM: " + str(svm_prediction[0]))
    print("LOGISTIC REGRESSION: " + str(logistic_regression_prediction[0]))
    print("NAIVE BAYES: " + str(naive_bayes_prediction))

    # DECIDE THE FINAL RESULT
    negatives = predictions.count(0)
    positives = predictions.count(1)

    print("FINAL PREDICTION: ", end='')
    if negatives > positives:
        print("NEGATIVE")
    else:
        print("POSITIVE")

    input()