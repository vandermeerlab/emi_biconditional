import os
import nept
from core import Rat, combine_rats
from load_data import assign_medpc_label
from plotting import plot_behavior


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'med_fall2016')
output_filepath = os.path.join(thisdir, 'plots', 'fall2016')

broken_sessions = ['!2016-10-19a1', '!2016-10-19a2']
extended = ['!2016-11-28', '!2016-11-29', '!2016-11-30', '!2016-12-01', '!2016-12-02', '!2016-12-03',
            '!2016-12-06', '!2016-12-07a', '!2016-12-07b', '!2016-12-08', '!2016-12-09']
sessions = []
extended_sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!' and file not in broken_sessions and file not in extended:
        sessions.append(os.path.join(data_filepath, file))
    if file[0] == '!' and file not in broken_sessions and file not in extended:
        extended_sessions.append(os.path.join(data_filepath, file))

rats = ['1', '2', '3', '4', '5', '6', '7', '8']
group1 = ['1', '3', '5', '7']
group2 = ['2', '4', '6', '8']

plot_extended = True
if plot_extended:
    rats = ['5', '8']
    sessions = extended_sessions

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

broken_a = os.path.join(data_filepath, broken_sessions[0])
broken_b = os.path.join(data_filepath, broken_sessions[1])
rats_data_a = nept.load_medpc(broken_a, assign_medpc_label)
rats_data_b = nept.load_medpc(broken_b, assign_medpc_label)

for rat in rats_data_a:
    for key in rats_data_a[rat]:
        rats_data_b[rat][key].join(rats_data_a[rat][key])
for rat in rats:
    data[rat].add_session_medpc(**rats_data_b[rat])

for session in sessions:
    rats_data = nept.load_medpc(os.path.join(data_filepath, session), assign_medpc_label)

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
            plot_behavior(df, [rat], filepath, only_sound=only_sound, by_outcome=by_outcome,
                          change_sessions=[35, 46, 52])

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
