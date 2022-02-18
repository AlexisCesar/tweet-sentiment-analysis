from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


stop_words = set(stopwords.words('portuguese'))
 
word_tokens = word_tokenize("#Brasil @Alexis Essa é uma mensagem de exemplo e deverá ser substituida pelos tweets coletados. Programas programa programador programado programando")

filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

print(filtered_sentence)


# For loop through stored tweets in database

    # Tweet text tokenization

    # Stopwords removal

    # Stemming proccess

