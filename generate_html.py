import itertools
import os
import pickle

from twtr import utils


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'twtr', 'data')
HTML_DIR = os.path.join(BASE_DIR, 'html')


with open(os.path.join(DATA_DIR, 'selected_tweets.pickle'), 'rb') as f:
    chains = pickle.load(f)

parsed_chains = utils.parse_chains(chains)

html = """
<meta charset="utf-8">
<title>Test</title>
<script src="https://twemoji.maxcdn.com/twemoji.min.js"></script>
<style>
  /*
    EmojiSymbols Font (c)blockworks - Kenichi Kaneko
    http://emojisymbols.com/
  */
  @font-face {
    font-family: "EmojiSymbols";
    src: url('EmojiSymbols-Regular.woff') format('woff');
    text-decoration: none;
    font-style: normal;
  }
  body {
    font-family: 'EmojiSymbols', sans-serif;
    line-height: 1;
    font-size: 24px;
  }
</style>
"""

for counter, chain in parsed_chains.items():
    html += '<h1>Conversation {counter}</h1>'.format(counter=counter + 1)
    author = itertools.cycle('AB')
    for message in chain:
        html += '<p><strong>{author}</strong>: {message}</p>'.format(
            author=next(author), message=message
        ).replace('\n', '<br>')

with open(os.path.join(HTML_DIR, 'messages.html'), 'w') as f:
    f.write(html)
