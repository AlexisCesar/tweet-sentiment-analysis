from classifiers_commons import clearTextList
from svm import SupportVectorMachineClassifier
from lr import LogisticRegressionClassifier
from nb import NaiveBayesClassifier
from api_secrets import Secrets
import PySimpleGUI as psg
import tweepy
import sys

class Window:
    def __init__(self):
        psg.theme('Reddit')

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
                
                tweets_found = []
                for tweet in tweepy.Cursor(twitter_api.search_tweets, q=keyword + '-filter:retweets',
                                            count=maxTweetCount,
                                            result_type="recent",
                                            tweet_mode='extended',
                                            lang="pt").items(maxTweetCount):
                    tweets_found.append(tweet.full_text)

                tweets_found = clearTextList(tweets_found)
                
                total_predicted_as_positive = total_predicted_as_negative = 0
                for tweet in tweets_found:
                    predictions = []

                    predictions.append(lr_classifier.classifyText(tweet))
                    predictions.append(svm_classifier.classifyText(tweet))
                    predictions.append(nb_classifier.classifyText(tweet))

                    if predictions.count(0) > predictions.count(1):
                        total_predicted_as_negative = total_predicted_as_negative + 1
                    else:
                        total_predicted_as_positive = total_predicted_as_positive + 1

                total_predicted = total_predicted_as_negative + total_predicted_as_positive

                print(f"Classificados com sentimento negativo: {total_predicted_as_negative} ({(total_predicted_as_negative / total_predicted * 100):.2f}%)")
                print(f"Classificados com sentimento positivo: {total_predicted_as_positive} ({(total_predicted_as_positive / total_predicted * 100):.2f}%)")

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