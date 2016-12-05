import os
import numpy as np
import scipy
import matplotlib.pyplot as plt

import vdmlab as vdm
from core import Rat, vdm_assign_label, combine_rats
from load_data import get_events
from plotting import plot_behavior

import info.RH01d1 as RH01d1

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'vdmlab')
output_filepath = os.path.join(thisdir, 'plots')


def correct_timestamps(events):
    events['cue_on'] = events['cue']

    events['cue_off'] = []
    for on in events['cue_on']:
        for off in events['main_off']:
            if np.allclose(on + 10, off, atol=0.5):
                events['cue_off'].append(off)
    events['cue_off'] = np.array(events['cue_off'])

    events['house_on'] = [events['house'][0], events['house'][7], events['house'][14], events['house'][21]]
    events['house_on'] = np.array(events['house_on'])

    events['flash_off'] = [events['house'][6], events['house'][13], events['house'][20], events['house'][-1]]

    events['house_off'] = []
    for last in events['flash_off']:
        for off in events['main_off']:
            if np.allclose(last, off, atol=0.5):
                events['house_off'].append(off)
    events['house_off'] = np.array(events['house_off'])

    return events


this_rat = '1'

rats = [this_rat]
data = dict()
data[this_rat] = Rat(this_rat)

sessions = [RH01d1]

for session in sessions:
    events = get_events(session.event_mat)

    if session == 'RH01d1':
        events = correct_timestamps(events)

    rats_data = vdm_assign_label(events)

    data[this_rat].add_session(**rats_data, n_unique=2, delay=5.0, tolerance=1.7)

n_sessions = len(data[this_rat].sessions)

df = combine_rats(data, rats, n_sessions)

filename = 'vdmlab_trials_rat1_behavior.png'
filepath = os.path.join(output_filepath, filename)
plot_behavior(df, ['1'], filepath, only_sound=False, by_outcome=False)
