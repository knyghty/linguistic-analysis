import collections
import os
import pickle
import statistics

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

from core import constants


with open(os.path.join(constants.DATA_DIR, 'ftf_neutral_flat.pickle'), 'rb') as f:
    neutral_flat_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_power_flat.pickle'), 'rb') as f:
    power_flat_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_neutral_window.pickle'), 'rb') as f:
    neutral_window_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_power_window.pickle'), 'rb') as f:
    power_window_scores = pickle.load(f)


with open(os.path.join(constants.DATA_DIR, 'ftf_short_neutral_flat.pickle'), 'rb') as f:
    short_neutral_flat_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_power_flat.pickle'), 'rb') as f:
    short_power_flat_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_neutral_window.pickle'), 'rb') as f:
    short_neutral_window_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_short_power_window.pickle'), 'rb') as f:
    short_power_window_scores = pickle.load(f)


with open(os.path.join(constants.DATA_DIR, 'ftf_very_short_neutral_window.pickle'), 'rb') as f:
    very_short_neutral_window_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_very_short_power_window.pickle'), 'rb') as f:
    very_short_power_window_scores = pickle.load(f)


with open(os.path.join(constants.DATA_DIR, 'ftf_random_very_short_neutral_window.pickle'), 'rb') as f:
    random_very_short_neutral_window_scores = pickle.load(f)

with open(os.path.join(constants.DATA_DIR, 'ftf_random_very_short_power_window.pickle'), 'rb') as f:
    random_very_short_power_window_scores = pickle.load(f)


'''LSM'''

plt.figure(0)

for conversation in power_window_scores[:10]:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lsm'])
    plt.plot(x, y)

plt.show()


plt.figure(1)

for conversation in power_window_scores + neutral_window_scores:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lsm'])
    plt.plot(y, x)

plt.show()


plt.figure(2)

window_sizes = []
mean_scores = []

for conversation in power_window_scores + neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lsm'])
        max_window_size = max(max_window_size, window_size)
    mean_scores.append(statistics.mean(means))
    window_sizes.append(max_window_size)

r, p = stats.pearsonr(window_sizes, mean_scores)
print('r={r}, p={p:.20f}'.format(r=r, p=p))

plt.plot(mean_scores, window_sizes, 'ro')
plt.show()


plt.figure(3)

max_window_size = 0
scores = {}

for conversation in power_window_scores + neutral_window_scores:
    for window_size in conversation.keys():
        max_window_size = max(max_window_size, window_size)

for conversation in power_window_scores + neutral_window_scores:
    for window_size, parsed in conversation.items():
        if window_size not in scores:
            scores[window_size] = []

        scores[window_size].append(parsed['mean']['lsm'])

scores = collections.OrderedDict(sorted(scores.items()))
data = []
x = []

for k, v in scores.items():
    if len(v) > 1:
        x.append(k)
        data.append(v)

print(len(data))
y = np.array([np.mean(row) for row in data])

cis = []
for row in data:
    mean = np.mean(row)
    std = np.std(row)
    cis.append(stats.norm.interval(0.95, loc=np.mean(row), scale=std))

ci_lower = [ci[0] for ci in cis]
ci_upper = [ci[1] for ci in cis]
cis = [ci_lower, ci_upper]

offsets = np.abs(cis - y[None, :])

plt.fill_between(x, y - offsets[0], y + offsets[1], facecolor=(0.8, 0.8, 0.8))
plt.errorbar(x, y, yerr=offsets, color=(0.8, 0.8, 0.8))
plt.plot(x, y, 'k', linewidth=3)
plt.show()


plt.figure(4)

for conversation in short_power_window_scores + short_neutral_window_scores:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lsm'])
    plt.plot(x, y)

plt.show()


plt.figure(5)

# Window sizes are still correct from the previous run
mean_scores = []

for conversation in short_power_window_scores + short_neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lsm'])
    mean_scores.append(statistics.mean(means))

r, p = stats.pearsonr(window_sizes, mean_scores)
print('r={r}, p={p:.20f}'.format(r=r, p=p))

plt.plot(mean_scores, window_sizes, 'ro')
plt.show()


plt.figure(6)

power_diffs = []
neutral_diffs = []

for conversation in power_window_scores:
    diffs = []
    for window_size, parsed in conversation.items():
        diffs.append(abs(parsed['A']['lsm'] - parsed['B']['lsm']))
    power_diffs.append(statistics.mean(diffs))

for conversation in neutral_window_scores:
    diffs = []
    for window_size, parsed in conversation.items():
        diffs.append(abs(parsed['A']['lsm'] - parsed['B']['lsm']))
    neutral_diffs.append(statistics.mean(diffs))

power_diffs_mean = statistics.mean(power_diffs)
neutral_diffs_mean = statistics.mean(neutral_diffs)

power_diffs_median = statistics.median(power_diffs)
neutral_diffs_median = statistics.median(neutral_diffs)

print('Power set mean:', power_diffs_mean)
print('Neutral set mean:', neutral_diffs_mean)

print('Power set median:', power_diffs_median)
print('Neutral set median:', neutral_diffs_median)

power_x = range(len(power_diffs))
neutral_x = range(len(neutral_diffs))

plt.plot(power_x, power_diffs, 'ro')
plt.plot(neutral_x, neutral_diffs, 'bo')
plt.show()


plt.figure(7)

mean_scores = []

for conversation in very_short_power_window_scores + very_short_neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lsm'])
    mean_scores.append(statistics.mean(means))

r, p = stats.pearsonr(window_sizes, mean_scores)
print('r={r}, p={p:.20f}'.format(r=r, p=p))

plt.plot(mean_scores, window_sizes, 'ro')
plt.show()


plt.figure(8)

mean_scores = []

for conversation in random_very_short_power_window_scores + random_very_short_neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lsm'])
    mean_scores.append(statistics.mean(means))

r, p = stats.pearsonr(window_sizes, mean_scores)
print('r={r}, p={p:.20f}'.format(r=r, p=p))

plt.plot(mean_scores, window_sizes, 'ro')
plt.show()


'''LILLA'''

plt.figure(100)

for conversation in power_window_scores[:10]:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lilla'])
    plt.plot(x, y)

plt.show()


plt.figure(101)

for conversation in power_window_scores + neutral_window_scores:
    x = []
    y = []
    for window_size, parsed in conversation.items():
        x.append(window_size)
        y.append(parsed['mean']['lilla'])
    plt.plot(x, y)

plt.show()


window_sizes = []
mean_scores = []

for conversation in power_window_scores + neutral_window_scores:
    means = []
    max_window_size = 0
    for window_size, parsed in conversation.items():
        means.append(parsed['mean']['lilla'])
        max_window_size = max(max_window_size, window_size)
    mean_scores.append(statistics.mean(means))
    window_sizes.append(max_window_size)

r, p = stats.pearsonr(window_sizes, mean_scores)
print('r={r}, p={p:.20f}'.format(r=r, p=p))

plt.figure(102)
plt.plot(mean_scores, window_sizes, 'ro')
plt.show()
