import os
import vdmlab as vdm
from core import Rat, combine_rats
from load_data import assign_label
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data')
output_filepath = os.path.join(thisdir, 'plots')

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!':
        sessions.append(os.path.join(data_filepath, file))

rats = ['1', '2', '3', '4', '5', '6', '7']

data = dict()
for rat in rats:
    data[rat] = Rat(rat)

for session in sessions:
    rats_data = vdm.load_medpc(os.path.join(data_filepath, session), assign_label)

    for rat in rats:
        data[rat].add_session(**rats_data[rat])

n_sessions = len(data[rats[0]].sessions)

df = combine_rats(data, rats, n_sessions)

if 1:
    for rat in rats:
        filename = 'rat' + rat + '_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=by_outcome)

    for by_outcome in [True, False]:
        filenames = ['trials_group1_behavior.png', 'trials_group2_behavior.png', 'trials_all-rats_behavior.png']
        outcome_filenames = ['outcome_group1_behavior.png', 'outcome_group2_behavior.png', 'outcome_all-rats_behavior.png']
        rat_groups = [['1', '3', '5', '7'], ['2', '4', '6'], rats]

        for i, rat in enumerate(rat_groups):
            if by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, by_outcome=by_outcome)
