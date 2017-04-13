import os
import nept
from core import Rat, combine_rats
from load_data import assign_label
from plotting import plot_behavior, plot_duration


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'spring2017')
output_filepath = os.path.join(thisdir, 'plots', 'spring2017')

magazine_session = '!2017-04-14'

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file != magazine_session and file[0] == '!':
        sessions.append(os.path.join(data_filepath, file))

rats = ['R141', 'R142', 'R143', 'R144', 'R145', 'R146', 'R147', 'R148']
groups = [1, 2, 2, 1, 2, 1, 1, 2]
males = ['R141', 'R143', 'R145', 'R147']
females = ['R142', 'R144', 'R146', 'R148']
group1 = ['R141', 'R144', 'R146', 'R147']
group2 = ['R142', 'R143', 'R145', 'R148']

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

for session in sessions:
    rats_data = nept.load_medpc(os.path.join(data_filepath, session), assign_label)

    for rat, group in zip(rats, groups):
        data[rat].add_session(**rats_data[rat], group=group)

n_sessions = len(data[rats[0]].sessions)

df = combine_rats(data, rats, n_sessions)


if 1:
    for rat in rats:
        filename = rat + '_outcome_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=True)

if 1:
    for rat in rats:
        filename = rat + '_outcome_duration.png'
        filepath = os.path.join(output_filepath, filename)
        plot_duration(df, [rat], filepath, by_outcome=True, ymax=10.)

if 0:
    for rat in rats:
        filename = rat + '_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=False)

if 0:
    for by_outcome in [True, False]:
        filenames = ['group1_trials_medpc.png', 'group2_trials_medpc.png', 'all-rats_trials_medpc.png']
        outcome_filenames = ['group1_outcome_medpc.png', 'group2_outcome_medpc.png', 'all-rats_outcome_medpc.png',
                             'female_outcome_medpc.png', 'male_outcome_medpc.png']
        rat_groups = [group1, group2, rats, females, males]

        for i, rat in enumerate(rat_groups):
            if by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, by_outcome=by_outcome)
