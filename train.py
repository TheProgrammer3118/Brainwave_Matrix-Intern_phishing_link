import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import numpy as np
import os

print("Files in the current directory:", os.listdir('.'))

data = pd.read_csv('url_dataset.csv')

if 'url' not in data.columns or 'label' not in data.columns:
    raise ValueError("The dataset must contain 'url' and 'label' columns.")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['url'])
y = data['label']

sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

params = {'alpha': [0.1, 0.5, 1.0]}
grid_search = GridSearchCV(MultinomialNB(), params, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
model = grid_search.best_estimator_

accuracy = model.score(X_test, y_test)
print(f'Model accuracy: {accuracy * 100:.2f}%')

y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

labels = np.unique(y)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=labels))

# Save the model and vectorizer
joblib.dump(model, 'url_classifier_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model and vectorizer saved successfully.")
