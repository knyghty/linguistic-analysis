import os
import pickle
import statistics

from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import svm

from core import constants


with open(os.path.join(constants.DATA_DIR, 'ftf_neutral_window.pickle'), 'rb') as f:
    neutral_window_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_power_window.pickle'), 'rb') as f:
    power_window_scores = pickle.load(f)

window_sizes = []
mean_scores = []

for conversation in power_window_scores + neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lsm'])
        max_window_size = max(max_window_size, window_size)
    mean_scores.append([statistics.mean(means)])
    window_sizes.append(max_window_size)

clf = svm.SVC(kernel='linear', C=1)
model = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', LinearRegression())])

scores = cross_val_score(clf, mean_scores, window_sizes, cv=5)
print('SVC Accuracy: {} (+/- {})'.format(scores.mean(), scores.std() * 2))

scores = cross_val_score(model, mean_scores, window_sizes, cv=5)
print('PR Accuracy: {} (+/- {})'.format(scores.mean(), scores.std() * 2))
