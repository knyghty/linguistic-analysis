import os
import pickle
import random
import statistics

from textblob import TextBlob

from core import constants
from measures import lla, lsm


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
    parsed['A']['tb'] = TextBlob(flat_a)
    parsed['B']['tb'] = TextBlob(flat_b)
    return parsed


def flat_scores(conversation):
    conversation = parse_flat(flatten(conversation))
    score = {
        'lsm': lsm.dyad_lsm(conversation['A']['tb'].words, conversation['B']['tb'].words, lsm_func=lsm.liwc_lsm),
        'lilla': lla.lilla(conversation['A']['tb'].words, conversation['B']['tb'].words),
    }
    return score


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

short_neutral_set = []
short_power_set = []

very_short_neutral_set = []
very_short_power_set = []

random_very_short_neutral_set = []
random_very_short_power_set = []

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


for filename in os.listdir(NEUTRAL_DIR):
    with open(os.path.join(NEUTRAL_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            if len(conversation) == 20:
                break
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        short_neutral_set.append(conversation)


for filename in os.listdir(POWER_DIR):
    with open(os.path.join(POWER_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            if len(conversation) == 20:
                break
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        short_power_set.append(conversation)


for filename in os.listdir(NEUTRAL_DIR):
    with open(os.path.join(NEUTRAL_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            if len(conversation) == 10:
                break
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        very_short_neutral_set.append(conversation)


for filename in os.listdir(POWER_DIR):
    with open(os.path.join(POWER_DIR, filename), encoding='latin-1') as f:
        conversation = []
        for line in f.readlines():
            if len(conversation) == 10:
                break
            line = line.strip()[2:].strip()
            if line:
                conversation.append(line)
        very_short_power_set.append(conversation)


for filename in os.listdir(NEUTRAL_DIR):
    with open(os.path.join(NEUTRAL_DIR, filename), encoding='latin-1') as f:
        conversation = [line for line in f.readlines() if line.strip()]
        length = len(conversation)
        if length < 10:
            continue

        start = random.randrange(length - 9)
        random_very_short_neutral_set.append(conversation[start:start + 10])


for filename in os.listdir(POWER_DIR):
    with open(os.path.join(POWER_DIR, filename), encoding='latin-1') as f:
        conversation = [line for line in f.readlines() if line.strip()]
        length = len(conversation)
        if length < 10:
            continue

        start = random.randrange(length - 9)
        random_very_short_power_set.append(conversation[start:start + 10])


neutral_flat_scores = []
neutral_window_scores = []
power_flat_scores = []
power_window_scores = []

short_neutral_flat_scores = []
short_neutral_window_scores = []
short_power_flat_scores = []
short_power_window_scores = []

very_short_neutral_flat_scores = []
very_short_neutral_window_scores = []
very_short_power_flat_scores = []
very_short_power_window_scores = []

random_very_short_neutral_flat_scores = []
random_very_short_neutral_window_scores = []
random_very_short_power_flat_scores = []
random_very_short_power_window_scores = []

for conversation in neutral_set:
    neutral_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    neutral_window_scores.append(windowed_scores(windows))

for conversation in power_set:
    power_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    power_window_scores.append(windowed_scores(windows))

for conversation in short_neutral_set:
    short_neutral_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    short_neutral_window_scores.append(windowed_scores(windows))

for conversation in short_power_set:
    short_power_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    short_power_window_scores.append(windowed_scores(windows))

for conversation in very_short_neutral_set:
    very_short_neutral_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    very_short_neutral_window_scores.append(windowed_scores(windows))

for conversation in very_short_power_set:
    very_short_power_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    very_short_power_window_scores.append(windowed_scores(windows))

for conversation in random_very_short_neutral_set:
    random_very_short_neutral_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    random_very_short_neutral_window_scores.append(windowed_scores(windows))

for conversation in random_very_short_power_set:
    random_very_short_power_flat_scores.append(flat_scores(conversation))
    windows = slider(conversation)
    random_very_short_power_window_scores.append(windowed_scores(windows))


with open(os.path.join(constants.DATA_DIR, 'ftf_neutral_flat.pickle'), 'wb') as f:
    pickle.dump(neutral_flat_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_power_flat.pickle'), 'wb') as f:
    pickle.dump(power_flat_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_neutral_window.pickle'), 'wb') as f:
    pickle.dump(neutral_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_power_window.pickle'), 'wb') as f:
    pickle.dump(power_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_neutral_flat.pickle'), 'wb') as f:
    pickle.dump(short_neutral_flat_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_power_flat.pickle'), 'wb') as f:
    pickle.dump(short_power_flat_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_neutral_window.pickle'), 'wb') as f:
    pickle.dump(short_neutral_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_power_window.pickle'), 'wb') as f:
    pickle.dump(short_power_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_very_short_neutral_window.pickle'), 'wb') as f:
    pickle.dump(very_short_neutral_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_very_short_power_window.pickle'), 'wb') as f:
    pickle.dump(very_short_power_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_random_very_short_neutral_window.pickle'), 'wb') as f:
    pickle.dump(random_very_short_neutral_window_scores, f)

with open(os.path.join(constants.DATA_DIR, 'ftf_random_very_short_power_window.pickle'), 'wb') as f:
    pickle.dump(random_very_short_power_window_scores, f)
