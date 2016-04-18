import pickle


with open('tweets.pickle', 'rb') as f:
    chains = pickle.load(f)

print(len(chains))

for chain in chains:
    print(len(chain))
    for tweet in chain:
        print(tweet.text)
