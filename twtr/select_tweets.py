import pickle

from distutils.util import strtobool


def query_yes_no(question, default="yes"):
    print('{question} [y/n]'.format(question=question))
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")


with open('tweets.pickle', 'rb') as f:
    chains = pickle.load(f)

keepers = []
for chain in chains:
    for status in chain:
        print('{author}: {status}'.format(author=status.author.screen_name, status=status.text))
    is_keeper = query_yes_no('Do you want to keep this chain?')

    if is_keeper:
        keepers.append(chain)

with open('selected_tweets.pickle', 'wb') as f:
    pickle.dump(keepers, f)
