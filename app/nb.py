from sklearn.model_selection import train_test_split
from pymongo import MongoClient
import pandas as pd
from classifiers_commons import clearTextList
import pickle
from pathlib import Path


class NaiveBayesClassifier:
    def __init__(self):
        self.trainClassifier()
    
    def trainClassifier(self):
        # Verify if is already saved
        prefix = './saves/nb/'
        Path(prefix).mkdir(parents=True, exist_ok=True)
        try:
            self.positive_initial_guess = pickle.load(open(prefix + "pos_initial_guess.pickle", 'rb'))
            self.negative_initial_guess = pickle.load(open(prefix + "neg_initial_guess.pickle", 'rb'))
            self.bag_of_words = pickle.load(open(prefix + "bag_of_words.pickle", 'rb'))
            self.X_test = pickle.load(open(prefix + "X_test.pickle", 'rb'))
            self.y_test = pickle.load(open(prefix + "y_test.pickle", 'rb'))
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

            # dataset division
            X_train, self.X_test, y_train, self.y_test = train_test_split(tweetDataFrame.tweet, tweetDataFrame.sentiment, test_size=0.33)

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
            
            # Save model
            pickle.dump(self.positive_initial_guess, open(prefix + 'pos_initial_guess.pickle', 'wb'))
            pickle.dump(self.negative_initial_guess, open(prefix + 'neg_initial_guess.pickle', 'wb'))
            pickle.dump(self.bag_of_words, open(prefix + 'bag_of_words.pickle', 'wb'))
            pickle.dump(self.X_test, open(prefix + 'X_test.pickle', 'wb'))
            pickle.dump(self.y_test, open(prefix + 'y_test.pickle', 'wb'))

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

    def testAndReturnAccuracy(self):
        WORD = 0
        POSITIVE_TENDENCY = 4
        NEGATIVE_TENDENCY = 5
        
        correct_predictions = 0
        incorrect_predictions = 0

        nb_test_list = []
        for tweet in self.X_test:
            nb_test_list.append([tweet, -1])

        i = 0
        for classification in self.y_test:
            if classification == 1:
                nb_test_list[i][1] = 1
            else:
                nb_test_list[i][1] = 0
            i = i + 1

        for tweet in nb_test_list:
            positive_probability = self.positive_initial_guess
            negative_probability = self.negative_initial_guess

            for word in tweet[0].upper().split():
                for registered_word in self.bag_of_words:
                    if word == registered_word[WORD]:
                        positive_probability = positive_probability * registered_word[POSITIVE_TENDENCY]
                        negative_probability = negative_probability * registered_word[NEGATIVE_TENDENCY]

            naive_bayes_prediction = -1 # There's a problem here, what about when pos/neg hits 0?

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
        
        return naive_bayes_accuracy

# HOW TO USE:
# test = NaiveBayesClassifier()
# pred = test.classifyText("ruim")
# print('pred: ' + str(pred))