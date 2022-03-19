from sklearn.model_selection import train_test_split
from pymongo import MongoClient
import pandas as pd
from classifiers_commons import clearTextList


class NaiveBayesClassifier:
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
        X_train, X_test, y_train, y_test = train_test_split(tweetDataFrame.tweet, tweetDataFrame.sentiment, test_size=0.33)

        # TRAINING PHASE: NAIVE BAYES
        WORD = 0
        POSITIVE_OCCURRENCES = 1
        NEGATIVE_OCCURRENCES = 2
        TOTAL_OCCURRENCES = 3
        POSITIVE_TENDENCY = 4
        NEGATIVE_TENDENCY = 5
        self.bag_of_words = list()
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

            text_words = text[WORD].split(" ")
            word_was_already_registered = False
            index_of_already_registered_word = -1
            
            for word in text_words:
                for registered_word in self.bag_of_words:
                    if word.upper() == registered_word[WORD]:
                        word_was_already_registered = True
                        index_of_already_registered_word = self.bag_of_words.index(registered_word)

                if word_was_already_registered == False:
                    if text[SENTIMENT] == 'positive':
                        self.bag_of_words.append([word.upper(), 1, 0, 1, 0, 0])
                    else:
                        self.bag_of_words.append([word.upper(), 0, 1, 1, 0, 0])

                else:
                    self.bag_of_words[index_of_already_registered_word][TOTAL_OCCURRENCES] += 1
                    
                    if text[SENTIMENT] == 'positive':
                        self.bag_of_words[index_of_already_registered_word][POSITIVE_OCCURRENCES] += 1
                    else:
                        self.bag_of_words[index_of_already_registered_word][NEGATIVE_OCCURRENCES] += 1

        # Calculating the initial guess
        positive_count = negative_count = 0
        total = len(training_set)

        for text in training_set:
            if(text[SENTIMENT] == 'positive'):
                positive_count += 1
            else:
                negative_count += 1

        self.positive_initial_guess = positive_count / total
        self.negative_initial_guess = negative_count / total

        # Add the blackbox
        for registered_word in self.bag_of_words:
            registered_word[POSITIVE_OCCURRENCES] += 1
            registered_word[NEGATIVE_OCCURRENCES] += 1
            registered_word[TOTAL_OCCURRENCES] += 1

        # Calculating the probability of each word
        total_positive_words_registered = total_negative_word_registered = 0
        for registered_word in self.bag_of_words:
            total_positive_words_registered += registered_word[POSITIVE_OCCURRENCES]
            total_negative_word_registered += registered_word[NEGATIVE_OCCURRENCES]

        for registered_word in self.bag_of_words:
            registered_word[POSITIVE_TENDENCY] = registered_word[POSITIVE_OCCURRENCES] / total_positive_words_registered
            registered_word[NEGATIVE_TENDENCY] = registered_word[NEGATIVE_OCCURRENCES] / total_negative_word_registered

    def classifyText(self, text):
        WORD = 0
        POSITIVE_TENDENCY = 4
        NEGATIVE_TENDENCY = 5

        # PREDICT PHASE: NAIVE BAYES
        positive_probability = self.positive_initial_guess
        negative_probability = self.negative_initial_guess

        for word in text.upper().split():
            for registered_word in self.bag_of_words:
                if word == registered_word[WORD]:
                    positive_probability = positive_probability * registered_word[POSITIVE_TENDENCY]
                    negative_probability = negative_probability * registered_word[NEGATIVE_TENDENCY]

        naive_bayes_prediction = -1 # There's a problem here, what about when pos/neg hits 0?

        if positive_probability > negative_probability:
            naive_bayes_prediction = 1
        elif negative_probability > positive_probability:
            naive_bayes_prediction = 0
        return naive_bayes_prediction

# HOW TO USE:
# test = NaiveBayesClassifier()
# pred = test.classifyText("ruim")
# print('pred: ' + str(pred))