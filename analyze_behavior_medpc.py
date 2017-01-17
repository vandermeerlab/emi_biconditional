import os
import vdmlab as vdm
from core import Rat, combine_rats
from load_data import assign_label
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'winter2017')
output_filepath = os.path.join(thisdir, 'plots')

magazine_session = '!2017-01-17'

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file != magazine_session and file[0] == '!':
        sessions.append(os.path.join(data_filepath, file))

rats = ['R120', 'R121', 'R118', 'R119', 'R116', 'R117', 'R114']
group1 = ['R120', 'R118', 'R116', 'R114']
group2 = ['R121', 'R119', 'R117']

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

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
        plot_behavior(df, [rat], filepath, by_outcome=True)

if 1:
    for by_outcome in [True, False]:
        filenames = ['trials_group1_behavior.png', 'trials_group2_behavior.png', 'trials_all-rats_behavior.png']
        outcome_filenames = ['outcome_group1_behavior.png', 'outcome_group2_behavior.png', 'outcome_all-rats_behavior.png']
        rat_groups = [group1, group2, rats]

        for i, rat in enumerate(rat_groups):
            if by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, by_outcome=by_outcome)
