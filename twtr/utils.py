import html
import itertools
import validators


def normalise_urls(text):
    for word in text.split(' '):
        if validators.url(word):
            text = text.replace(word, '[URL]')
    return text


def remove_screen_names(text):
    while True:
        text = text.lstrip()
        word = text.split(' ')[0]
        if not word.startswith('@'):
            break

        text = text.replace(word, '')
    return text


def format_message(text, escape_html=True):
    text = remove_screen_names(text)
    text = normalise_urls(text)
    if escape_html:
        text = html.unescape(text)
    return text.strip()


def parse_chains(chains, escape_html=True):
    parsed_chains = {}
    for counter, chain in enumerate(chains):
        messages = []
        for key, group in itertools.groupby(chain, lambda x: x.author.screen_name):
            merged = []
            for status in group:
                merged.append(format_message(status.text, escape_html))

            merged = '\n'.join(merged)
            messages.append(merged)

        parsed_chains[counter] = messages
    return parsed_chains
