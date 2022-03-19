from itertools import count
import PySimpleGUI as psg
import sys
from numpy import result_type
from pymongo import MongoClient
from classifiers_commons import clearTextList
import pandas as pd
from lr import LogisticRegressionClassifier
from svm import SupportVectorMachineClassifier
from nb import NaiveBayesClassifier
from api_secrets import Secrets
import tweepy

# GUI definition
class Window:
    def __init__(self):
        psg.theme('Reddit')

        # Layout
        layout = [
            [psg.Text('Palavra-Chave (Nome, Pessoa, Empresa, Hashtag, Usuário...)', size=(100,0))], 
            [psg.Input(size=(35,0), key='keyword')],
            [psg.Text('Exemplo: #Brasil, @g1, economia...', size=(100,0))], 
            [psg.Text('', size=(100,0))], 
            [psg.Text('Quantidade de tweets a serem buscados:', size=(100,0))], 
            [psg.Slider(range=(1, 100), default_value= 10, orientation='h', size=(15, 20), key='maxTweetCount')],
            [psg.Text('Nota: serão recuperados os N tweets mais recentes sobre a palavra-chave', size=(100,0))], 
            [psg.Text('', size=(100,0))], 
            [psg.Button('Iniciar Análise')],
            [psg.Text('', size=(100,0))], 
            [psg.Text('Resultado:', size=(100,0))], 
            [psg.Output(size=(50, 10), key='output')]
        ]

        # Window
        self.window = psg.Window("Twitter Sentiment Analysis", size=(800, 600)).layout(layout)

    def start(self):
        svm_classifier = SupportVectorMachineClassifier()
        lr_classifier = LogisticRegressionClassifier()
        nb_classifier = NaiveBayesClassifier()

        twitter_api = getTwitterApi()

        while True:
            self.event, self.values = self.window.Read()

            if self.event in (None, 'Exit'):
                sys.exit(1)

            if self.event == 'Iniciar Análise':
                self.window.FindElement('output').update('')

                keyword = self.values['keyword']
                if keyword.replace(' ', '') == '':
                    print('Informe uma palavra-chave válida!')
                    continue
                
                keyword = keyword.strip()
                maxTweetCount = int(self.values['maxTweetCount'])
                print(f'Buscando {maxTweetCount} tweets sobre: \'{keyword}\'')
                
                # Call a function to retrieve the tweets and store into a list
                # tweets_found = ['@pessoaX eu te amo', '@pessoaY eu te odeio', 'livro muito bom #gostei', 'livro excelente https://livro.com', 'jogo muito ruim']
                tweets_found = []
                for tweet in tweepy.Cursor(twitter_api.search_tweets, q=keyword + '-filter:retweets',
                                            count=maxTweetCount,
                                            result_type="recent",
                                            tweet_mode='extended',
                                            lang="pt").items(maxTweetCount):
                    tweets_found.append(tweet.full_text)
                # print(tweets_found)
                # Clean tweets with data preparation steps
                tweets_found = clearTextList(tweets_found)
                # print(tweets_found)
                
                # Perform classification of each list item and store in pos/neg counters
                total_predicted_as_positive = total_predicted_as_negative = 0
                for tweet in tweets_found:
                    predictions = []

                    predictions.append(lr_classifier.classifyText(tweet))
                    predictions.append(svm_classifier.classifyText(tweet))
                    predictions.append(nb_classifier.classifyText(tweet))
                    # print(predictions)

                    # Voting
                    if predictions.count(0) > predictions.count(1):
                        total_predicted_as_negative = total_predicted_as_negative + 1
                    else:
                        total_predicted_as_positive = total_predicted_as_positive + 1

                # Inform how many are classified as pos and how many as neg, with their percentage
                total_predicted = total_predicted_as_negative + total_predicted_as_positive

                print(f"Classificados com sentimento negativo: {total_predicted_as_negative} ({total_predicted_as_negative / total_predicted * 100}%)")
                print(f"Classificados com sentimento positivo: {total_predicted_as_positive} ({total_predicted_as_positive / total_predicted * 100}%)")

def getTwitterApi():
    CONSUMER_KEY=Secrets.CONSUMER_KEY
    CONSUMER_SECRET=Secrets.CONSUMER_SECRET
    ACCESS_TOKEN=Secrets.ACCESS_TOKEN
    ACCESS_TOKEN_SECRET=Secrets.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    if(not api):
        sys.exit("Twitter API authentication failed.")

    return api

window = Window()
window.start()