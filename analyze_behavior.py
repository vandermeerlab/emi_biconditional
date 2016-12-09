import os
import vdmlab as vdm
from core import Rat, assign_label, combine_rats
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data')
output_filepath = os.path.join(thisdir, 'plots')

broken_sessions = ['!2016-10-19a1', '!2016-10-19a2']
sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!' and file not in broken_sessions:
        sessions.append(os.path.join(data_filepath, file))

# rats = ['1', '2', '3', '4', '5', '6', '7', '8']
rats = ['5', '8']

data = dict()
for rat in rats:
    data[rat] = Rat(rat)

broken_a = os.path.join(data_filepath, broken_sessions[0])
broken_b = os.path.join(data_filepath, broken_sessions[1])
rats_data_a = vdm.load_medpc(broken_a, assign_label)
rats_data_b = vdm.load_medpc(broken_b, assign_label)

for rat in rats_data_a:
    for key in rats_data_a[rat]:
        rats_data_b[rat][key].join(rats_data_a[rat][key])
for rat in rats:
    data[rat].add_session_medpc(**rats_data_b[rat])

for session in sessions:
    rats_data = vdm.load_medpc(os.path.join(data_filepath, session), assign_label)

    for rat in rats:
        data[rat].add_session_medpc(**rats_data[rat])

n_sessions = len(data[rats[0]].sessions)
only_sound = False

df = combine_rats(data, rats, n_sessions, only_sound)

if 1:
    for by_outcome in [True, False]:
        for rat in rats:
            if only_sound:
                filename = 'sound_rat' + rat + '_behavior.png'
            elif by_outcome:
                filename = 'outcome_rat' + rat + '_behavior.png'
            else:
                filename = 'trials_rat' + rat + '_behavior.png'
            filepath = os.path.join(output_filepath, filename)
            plot_behavior(df, [rat], filepath, only_sound=only_sound, by_outcome=by_outcome, change_sessions=[35, 46, 52])

        filenames = ['trials_group1_behavior.png', 'trials_group2_behavior.png',
                     'trials_all-rats_behavior.png', 'trials_exp-rats_behavior.png',
                     'trials_bucci-rats_behavior.png']
        sound_filenames = ['sound_group1_behavior.png', 'sound_group2_behavior.png',
                           'sound_all-rats_behavior.png', 'sound_exp-rats_behavior.png',
                           'sound_bucci-rats_behavior.png']
        outcome_filenames = ['outcome_group1_behavior.png', 'outcome_group2_behavior.png',
                             'outcome_all-rats_behavior.png', 'outcome_exp-rats_behavior.png',
                             'outcome_bucci-rats_behavior.png']
        rat_groups = [['1', '3', '5', '7'], ['2', '4', '6', '8'], rats, ['1', '2', '3', '5', '6', '7', '8'],
                      ['1', '2', '3', '4', '5', '6']]

        for i, rat in enumerate(rat_groups):
            if only_sound:
                filepath = os.path.join(output_filepath, sound_filenames[i])
            elif by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, only_sound=only_sound, by_outcome=by_outcome, change_sessions=[35, 46, 52])
