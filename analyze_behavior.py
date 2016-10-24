import os
import vdmlab as vdm
from core import Rat, assign_label
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data')
output_filepath = os.path.join(thisdir, 'plots')

sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!':
        sessions.append(os.path.join(data_filepath, file))

rats = ['1', '2', '3', '4', '5', '6', '7', '8']

data = dict()
for rat in rats:
    data[rat] = Rat(rat)

n_sessions = len(sessions)

for session in sessions:
    rats_data = vdm.load_medpc(os.path.join(data_filepath, session), assign_label)

    for rat in rats:
        data[rat].add_session(**rats_data[rat])

only_sound = False

if 1:
    for rat in rats:
        if only_sound:
            filename = 'sound_rat' + rat + '_behavior.png'
        else:
            filename = 'rat' + rat + '_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(data, [rat], n_sessions, filepath, only_sound=only_sound)

if 1:
    filenames = ['group1_behavior.png', 'group2_behavior.png',
                 'all-rats_behavior.png', 'exp-rats_behavior.png']
    sound_filenames = ['sound_group1_behavior.png', 'sound_group2_behavior.png',
                       'sound_all-rats_behavior.png', 'sound_exp-rats_behavior.png']
    rat_groups = [['1', '3', '5', '7'], ['2', '4', '6', '8'], rats, ['1', '2', '3', '5', '6', '7', '8']]

    for i, rat in enumerate(rat_groups):
        if only_sound:
            filepath = os.path.join(output_filepath, sound_filenames[i])
        else:
            filepath = os.path.join(output_filepath, filenames[i])
        plot_behavior(data, rat, n_sessions, filepath, only_sound=only_sound)
