from sklearn import ensemble
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from pymongo import MongoClient
import pandas as pd
from classifiers_commons import clearTextList
import pickle
from pathlib import Path


def returnEnsembleAccuracy(classifiers):
    # Verify if is already saved
    prefix = './saves/ensemble/'
    Path(prefix).mkdir(parents=True, exist_ok=True)
    try:
        ensemble_accuracy = pickle.load(open(prefix + "accuracy.pickle", 'rb'))
        return ensemble_accuracy
    except (OSError, IOError):
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

        X_train, X_test, y_train, y_test = train_test_split(tweetDataFrame.tweet, tweetDataFrame.sentiment, test_size=0.33)
        
        # Prepare test
        test_list = []
        for tweet in X_test:
            test_list.append([tweet, -1])

        i = 0
        for classification in y_test:
            if classification == 1:
                test_list[i][1] = 1
            else:
                test_list[i][1] = 0
            i = i + 1

        # Classify test
        total_classifications = 0
        correct_classifications = 0

        for tweet in test_list:
            total_classifications = total_classifications + 1

            predictions = []

            for classifier in classifiers:
                predictions.append(classifier.classifyText(tweet[0]))
            
            final_classification = -1

            if predictions.count(0) > predictions.count(1):
                final_classification = 0
            else:
                final_classification = 1
            
            # Compare with the real classification
            if final_classification == tweet[1]:
                correct_classifications = correct_classifications + 1
        
        ensemble_accuracy = correct_classifications / total_classifications

        pickle.dump(ensemble_accuracy, open(prefix + 'accuracy.pickle', 'wb'))
        
        return ensemble_accuracy
