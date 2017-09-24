import os
import numpy as np
import nept

from core import combine_rats, Rat

from load_data import load_biconditional_events_general, vdm_assign_label
from plotting import plot_behavior

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'winter2017')
output_filepath = os.path.join(thisdir, 'plots', 'winter2017')

magazine_session = 'R115-2017-01-17-Events.nev'
c_photobeams = ['R115-2017-01-26-Events.nev']
missing_events = ['R115-2017-02-11-Events.nev', 'R115-2017-02-16-Events.nev']
missing_value = [('sound1_on', 6, 'sound1_off'), ('sound1_on', 3, 'sound1_off')]

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file != magazine_session and file[-4:] == '.nev':
        sessions.append(os.path.join(data_filepath, file))

rat = 'R115'
group2 = [rat]

data = dict()
data[rat] = nept.Rat(rat, group2)

for session in sessions:
    if session[-26:] in c_photobeams:
        events = load_biconditional_events_general(session, photobeam='c')
    else:
        events = load_biconditional_events_general(session, photobeam='zero')

    for i, missing in enumerate(missing_events):
        if missing == session[-26:]:
            events[missing_value[i][0]] = np.insert(events[missing_value[i][0]],
                                                    missing_value[i][1],
                                                    np.array(events[missing_value[i][2]][missing_value[i][1]] - 10))

    rats_data = vdm_assign_label(events)
    data[rat].add_biconditional_session(**rats_data, group=2)

n_sessions = len(data[rat].sessions)

df = nept.combine_rats(data, [rat], n_sessions)

if 1:
    filename = rat + '_outcome_behavior.png'
    filepath = os.path.join(output_filepath, filename)
    plot_behavior(df, [rat], filepath=filepath, only_sound=False, by_outcome=True)

if 1:
    filename = rat + '_behavior.png'
    filepath = os.path.join(output_filepath, filename)
    plot_behavior(df, [rat], filepath=filepath, only_sound=False, by_outcome=False)
