from classifiers_commons import clearTextList
from ensemblee import returnEnsembleAccuracy
from svm import SupportVectorMachineClassifier
from lr import LogisticRegressionClassifier
from nb import NaiveBayesClassifier
from api_secrets import Secrets
import PySimpleGUI as psg
import tweepy
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window:
    def __init__(self):
        psg.theme('Reddit')

        layout = [
            [psg.Text('Demonstração', font=('Times New Roman', 24))],
            [psg.Text('', font=('Times New Roman', 16))], 
            [psg.Text('Insira o texto:', font=('Times New Roman', 16))],
            [psg.Input(size=(35, 0), key='keyword', font=('Times New Roman', 18))],
            [psg.Text('')], 
            [psg.Button('Analisar', font=('Times New Roman', 16))],
            [psg.Text('')], 
            [psg.Text('Saída:', font=('Times New Roman', 16))], 
            [psg.Output(size=(50, 10), key='output', font=('Times New Roman', 16))]
        ]

        self.window = psg.Window("Twitter Sentiment Analysis", size=(1200, 800), element_justification='center', layout=layout)


    def start(self):
        print('Starting classifiers...')
        svm_classifier = SupportVectorMachineClassifier()
        lr_classifier = LogisticRegressionClassifier()
        nb_classifier = NaiveBayesClassifier()

        print('Connecting to Twitter\'s API...')
        twitter_api = getTwitterApi()

        print('Application started.')
        while True:
            self.event, self.values = self.window.Read()

            if self.event in (None, 'Exit'):
                sys.exit(1)
            
            if self.event == 'Analisar':
                self.window.FindElement('output').update('')

                textToAnalyze = self.values['keyword']
                if textToAnalyze.replace(' ', '') == '':
                    print('Informe um texto válido!')
                    continue
                
                textToAnalyze = textToAnalyze.strip()
                
                textToAnalyzeList = clearTextList([textToAnalyze])

                textToAnalyze = textToAnalyzeList[0]

                result = ""

                predictions = []

                predictions.append(lr_classifier.classifyText(textToAnalyze))
                predictions.append(svm_classifier.classifyText(textToAnalyze))
                predictions.append(nb_classifier.classifyText(textToAnalyze))

                if predictions.count(0) > predictions.count(1):
                    result = "sentimento NEGATIVO"
                else:
                    result = "sentimento POSITIVO"

                print(f"Resultado: " + result)
            
                

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

print('Starting application...')
window = Window()
window.start()