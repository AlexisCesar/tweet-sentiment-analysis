from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from pymongo import MongoClient
import pandas as pd
from classifiers_commons import clearTextList

class SupportVectorMachineClassifier:
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
        
        # dataset division
        X_train, self.X_test, y_train, self.y_test = train_test_split(tweetDataFrame.tweet, tweetDataFrame.sentiment, test_size=0.33)

        # TRAINING PHASE: SUPPORT VECTOR MACHINE
        self.vectorizer = TfidfVectorizer(max_features=1000, decode_error="ignore", ngram_range=(1, 2))
        self.vectorizer.fit(X_train)

        # model
        svm_classifier = LinearSVC().fit(self.vectorizer.transform(X_train), y_train)

        self.classifier = svm_classifier
    
    def classifyText(self, text):
        prediction = self.classifier.predict(self.vectorizer.transform([text]))
        return prediction[0]

    def testAndReturnAccuracy(self):
        y_pred = self.classifier.predict(self.vectorizer.transform(self.X_test))
        return accuracy_score(self.y_test, y_pred)

# test = SupportVectorMachineClassifier()
# pred = test.classifyText("ruim")
# print('pred: ' + str(pred))