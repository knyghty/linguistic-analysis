import os
import pickle
import statistics

from scipy import stats

from core import constants


with open(os.path.join(constants.DATA_DIR, 'classifications.pickle'), 'rb') as f:
    classifications = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'scores.pickle'), 'rb') as f:
    scores = pickle.load(f)

lexical_scores = classifications['means']['lexical']
syntactic_scores = classifications['means']['syntactic']
semantic_scores = classifications['means']['semantic']
mean_scores = [statistics.mean(scores) for scores in zip(*[lexical_scores, syntactic_scores, semantic_scores])]

lilla_scores = [score['lilla'] for score in scores.values()]
silla_scores = [score['silla'] for score in scores.values()]
wv_scores = [score['wv'] for score in scores.values()]
wv_conversation_scores = [score['wv_conversation'] for score in scores.values()]
lsm_scores = [score['lsm'] for score in scores.values()]


r, p = stats.pearsonr(lexical_scores, lilla_scores)
print('Lexical vs LILLA: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(syntactic_scores, silla_scores)
print('Syntactic vs SILLA: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(semantic_scores, wv_scores)
print('Semantic vs Word2vec: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(lexical_scores, wv_scores)
print('Lexical vs Word2vec: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(syntactic_scores, wv_scores)
print('Syntactic vs Word2vec: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(mean_scores, wv_scores)
print('Mean vs Word2vec: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(semantic_scores, wv_conversation_scores)
print('Semantic vs Word2vec (conversation): r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(mean_scores, lsm_scores)
print('Mean vs LSM: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(lexical_scores, lsm_scores)
print('Lexical vs LSM: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(syntactic_scores, lsm_scores)
print('Syntactic vs LSM: r={r}, p={p:.20f}'.format(r=r, p=p))

r, p = stats.pearsonr(semantic_scores, lsm_scores)
print('Semantic vs LSM: r={r}, p={p:.20f}'.format(r=r, p=p))
