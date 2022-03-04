from itertools import count
from sys import prefix
from sklearn.datasets import make_classification
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import pandas as pd
import json
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2

# Generating dataset

json_data = None
with open('../../mock/mockTestData.json', encoding='utf-8') as data_file:
    lines = data_file.readlines()
    joined_lines = "[" + ",".join(lines) + "]"

    json_data = json.loads(joined_lines)

data = pd.DataFrame(json_data)

X_train, X_test, y_train, y_test = train_test_split(data.tweet, data.sentiment, test_size=0.1)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(data['tweet'])
#print(X_train_counts.shape)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = LogisticRegression().fit(X_train_tfidf, data['sentiment'])

text_to_analyse = ['Curso excelente bom e incrível adorei']
X_new_counts = count_vect.transform(text_to_analyse)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

print("Text to analyze: " + text_to_analyse[0])
predicted = clf.predict(X_new_tfidf)
print("Predicted as: ")
if predicted[0] == 1:
    print("Positive")
else:
    print("Negative")

text_to_analyse = ['Muito ruim odiei']
X_new_counts = count_vect.transform(text_to_analyse)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

print("Text to analyze: " + text_to_analyse[0])
predicted = clf.predict(X_new_tfidf)
print("Predicted as: ")
if predicted[0] == 1:
    print("Positive")
else:
    print("Negative")

    
text_to_analyse = ['Esse jogo é excelente']
X_new_counts = count_vect.transform(text_to_analyse)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

print("Text to analyze: " + text_to_analyse[0])
predicted = clf.predict(X_new_tfidf)
print("Predicted as: ")
if predicted[0] == 1:
    print("Positive")
else:
    print("Negative")
