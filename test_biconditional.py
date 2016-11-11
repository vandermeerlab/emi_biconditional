import os
import numpy as np
import vdmlab as vdm
from core import Rat, assign_label, combine_rats

thisdir = os.path.dirname(os.path.realpath(__file__))
roborats = os.path.join(thisdir, 'cache', 'other', '!roborats')

rats_data = vdm.load_medpc(roborats, assign_label)

rats = ['1', '2', '3', '4', '5', '6', '7', '8']

data = dict()
for rat in rats:
    data[rat] = Rat(rat)
    data[rat].add_session(**rats_data[rat])

n_sessions = len(data['1'].sessions)
only_sound = False

df = combine_rats(data, rats, n_sessions, only_sound=False)

def test_no_mags():
    rat = '1'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                       groupby(['trial_type']).get_group(trial)[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))


def test_all_mags():
    rat = '2'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                       groupby(['trial_type']).get_group(trial)[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))


def test_sound_only():
    rat = '3'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))


def test_light_only():
    rat = '4'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))


def test_rewarded_sound():
    rat = '5'
    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    cue = 'sound'
    for trial in [2, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    for trial in [1, 3]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))


def test_iti_only():
    rat = '6'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                       groupby(['trial_type']).get_group(trial)[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))


def test_half_light():
    rat = '7'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    cue = 'light'
    for trial in [1, 3]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    for trial in [2, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
                   groupby(['trial_type']).get_group(trial)[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))


def test_complex():
    rat = '8'

    trial = 1  # are the trial numbers correct?
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    trial = 2
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 0.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    trial = 3
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 9.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 1.98))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    trial = 4  # or should it be trial 1?
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 2.5))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 2.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue']).get_group(cue).
               groupby(['trial_type']).get_group(trial)[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'durations']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'numbers']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'responses']['value']), 100.0))
