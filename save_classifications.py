import argparse
import csv
import os
import pickle
import statistics

from core import constants


def get_means(classifications, category):
    scores_zip = zip(*[classifier[category] for classifier in classifications['classifiers'].values()])
    return [statistics.mean(scores) for scores in scores_zip]


parser = argparse.ArgumentParser()
parser.add_argument('infiles', nargs='+', type=argparse.FileType('r'))
args = parser.parse_args()

classifications = {
    'classifiers': {},
    'means': {},
}
for classifier, csvfile in enumerate(args.infiles, 1):
    classifications['classifiers'][classifier] = {
        'lexical': [],
        'syntactic': [],
        'semantic': [],
    }
    reader = csv.DictReader(csvfile)
    for row in reader:
        classifications['classifiers'][classifier]['lexical'].append(int(row['Lexical']))
        classifications['classifiers'][classifier]['syntactic'].append(int(row['Syntactic']))
        classifications['classifiers'][classifier]['semantic'].append(int(row['Semantic']))

classifications['means']['lexical'] = get_means(classifications, 'lexical')
classifications['means']['syntactic'] = get_means(classifications, 'syntactic')
classifications['means']['semantic'] = get_means(classifications, 'semantic')

with open(os.path.join(constants.DATA_DIR, 'classifications.pickle'), 'wb') as f:
    pickle.dump(classifications, f)
