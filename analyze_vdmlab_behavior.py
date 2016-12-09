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

sessions = [RH01d1, RH01d1]


this_rat = '1'

rats = [this_rat]
data = dict()
data[this_rat] = Rat(this_rat)

for session in sessions:
    events = get_events(session.event_mat)
    rats_data = vdm_assign_label(events)
    data[this_rat].add_session(**rats_data)

n_sessions = len(data[this_rat].sessions)

df = combine_rats(data, rats, n_sessions)

filename = 'vdmlab_trials_rat1_behavior.png'
filepath = os.path.join(output_filepath, filename)
plot_behavior(df, [this_rat], filepath=filepath, only_sound=False, by_outcome=False)
