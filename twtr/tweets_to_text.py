import pickle


with open('selected_tweets.pickle', 'rb') as f:
    chains = pickle.load(f)


with open('data.txt', 'w') as f:
    for counter, chain in enumerate(chains):
        f.write('Chain {num}\n'.format(num=counter + 1))
        for status in chain:
            f.write('{author}: {status}\n'.format(author=status.author.screen_name, status=status.text))
        f.write('------------------------------------------------\n\n')
