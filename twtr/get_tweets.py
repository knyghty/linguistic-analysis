import os
import pickle
import sys

import tweepy

from core import constants


CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_status_chain(api, status_id):
    """Given a status ID, iterate up the chain of tweets and return them in order.

    This function doesn't look further down the chain, it only looks up, so it could be incomplete.
    We also stop short if we hit a third author, as we only care about dyads.

    Keyword arguments:
    api -- tweepy API object
    status_id -- ID of the status to start from
    """
    authors = []
    statuses = []

    while True:
        status = api.get_status(status_id)
        author = status.author.screen_name

        # Check we're in a dyadic conversation.
        if len(authors) < 2 and author not in authors:
            authors.append(author)
        elif author not in authors:
            # No longer a dyad, cut off at this status and only use the dyadic part.
            break

        statuses.append(status)

        if not status.in_reply_to_status_id_str:
            break

        status_id = status.in_reply_to_status_id_str

    statuses.reverse()
    return statuses


chains = []

page = 1
while len(chains) < 200:
    statuses = None
    while statuses is None:
        try:
            statuses = api.search(q='filter:replies', count=100, lang='en')
        except Exception as e:
            print('Error: {error}. Retrying.'.format(error=e), file=sys.stderr)

    if statuses:
        for status in statuses:
            try:
                status_chain = get_status_chain(api, status.id_str)
                if len(status_chain) > 9:
                    chains.append(status_chain)
            except Exception as e:
                # We hit a private message or a connection issue, skip to the next.
                print('Error: {error}. Continuing.'.format(error=e), file=sys.stderr)
                continue

            print(len(chains))
            if len(chains) >= 200:
                break
    else:
        break

    page += 1

with open(os.path.join(constants.DATA_DIR, 'tweets.pickle'), 'wb') as f:
    pickle.dump(chains, f)
