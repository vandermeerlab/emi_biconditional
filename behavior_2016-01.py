import measurements as m
from core import Experiment, Rat, TrialEpoch

cached_data = True

# rats = ["R081", "R079", "R082", "R083", "R074"]
counterconditioning_sessions = ['!2016-02-20', '!2016-02-21', '!2016-02-22', '!2016-02-23']
test_session = ['!2016-02-24']

expt = Experiment(
    name="201601",
    cache_key="epoch",
    plot_key="",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("baseline", start_idx=8, duration=-10),
        TrialEpoch("baseline", start_idx=10, duration=-10),
        TrialEpoch("light", start_idx=4, stop_idx=5),
        TrialEpoch("sound", start_idx=6, stop_idx=7),
        TrialEpoch("trial1", start_idx=8, stop_idx=9),
        TrialEpoch("trial2", start_idx=10, stop_idx=11),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('1', group="1"),
        Rat('2', group="1"),
        Rat('3', group="1"),
        Rat('4', group="1"),
        Rat('5', group="1")
    ],
    ignore_sessions=['!2016-01-07', '!2016-01-09'] + counterconditioning_sessions + test_session
)

colours = {'baseline, ': '#252525',
           'light, rewarded': '#1f77b4',
           'light, unrewarded': '#aec7e8',
           'sound, rewarded': '#2ca02c',
           'sound, unrewarded': '#98df8a',
           }

equalratio_sessions = [val for val in range(1, 33)]
unequalsameiti_sessions = [val for val in range(1, 43)]
shortiti_sessions = [val for val in range(43, 53)]
# test_session = [53]


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue,
                "trial_type": trial,
                "rewarded": "rewarded" if trial[-1] == "1" else "unrewarded",
                "cue": cue,
            }
            trial = data[trial]
            cue = data[cue]
            session.add_epoch_data(rat.rat_id, trial.intersect(cue), meta, n_missing)
        else:
            meta = {
                "cue_type": cue,
                "trial_type": "",
                "rewarded": "",
                "cue": cue,
            }
            session.add_epoch_data(rat.rat_id, data[cue], meta, n_missing)

    if session.number in equalratio_sessions:
        print("equalratio")
        add_data("sound", "trial1", n_missing=8)
        add_data("sound", "trial2", n_missing=40)
        add_data("light", "trial2", n_missing=40)
        add_data("baseline", n_missing=48)
    elif session.number in unequalsameiti_sessions:
        print("unequalsameiti")
        add_data("sound", "trial1", n_missing=12)
        add_data("sound", "trial2", n_missing=36)
        add_data("light", "trial2", n_missing=36)
        add_data("baseline", n_missing=48)
    elif session.number in shortiti_sessions:
        print("shortiti")
        add_data("sound", "trial1")
        add_data("sound", "trial2")
        add_data("light", "trial2")
        add_data("baseline")
    elif rat.rat_id == "5" and session.number in test_session:
        print("testsession-rat5")
        add_data("sound", "trial1", n_missing=16)
        add_data("sound", "trial2", n_missing=48)
        add_data("light", "trial2", n_missing=48)
        add_data("baseline", n_missing=64)
    elif rat.rat_id != "5" and session.number in test_session:
        print("testsession")
        add_data("sound", "trial1")
        add_data("sound", "trial2")
        add_data("light", "trial2")
        add_data("baseline")
    else:
        raise ValueError("session %s is undefined. Please specify whether it has any missing trials." % session.number)

change = [16.5, 32.5, 42.5, 52.5]
expt.add_datapoints = add_datapoints
expt.plot_all(cached_data=cached_data, change=change, colours=colours)
expt.plot_all(measure="Duration", cached_data=cached_data, change=change, colours=colours)
expt.plot_all(measure="Count", cached_data=cached_data, change=change, colours=colours)
