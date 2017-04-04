import matplotlib.pyplot as plt
import os
import numpy as np

import nept
from core import Rat
from load_data import assign_label, load_biconditional_events_general, vdm_assign_label

data_filepath = 'E:/code/emi_biconditional/cache/data/winter2017'


session_id = '2017-01-22'
this_rat = 'R115'


rats = ['R120', 'R121', 'R118', 'R119', 'R116', 'R117', 'R114']
other_rat = 'R115'

if this_rat in rats:
    filename = os.path.join(data_filepath, '!' + session_id)
    groups = [1, 2, 1, 2, 1, 2, 1]
    group1 = ['R120', 'R118', 'R116', 'R114']
    group2 = ['R121', 'R119', 'R117']

    data = dict()
    for rat in rats:
        data[rat] = Rat(rat, group1, group2)

    rats_data = nept.load_medpc(filename, assign_label)

elif this_rat == other_rat:
    filename = os.path.join(data_filepath, 'R115-' + session_id + '-Events.nev')
    group2 = [other_rat]

    data = dict()
    data[other_rat] = Rat(other_rat, group2)

    events = load_biconditional_events_general(filename, photobeam='zero')

    rats_data = dict()
    rats_data[other_rat] = vdm_assign_label(events)

else:
    raise ValueError("unrecognized rat ID")

trial_order = []
for trial in ['trial1', 'trial2', 'trial3', 'trial4']:
    for start, stop in zip(rats_data[this_rat][trial].starts, rats_data[this_rat][trial].stops):
        trial_order.append((trial, nept.Epoch(start, stop-start)))

ordered = sorted(trial_order, key=lambda x: x[1].start)

mags = rats_data[this_rat]['mags']
sounds1 = rats_data[this_rat]['sounds1']
sounds2 = rats_data[this_rat]['sounds2']

durations = []
for t in ordered:
    trial = t[0]
    trial_epoch = t[1]

    if trial in ['trial1', 'trial4']:
        sound_epochs = trial_epoch.intersect(sounds2)
        cue_mags = sound_epochs.intersect(mags)
        durations.append(np.sum(cue_mags.durations))
    if trial in ['trial2', 'trial3']:
        sound_epochs = trial_epoch.intersect(sounds1)
        cue_mags = sound_epochs.intersect(mags)
        durations.append(np.sum(cue_mags.durations))

trials = []
for label in ordered:
    trials.append(label[0])

ax = plt.subplot(111)
plt.plot(durations, 'k', ms=4)
plt.xticks(range(32), trials, rotation='vertical')
plt.title(this_rat + ' session ' + session_id)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.show()
