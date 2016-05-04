import os
import pickle
import statistics

from spacy.en import English
from textblob import TextBlob

from core import constants
from measures import lla, lsm
from twtr import utils


nlp = English()
nlp.vocab.load_vectors(os.path.join(constants.DATA_DIR, 'word2vec_twitter_model.bin'))


with open(os.path.join(constants.DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

parsed_chains = utils.parse_chains(chains, escape_html=False)

chain_scores = {}
for chain_id, chain in parsed_chains.items():
    messages_a = [{'textblob': TextBlob(message), 'spacy': nlp(message)} for message in chain[::2]]
    messages_b = [{'textblob': TextBlob(message), 'spacy': nlp(message)} for message in chain[1::2]]
    chain_scores[chain_id] = {}

    lilla_scores = []
    silla_scores = []
    lsm_scores = []
    wv_scores = []

    for counter, message_a in enumerate(messages_a, 1):
        for message_b in messages_b[counter:]:
            lilla_scores.append(float(lla.lilla(message_a['textblob'].words, message_b['textblob'].words)))
            silla_scores.append(float(lla.silla(message_a['spacy'], message_b['spacy'])))
            lsm_scores.append(float(lsm.dyad_lsm(message_a['spacy'], message_b['spacy'])))
            wv_scores.append(float(message_a['spacy'].similarity(message_b['spacy'])))

    for counter, message_b in enumerate(messages_b, 1):
        for message_a in messages_a[counter:]:
            lilla_scores.append(float(lla.lilla(message_a['textblob'].words, message_b['textblob'].words)))
            silla_scores.append(float(lla.silla(message_a['spacy'], message_b['spacy'])))
            lsm_scores.append(float(lsm.dyad_lsm(message_a['spacy'], message_b['spacy'])))
            wv_scores.append(float(message_a['spacy'].similarity(message_b['spacy'])))

    chain_scores[chain_id]['lilla'] = statistics.mean(lilla_scores)
    chain_scores[chain_id]['silla'] = statistics.mean(silla_scores)
    chain_scores[chain_id]['lsm'] = statistics.mean(lsm_scores)
    chain_scores[chain_id]['wv'] = statistics.mean(wv_scores)

with open(os.path.join(constants.DATA_DIR, 'scores.pickle'), 'wb') as f:
    pickle.dump(chain_scores, f)
