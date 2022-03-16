import PySimpleGUI as psg
import sys

# GUI definition
class Window:
    def __init__(self):
        psg.theme('Dark')

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
            [psg.Text('_________________________________', size=(100,0))], 
            [psg.Text('', size=(100,0))], 
            [psg.Text('Resultado:', size=(100,0))], 
            [psg.Output(size=(50, 10), key='output')]
        ]

        # Window
        self.window = psg.Window("Twitter Sentiment Analysis", size=(800, 600)).layout(layout)

    def start(self):
        while True:

            # User input data extraction
            self.event, self.values = self.window.Read()

            if self.event in (None, 'Exit'):
                sys.exit(1)

            if self.event == 'Iniciar Análise':
                keyword = self.values['keyword']
                maxTweetCount = self.values['maxTweetCount']
                print(f'BUSCANDO {maxTweetCount} TWEETS SOBRE: \'{keyword}\'')

window = Window()
window.start()