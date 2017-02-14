import os
import scipy.stats as stats

from load_data import assign_label, load_biconditional_events_general, vdm_assign_label
from core import Rat, combine_rats
import vdmlab as vdm

thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'winter2017')

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
# session_id = '2017-01-19'
print('checking session:', session_id)

# rats in medpc boxes
rats = ['R120', 'R121', 'R118', 'R119', 'R116', 'R117', 'R114']
groups = [1, 2, 1, 2, 1, 2, 1]
group1 = ['R120', 'R118', 'R116', 'R114']
group2 = ['R121', 'R119', 'R117']

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

filename = os.path.join(data_filepath, '!' + session_id)
rats_data = vdm.load_medpc(filename, assign_label)

for rat, group in zip(rats, groups):
    data[rat].add_session(**rats_data[rat], group=group)

n_sessions = len(data[rats[0]].sessions)

df = combine_rats(data, rats, n_sessions)

duration_df = df[df['measure'] == 'durations']

for rat in rats:
    print(rat)
    for outcome in ['rewarded', 'unrewarded']:
        outcome_df = duration_df[duration_df['rewarded'] == 'sound ' + outcome]
        rat_df = outcome_df[outcome_df['rat'] == rat]
        print(outcome, ':', rat_df['value'].mean(), '+/-', stats.sem(rat_df['value']))


# rat in recording box
rat = 'R115'
group2 = [rat]

data = dict()
data[rat] = Rat(rat, group2)

rec_filename = os.path.join(data_filepath, 'R115-' + session_id + '-Events.nev')
events = load_biconditional_events_general(rec_filename, photobeam='zero')
# events = load_biconditional_events_general(rec_filename, photobeam='c')

rats_data = vdm_assign_label(events)
data[rat].add_session(**rats_data, group=2)

n_sessions = len(data[rat].sessions)

df = combine_rats(data, [rat], n_sessions)

duration_df = df[df['measure'] == 'durations']

print(rat)
for outcome in ['rewarded', 'unrewarded']:
    outcome_df = duration_df[duration_df['rewarded'] == 'sound ' + outcome]
    rat_df = outcome_df[outcome_df['rat'] == rat]
    print(outcome, ':', rat_df['value'].mean(), '+/-', stats.sem(rat_df['value']))
