import os
import scipy.stats as stats

from load_data import assign_label, load_biconditional_events_general, vdm_assign_label
from core import Rat, combine_rats
import nept

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'spring2017')

# Finds newest session id
this_id = 0
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!':
        session = file[1:5] + file[6:8] + file[9:]
        if int(session) > this_id:
            this_id = int(session)
            session_id = file[1:]

# If interested in a particular session, uncomment below.
# Otherwise this evaluates only the newest session.
# session_id = '2017-04-13'
print('checking session:', session_id)

rats = ['R141', 'R142', 'R143', 'R144', 'R145', 'R146', 'R147', 'R148']
groups = [1, 2, 2, 1, 2, 1, 1, 2]
males = ['R141', 'R143', 'R145', 'R147']
females = ['R142', 'R144', 'R146', 'R148']
group1 = ['R141', 'R144', 'R146', 'R147']
group2 = ['R142', 'R143', 'R145', 'R148']

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

filename = os.path.join(data_filepath, '!' + session_id)
rats_data = nept.load_medpc(filename, assign_label)

for rat, group in zip(rats, groups):
    data[rat].add_session(**rats_data[rat], group=group)

n_sessions = len(data[rats[0]].sessions)

df = combine_rats(data, rats, n_sessions)

duration_df = df[df['measure'] == 'durations']

for rat in rats:
    print('\n', rat)
    for outcome in ['rewarded', 'unrewarded']:
        outcome_df = duration_df[duration_df['rewarded'] == 'sound ' + outcome]
        rat_df = outcome_df[outcome_df['rat'] == rat]
        print(outcome, ':', rat_df['value'].mean(), '+/-', stats.sem(rat_df['value']))
