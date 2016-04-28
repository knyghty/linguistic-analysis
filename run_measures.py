import os
import pickle

from spacy.en import English
from textblob import TextBlob

from core import constants
from measures import lla, lsm
from twtr import utils


nlp = English()


with open(os.path.join(constants.DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

parsed_chains = utils.parse_chains(chains, escape_html=False)

for chain_id, chain in parsed_chains.items():
    messages_a = [{'textblob': TextBlob(message), 'spacy': nlp(message)} for message in chain[::2]]
    messages_b = [{'textblob': TextBlob(message), 'spacy': nlp(message)} for message in chain[1::2]]

    for counter, message_a in enumerate(messages_a, 1):
        for message_b in messages_b[counter:]:
            lilla_score = lla.lilla(message_a['textblob'].words, message_b['textblob'].words)
            silla_score = lla.silla(message_a['spacy'], message_b['spacy'])
            lsm_score = lsm.dyad_lsm(message_a['spacy'], message_b['spacy'])
            wv_score = message_a['spacy'].similarity(message_b['spacy'])

    for counter, message_b in enumerate(messages_b, 1):
        for message_a in messages_a[counter:]:
            lilla_score = lla.lilla(message_a['textblob'].words, message_b['textblob'].words)
            silla_score = lla.silla(message_a['spacy'], message_b['spacy'])
            lsm_score = lsm.dyad_lsm(message_a['spacy'], message_b['spacy'])
            wv_score = message_a['spacy'].similarity(message_b['spacy'])
