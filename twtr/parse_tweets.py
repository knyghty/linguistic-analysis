import os
import pickle


def get_authors(chain):
    a = chain[0].author.screen_name
    b = next(status.author.screen_name for status in chain[1:] if status.author.screen_name != a)
    return a, b


DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DIR, 'data')

with open(os.path.join(DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

for chain in chains:
    print(get_authors(chain))
