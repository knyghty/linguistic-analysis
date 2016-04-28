import os
import pickle

from core import constants


with open(os.path.join(constants.DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)


with open('data.txt', 'w') as f:
    for counter, chain in enumerate(chains, 1):
        f.write('Chain {num}\n'.format(num=counter))
        for status in chain:
            f.write('{author}: {status}\n'.format(author=status.author.screen_name, status=status.text))
        f.write('------------------------------------------------\n\n')
