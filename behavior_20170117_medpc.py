import os
import nept

from load_data import assign_label
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'winter2017')
output_filepath = os.path.join(thisdir, 'plots', 'winter2017')

magazine_session = '!2017-01-17'

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file != magazine_session and file[0] == '!':
        sessions.append(os.path.join(data_filepath, file))

rats = ['R120', 'R121', 'R118', 'R119', 'R116', 'R117', 'R114']
groups = [1, 2, 1, 2, 1, 2, 1]
group1 = ['R120', 'R118', 'R116', 'R114']
group2 = ['R121', 'R119', 'R117']

data = dict()
for rat in rats:
    data[rat] = nept.Rat(rat, group1, group2)

for session in sessions:
    rats_data = nept.load_medpc(os.path.join(data_filepath, session), assign_label)

    for rat, group in zip(rats, groups):
        data[rat].add_biconditional_session(**rats_data[rat], group=group)

n_sessions = len(data[rats[0]].sessions)

df = nept.combine_rats(data, rats, n_sessions)


if 1:
    for rat in rats:
        filename = rat + '_outcome_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=True)

if 1:
    for rat in rats:
        filename = rat + '_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=False)

if 1:
    for by_outcome in [True, False]:
        filenames = ['group1_trials_medpc.png', 'group2_trials_medpc.png', 'all-rats_trials_medpc.png']
        outcome_filenames = ['group1_outcome_medpc.png', 'group2_outcome_medpc.png', 'all-rats_outcome_medpc.png']
        rat_groups = [group1, group2, rats]

        for i, rat in enumerate(rat_groups):
            if by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, by_outcome=by_outcome)
