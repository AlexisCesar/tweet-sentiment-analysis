from sklearn.datasets import make_classification
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd

# TODO Add logistic regression classifier

# Generating dataset

x, y = make_classification(
    n_samples=100,
    n_features=1,
    n_classes=2,
    n_clusters_per_class=1,
    flip_y=0.03,
    n_informative=1,
    n_redundant=0,
    n_repeated=0
)

#print(x)
#print(y)

#pyplot.scatter(x, y, c = y, cmap='rainbow')
#pyplot.title('Logistic Regression')
#pyplot.show()

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

classifier = LogisticRegression()
classifier.fit(x_train, y_train)

prediction = classifier.predict(x_test)

#print(confusion_matrix(y_test, prediction)) [TP, FP], [FN, TN]

matrix = confusion_matrix(y_test, prediction)

print('TP:' + str(matrix[0][0]) + " | FP:" + str(matrix[0][1]))
print('FN:' + str(matrix[1][0]) + " | TN:" + str(matrix[1][1]))
