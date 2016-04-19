import os
import pickle


DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DIR, 'data')


def get_authors(chain):
    return set(status.author.screen_name for status in chain)


with open(os.path.join(DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

for chain in chains:
    print(get_authors(chain))
