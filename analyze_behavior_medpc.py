import os
import numpy as np

import nept
from load_data import assign_occset_label
from plotting import plot_behavior, plot_duration


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'spring2017')
output_filepath = os.path.join(thisdir, 'plots', 'fall2017')

print(thisdir)

magazine_session = '!2017-04-14'

# sessions = []
# for file in sorted(os.listdir(data_filepath)):
#     if file != magazine_session and file[0] == '!':
#         sessions.append(os.path.join(data_filepath, file))

sessions = ['!2017-05-30', '!2017-05-31', '!2017-06-01']

rats = ['R141', 'R142', 'R143', 'R144', 'R145', 'R146', 'R147', 'R148']
groups = [1, 2, 2, 1, 2, 1, 1, 2]
males = ['R141', 'R143', 'R145', 'R147']
females = ['R142', 'R144', 'R146', 'R148']
group1 = ['R141', 'R144', 'R146', 'R147']
group2 = ['R142', 'R143', 'R145', 'R148']

cue_duration = 10.

data = dict()
for rat in rats:
    data[rat] = nept.Rat(rat, group1, group2)

for session in sessions:
    rats_data = nept.load_medpc(os.path.join(data_filepath, session), assign_occset_label)

    for rat in rats:
        iti_starts = []
        iti_stops = []
        for trial in ['trial1', 'trial2']:
            iti_starts.extend(rats_data[rat][trial].starts - cue_duration)
            iti_stops.extend(rats_data[rat][trial].starts)

        rats_data[rat]['pre_cs'] = nept.Epoch(np.vstack([iti_starts, iti_stops]))

        post_rewarded_starts = []
        post_rewarded_stops = []
        for trial in ['trial2']:
            post_rewarded_starts.extend(rats_data[rat][trial].stops)
            post_rewarded_stops.extend(rats_data[rat][trial].stops + cue_duration)
        rats_data[rat]['post_rewarded'] = nept.Epoch(np.vstack([post_rewarded_starts, post_rewarded_stops]))

        post_unrewarded_starts = []
        post_unrewarded_stops = []
        for trial in ['trial1']:
            post_unrewarded_starts.extend(rats_data[rat][trial].stops)
            post_unrewarded_stops.extend(rats_data[rat][trial].stops + cue_duration)
        rats_data[rat]['post_unrewarded'] = nept.Epoch(np.vstack([post_unrewarded_starts, post_unrewarded_stops]))

    for rat, group in zip(rats, groups):
        data[rat].add_long_feature_session(mags=rats_data[rat]['mags'],
                                           pellets=rats_data[rat]['pellets'],
                                           lights1=rats_data[rat]['lights1'],
                                           lights2=rats_data[rat]['lights2'],
                                           sounds1=rats_data[rat]['sounds1'],
                                           trial1=rats_data[rat]['trial1'],
                                           trial2=rats_data[rat]['trial2'],
                                           group=group)

n_sessions = len(data[rats[0]].sessions)
print('n_sessions:', n_sessions)

df = nept.combine_rats(data, rats, n_sessions)
print(rats_data)

if 1:
    for rat in rats:
        filename = rat + '_outcome_behavior.png'
        filepath = os.path.join(output_filepath, filename)
        plot_behavior(df, [rat], filepath, by_outcome=True, change_sessions=[11, 21, 46])

if 1:
    filenames = ['group1_medpc.png', 'group2_medpc.png', 'all-rats_medpc.png',
                 'female_medpc.png', 'male_medpc.png']
    rat_groups = [group1, group2, rats, females, males]

    for i, rat in enumerate(rat_groups):
        filepath = os.path.join(output_filepath, filenames[i])
        plot_duration(df, rat, filepath, by_outcome=True, ymax=10., change_sessions=[11, 21, 46])
