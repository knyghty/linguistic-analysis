import csv
import itertools
import os
import pickle

from twtr import utils


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'twtr', 'data')


with open(os.path.join(DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

parsed_chains = utils.parse_chains(chains)

with open(os.path.join(DATA_DIR, 'data.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Text'])
    for chain in parsed_chains.values():
        row = ''
        author = itertools.cycle('AB')
        for message in chain:
            row += '<p><strong>{author}</strong>: {message}</p>'.format(
                author=next(author), message=message
            ).replace('\n', '<br>')
        writer.writerow([row])
