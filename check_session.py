import os

from load_data import assign_label, load_biconditional_events_general, vdm_assign_label
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
# Otherwise this checks only the newest session.
# session_id = '2017-04-13'
print('checking session:', session_id)


def check_session(data, n_unique_trial=8, n_feeder=16, n_light=16, n_sound=16, n_mags=0):
    for trial in ['trial1', 'trial2', 'trial3', 'trial4']:
        n_trial = data[trial].n_epochs
        assert(n_trial == n_unique_trial)

    for light, sound in zip(['lights1', 'lights2'], ['sounds1', 'sounds2']):
        n_trial = data[light].n_epochs
        assert(n_trial == n_light)

        n_trial = data[sound].n_epochs
        assert(n_trial == n_sound)

    n_trial = data['pellets'].n_epochs
    assert(n_trial == n_feeder or n_trial == n_feeder*2)

    n_trial = data['mags'].n_epochs
    assert(n_trial > n_mags)

    print('passed')

rats = ['R141', 'R142', 'R143', 'R144', 'R145', 'R146', 'R147', 'R148']

# rats in medpc boxes
filename = os.path.join(data_filepath, '!' + session_id)
data = nept.load_medpc(filename, assign_label)

for rat in rats:
    print(rat, ':')
    check_session(data[rat])
