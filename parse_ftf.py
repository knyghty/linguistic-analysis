import os
import statistics

import matplotlib.pyplot as plt
from spacy.en import English
from textblob import TextBlob

from core import constants
from measures import lla, lsm


nlp = English()


NEUTRAL_DIR = os.path.join(constants.DATA_DIR, 'ftf', 'Neutral')
POWER_DIR = os.path.join(constants.DATA_DIR, 'ftf', 'Power')


def flatten(conversation):
    flattened = {}
    flattened['A'] = '\n'.join(conversation[::2])
    flattened['B'] = '\n'.join(conversation[1::2])
    return flattened


def parse_flat(flattened):
    parsed = {'A': {}, 'B': {}}
    flat_a = flattened['A']
    flat_b = flattened['B']
    parsed['A']['spacy'] = nlp(flat_a)
    parsed['B']['spacy'] = nlp(flat_b)
    parsed['A']['tb'] = TextBlob(flat_a)
    parsed['B']['tb'] = TextBlob(flat_b)
    return parsed


def sliding_window(utterances, window_size=1):
    window_dict = {'A': {}, 'B': {}}
    for counter, utterance in enumerate(utterances['A']):
        window_dict['A'][counter] = {'response': utterance, 'cues': []}
        for window in range(window_size, 0, -1):
            index = counter - window
            if index < 0 or index >= len(utterances['B']):
                continue
            window_dict['A'][counter]['cues'].append(utterances['B'][index])

    for counter, utterance in enumerate(utterances['B']):
        window_dict['B'][counter] = {'response': utterance, 'cues': []}
        for window in range(window_size, 0, -1):
            index = counter - window + 1
            if index < 0 or index >= len(utterances['A']):
                continue
            window_dict['B'][counter]['cues'].append(utterances['A'][index])

    return window_dict


def slider(conversation):
    utterances = {'A': flatten(conversation)['A'].split('\n'), 'B': flatten(conversation)['B'].split('\n')}
    windows = {}
    for window_size in range(1, max(len(utterances['A']), len(utterances['B'])) + 1):
        windows[window_size] = sliding_window(utterances, window_size)

    return windows


def windowed_scores(windows):
    scores = {}
    for window_size, conversation in windows.items():
        scores[window_size] = {}
        for participant_id, participant in conversation.items():
            scores[window_size][participant_id] = {}
            scores[window_size]['mean'] = {}
            lsm_scores = []
            lilla_scores = []
            for utterance in participant.values():
                response_tb = TextBlob(utterance['response'])
                for cue in utterance['cues']:
                    cue_tb = TextBlob(cue)
                    lsm_scores.append(lsm.dyad_lsm(cue_tb.words, response_tb.words, lsm_func=lsm.liwc_lsm))
                    lilla_scores.append(lla.lilla(cue_tb.words, response_tb.words))

            scores[window_size][participant_id]['lsm'] = statistics.mean(lsm_scores)
            scores[window_size][participant_id]['lilla'] = statistics.mean(lilla_scores)

        scores[window_size]['mean']['lsm'] = statistics.mean((scores[window_size]['A']['lsm'],
                                                              scores[window_size]['B']['lsm']))
        scores[window_size]['mean']['lilla'] = statistics.mean((scores[window_size]['A']['lilla'],
                                                                scores[window_size]['B']['lilla']))
    return scores


neutral_set = []
power_set = []


for filename in os.listdir(NEUTRAL_DIR):
    with open(os.path.join(NEUTRAL_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        neutral_set.append(conversation)


for filename in os.listdir(POWER_DIR):
    with open(os.path.join(POWER_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        power_set.append(conversation)


neutral_lsm_scores = []
neutral_liwc_lsm_scores = []
neutral_lilla_scores = []
neutral_silla_scores = []

power_lsm_scores = []
power_liwc_lsm_scores = []
power_lilla_scores = []
power_silla_scores = []

scores = []
for conversation in power_set:
    windows = slider(conversation)
    scores.append(windowed_scores(windows))


for conversation in scores:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lsm'])
    plt.plot(x, y)

plt.show()


for conversation in neutral_set:
    conversation = parse_flat(flatten(conversation))
    neutral_lsm_scores.append(lsm.dyad_lsm(conversation['A']['spacy'], conversation['B']['spacy']))
    neutral_liwc_lsm_scores.append(lsm.dyad_lsm(conversation['A']['tb'].words, conversation['B']['tb'].words,
                                                lsm_func=lsm.liwc_lsm))
    neutral_lilla_scores.append(lla.lilla(conversation['A']['tb'].words, conversation['B']['tb'].words))
    neutral_silla_scores.append(lla.silla(conversation['A']['spacy'], conversation['B']['spacy']))

for conversation in power_set:
    conversation = parse_flat(flatten(conversation))
    power_lsm_scores.append(lsm.dyad_lsm(conversation['A']['spacy'], conversation['B']['spacy']))
    power_liwc_lsm_scores.append(lsm.dyad_lsm(conversation['A']['tb'].words, conversation['B']['tb'].words,
                                              lsm_func=lsm.liwc_lsm))
    power_lilla_scores.append(lla.lilla(conversation['A']['tb'].words, conversation['B']['tb'].words))
    power_silla_scores.append(lla.silla(conversation['A']['spacy'], conversation['B']['spacy']))

print('========================================')
print('Flat')
print()
print('Neutral LILLA: {lilla}'.format(lilla=statistics.mean(neutral_lilla_scores)))
print('Power LILLA: {lilla}'.format(lilla=statistics.mean(power_lilla_scores)))
print()
print('Neutral SILLA: {silla}'.format(silla=statistics.mean(neutral_lilla_scores)))
print('Power SILLA: {silla}'.format(silla=statistics.mean(power_silla_scores)))
print()
print('Neutral LSM: {lsm}'.format(lsm=statistics.mean(neutral_lsm_scores)))
print('Power LSM: {lsm}'.format(lsm=statistics.mean(power_lsm_scores)))
print()
print('Neutral LIWC LSM: {lsm}'.format(lsm=statistics.mean(neutral_liwc_lsm_scores)))
print('Power LIWC LSM: {lsm}'.format(lsm=statistics.mean(power_liwc_lsm_scores)))
