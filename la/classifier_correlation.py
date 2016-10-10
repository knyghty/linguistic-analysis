import itertools
import os
import pickle

from scipy import stats

from core import constants


with open(os.path.join(constants.DATA_DIR, 'classifications.pickle'), 'rb') as f:
    classifications = pickle.load(f)

pairs = itertools.combinations(classifications['classifiers'].keys(), 2)

for classifier_a, classifier_b in pairs:
    print('Classifiers', classifier_a, 'and', classifier_b)

    lexical_a = classifications['classifiers'][classifier_a]['lexical']
    lexical_b = classifications['classifiers'][classifier_b]['lexical']
    r, p = stats.pearsonr(lexical_a, lexical_b)
    print('Lexical: r={r}, p={p}'.format(r=r, p=p))

    syntactic_a = classifications['classifiers'][classifier_a]['syntactic']
    syntactic_b = classifications['classifiers'][classifier_b]['syntactic']
    r, p = stats.pearsonr(syntactic_a, syntactic_b)
    print('Syntactic: r={r}, p={p}'.format(r=r, p=p))

    semantic_a = classifications['classifiers'][classifier_a]['semantic']
    semantic_b = classifications['classifiers'][classifier_b]['semantic']
    r, p = stats.pearsonr(semantic_a, semantic_b)
    print('Semantic: r={r}, p={p}'.format(r=r, p=p))
