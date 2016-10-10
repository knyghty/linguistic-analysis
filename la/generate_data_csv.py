import csv
import itertools
import os
import pickle

from core import constants
from twtr import utils


with open(os.path.join(constants.DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

parsed_chains = utils.parse_chains(chains)

with open(os.path.join(constants.DATA_DIR, 'data.csv'), 'w') as csvfile:
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
