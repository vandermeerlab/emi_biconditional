import numpy as np

import measurements as m
from core import Experiment, Rat, TrialEpoch

epoch_expt = Experiment(
    name="test",
    plot_key="",
    cache_key="",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('1', group="1"),
        Rat('2', group="2"),
        Rat('3', group="1"),
        Rat('4', group="2"),
        Rat('5', group="1"),
        Rat('6', group="2"),
        Rat('7', group="1"),
        Rat('8', group="2"),
    ],
    ignore_sessions='',
    sessionfiles=['!roborats']
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" else "unrewarded",
                "cue": cue,
            }
            trial = data[trial]
            cue = data[cue]
            session.add_epoch_data(rat.rat_id, trial.intersect(cue), meta)
        else:
            meta = {
                "cue_type": cue,
                "trial_type": "",
                "rewarded": "",
                "cue": cue,
            }
            session.add_epoch_data(rat.rat_id, data[cue], meta)

    add_data("light1", "trial1")
    add_data("sound1", "trial1")
    add_data("light2", "trial2")
    add_data("sound1", "trial2")
    add_data("light1", "trial3")
    add_data("sound2", "trial3")
    add_data("light2", "trial4")
    add_data("sound2", "trial4")
    add_data("baseline")

epoch_expt.add_datapoints = add_datapoints
df = epoch_expt.analyze()


def test_no_mags():
    rat = '1'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                       groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))


def test_all_mags():
    rat = '2'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                       groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))


def test_sound_only():
    rat = '3'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))


def test_light_only():
    rat = '4'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))


def test_rewarded_sound():
    rat = '5'
    cue = 'light'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    cue = 'sound'
    for trial in [2, 3]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    for trial in [1, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))


def test_iti_only():
    rat = '6'
    for cue in ['light', 'sound']:
        for trial in [1, 2, 3, 4]:
            this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                       groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
            assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))


def test_half_light():
    rat = '7'
    cue = 'sound'
    for trial in [1, 2, 3, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    cue = 'light'
    for trial in [1, 4]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    for trial in [2, 3]:
        this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
                   groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 5.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
        assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))


def test_complex():
    rat = '8'

    trial = 1
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 9.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 1.98))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    trial = 2
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    trial = 3
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 2.5))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 2.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 1.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 1.0))

    trial = 4
    cue = 'light'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))

    cue = 'sound'
    this_df = (df.groupby(['rat']).get_group(rat).groupby(['cue_type']).get_group(cue).
               groupby(['trial_type']).get_group(str(trial))[['measure', 'value']])

    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Duration']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Count']['value']), 0.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'Latency']['value']), 10.0))
    assert (np.allclose(np.mean(this_df[this_df['measure'] == 'AtLeastOne']['value']), 0.0))
