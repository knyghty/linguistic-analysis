import itertools
import os
import pickle

from scipy import stats

from core import constants


with open(os.path.join(constants.DATA_DIR, 'classifications.pickle'), 'rb') as c, \
        open(os.path.join(constants.DATA_DIR, 'scores.pickle'), 'rb') as s:
    classifications = pickle.load(c)
    scores = pickle.load(s)


scores_dict = {}
for measure in ['lsm', 'lilla', 'silla', 'wv']:
    scores_dict[measure] = [chain_scores[measure] for chain_scores in scores.values()]

for measure_a, measure_b in itertools.combinations(scores_dict.keys(), 2):
    print(measure_a, 'vs', measure_b)
    r, p = stats.pearsonr(scores_dict[measure_a], scores_dict[measure_b])
    print('r={r}, p={p:.20f}'.format(r=r, p=p))

print()

for category_a, category_b in itertools.combinations(classifications['means'].keys(), 2):
    print(category_a, 'vs', category_b)
    r, p = stats.pearsonr(classifications['means'][category_a], classifications['means'][category_b])
    print('r={r}, p={p:.20f}'.format(r=r, p=p))
