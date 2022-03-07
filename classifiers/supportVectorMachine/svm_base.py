DATA_DIR = './bbc/'

from sklearn.datasets import load_files
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

data = load_files(DATA_DIR, encoding="utf-8", decode_error="replace")

# calculate count of each category
labels, counts = np.unique(data.target, return_counts=True)

print(labels, counts)

labels_str = np.array(data.target_names)[labels]
print(dict(zip(labels_str, counts)))

# data prep
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)
print(len(X_train))
print(len(X_test))

vectorizer = TfidfVectorizer(max_features=1000, decode_error="ignore")
vectorizer.fit(X_train)

# model
cls = LinearSVC()
cls.fit(vectorizer.transform(X_train), y_train)

y_pred = cls.predict(vectorizer.transform(X_test))

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))