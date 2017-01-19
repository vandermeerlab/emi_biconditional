import os
import numpy as np

from core import Rat, combine_rats
from load_data import load_biconditional_events_old, vdm_assign_label, remove_trial_events
from plotting import plot_behavior

import info.RH05d1 as RH05d1
import info.RH05d2 as RH05d2
import info.RH05d3 as RH05d3
import info.RH05d4 as RH05d4
import info.RH05d5 as RH05d5
import info.RH05d6 as RH05d6

import info.R105d1 as R105d1
import info.R105d2 as R105d2
import info.R105d3 as R105d3
import info.R105d4 as R105d4
import info.R105d5 as R105d5
import info.R105d6 as R105d6

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'vdmlab_fall2016')
output_filepath = os.path.join(thisdir, 'plots', 'fall2016')

rat5_sessions = [RH05d1, RH05d2, RH05d3, RH05d4, RH05d5, RH05d6]
rat8_sessions = [R105d1, R105d2, R105d3, R105d4, R105d5, R105d6]
all_sessions = [rat5_sessions, rat8_sessions]

rats = ['5', '8']
group1 = ['5']
group2 = ['8']

for rat, sessions in zip(rats, all_sessions):
    data = dict()
    data[rat] = Rat(rat, group1, group2)

    for session in sessions:
        events = load_biconditional_events_old(os.path.join(data_filepath, session.event_file))

        if session == R105d1:
            events = remove_trial_events(events, 'trial3')
            events['light2_on'] = np.delete(events['light2_on'], 11)
            rats_data = vdm_assign_label(events, min_n_trials=16)
        else:
            rats_data = vdm_assign_label(events)
        data[rat].add_session(**rats_data)

    n_sessions = len(data[rat].sessions)

    df = combine_rats(data, [rat], n_sessions)

    filename = 'vdmlab_trials_rat' + rat + '_behavior.png'
    filepath = os.path.join(output_filepath, filename)
    plot_behavior(df, [rat], filepath=filepath, only_sound=False, by_outcome=False)
