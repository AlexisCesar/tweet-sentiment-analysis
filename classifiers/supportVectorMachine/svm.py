import re
from time import sleep
import pandas
import json
import numpy
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2

json_data = None
with open('../../mock/mockTestData.json', encoding='utf-8') as data_file:
    lines = data_file.readlines()
    joined_lines = "[" + ",".join(lines) + "]"

    json_data = json.loads(joined_lines)

data = pandas.DataFrame(json_data)

stemmer = SnowballStemmer('portuguese')
words = stopwords.words("portuguese")

data['cleaned'] = data['tweet'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.sentiment, test_size=0.2)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=150)),
                     ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=2000, dual=False))])


model = pipeline.fit(X_train, y_train)

vectorizer = model.named_steps['vect']
chi = model.named_steps['chi']
clf = model.named_steps['clf']

feature_names = vectorizer.get_feature_names_out()
feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
feature_names = numpy.asarray(feature_names)

print("accuracy score: " + str(model.score(X_test, y_test)))

text_to_classify = "bom demais amei"

print(model.predict([text_to_classify]))