import PySimpleGUI as psg
import sys

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
        # May the classifiers' training phase goes here

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

                # Perform classification of each list item and store in pos/neg counters

                # Inform how many are classified as pos and how many as neg, with their percentage

window = Window()
window.start()