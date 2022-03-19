from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from pymongo import MongoClient
import pandas as pd
from classifiers_commons import clearTextList

class LogisticRegressionClassifier:
    def __init__(self):
        self.trainClassifier()
    
    def trainClassifier(self):
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

        # Data preparation
        tweetDataFrame.tweet = clearTextList(tweetDataFrame.tweet)
       
        # TRAINING PHASE: LOGISTIC REGRESSION
        self.count_vect = CountVectorizer(ngram_range=(1, 2))
        X_train_counts = self.count_vect.fit_transform(tweetDataFrame['tweet'])

        self.tfidf_transformer = TfidfTransformer()
        X_train_tfidf = self.tfidf_transformer.fit_transform(X_train_counts)

        logistic_regression_classifier = LogisticRegression().fit(X_train_tfidf, tweetDataFrame['sentiment'])

        self.classifier = logistic_regression_classifier
        
    def classifyText(self, text):
        X_new_counts = self.count_vect.transform([text])
        X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)

        prediction = self.classifier.predict(X_new_tfidf)
        return prediction[0]

# HOW TO USE:
# test = LogisticRegressionClassifier()
# pred = test.classifyText("muito bom")
# print('pred: ' + str(pred))