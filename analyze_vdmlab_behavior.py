import os
import numpy as np
import scipy
import matplotlib.pyplot as plt

import vdmlab as vdm
from core import Rat, vdm_assign_label, combine_rats
from load_data import get_events
from plotting import plot_behavior

import info.RH01d1 as RH01d1
import info.RH01d2 as RH01d2

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'vdmlab')
output_filepath = os.path.join(thisdir, 'plots')

sessions = [RH01d1, RH01d2]


def correct_timestamps(events):
    events['cue_on'] = events['cue']

    events['cue_off'] = []
    for on in events['cue_on']:
        for off in events['main_off']:
            if np.allclose(on + 10, off, atol=0.5):
                events['cue_off'].append(off)
    events['cue_off'] = np.array(events['cue_off'])

    max_flash = 2.0
    between_flashes = np.diff(events['house'])
    events['house_on'] = [events['house'][0]]
    trial_idx = np.where(between_flashes > max_flash)[0]
    events['house_on'].extend(events['house'][trial_idx + 1])
    events['house_on'] = np.array(events['house_on'])

    events['house_off'] = []
    events['house_off'].extend(events['house'][trial_idx])
    events['house_off'].append(events['house'][-1])
    events['house_off'] = np.array(events['house_off'])

    return events


this_rat = '1'

rats = [this_rat]
data = dict()
data[this_rat] = Rat(this_rat)

for session in sessions:
    events = get_events(session.event_mat)

    events = correct_timestamps(events)

    rats_data = vdm_assign_label(events)

    data[this_rat].add_session_medpc(**rats_data, n_unique=2, delay=5.0, tolerance=1.7)

n_sessions = len(data[this_rat].sessions)

df = combine_rats(data, rats, n_sessions)

filename = 'vdmlab_trials_rat1_behavior.png'
filepath = os.path.join(output_filepath, filename)
plot_behavior(df, [this_rat], filepath=None, only_sound=False, by_outcome=False)
