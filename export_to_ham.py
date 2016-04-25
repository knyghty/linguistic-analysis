import csv
import os
import pickle

from twtr import utils


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'twtr', 'data')


with open(os.path.join(DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)


def build_user_tsv():
    fieldnames = ['uid', 'screenname', 'verified', 'numtweets', 'numfriends', 'numfollowers', 'numlistsin',
                  'numfavoritesgiven', 'creationyear', 'creationmonth', 'creationdate']
    for conversation_id, chain in enumerate(chains, 1):
        authors = {status.author for status in chain}
        with open(os.path.join(DATA_DIR, 'ham', conversation_id.zfill(3) + '_users.tsv')) as f:
            writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=fieldnames)
            for author in authors:
                writer.writerow({
                    'uid': author.id_str,
                    'screenname': author.screen_name,
                    'verified': author.verified,
                    'numtweets': author.statuses_count,
                    'numfriends': author.friends_count,
                    'numfollowers': author.followers_count,
                    'numlistsin': author.listed_count,
                    'numfavoritesgiven': author.favourites_count,
                    'creationyear': author.created_at.year,
                    'creationmonth': author.created_at.month,
                    'creationdate': author.created_at.day,
                })


def build_status_tsv():
    fieldnames = ['msguser', 'msgtext', 'replyid', 'replyuser', 'replytext']

    for conversation_id, chain in enumerate(chains, 1):
        with open(os.path.join(DATA_DIR, 'ham', conversation_id.zfill(3) + '.tsv')) as f:
            writer = csv.DictWriter(f, dialect='excel-tab', fieldnames=fieldnames)
            previous_status = None
            for status in chain:
                if conversation_id == 1:
                    previous_status = status
                    continue

                assert status.in_reply_to_status_id_str == previous_status.id_str

                writer.writerow({
                    'msgid': status.id_str,
                    'msguser': status.author.id_str,
                    'msgtext': utils.format_message(status.text, is_ham=True),
                    'replyid': previous_status.id_str,
                    'replyuser': previous_status.author.id_str,
                    'replytext': previous_status.replytext.id_str,
                })


build_user_tsv()
build_status_tsv()
