import numpy as np
import measurements as m
from core import Experiment, Rat, TrialEpoch

cached_data = True

expt = Experiment(
    name="201704",
    cache_key="epoch",
    plot_key="",
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
        Rat('R141', group="1", gender="male"),
        Rat('R142', group="2", gender="female"),
        Rat('R143', group="2", gender="male"),
        Rat('R144', group="1", gender="female"),
        Rat('R145', group="2", gender="male"),
        Rat('R146', group="1", gender="female"),
        Rat('R147', group="1", gender="male"),
        Rat('R148', group="2", gender="female"),
    ],
    ignore_sessions=['!2017-04-14'],
)

short_sessions = [val for val in np.arange(20) + 1]

colours = {'baseline, ': '#252525',
           'light, rewarded': '#1f77b4',
           'light, unrewarded': '#aec7e8',
           'light1, rewarded': '#1f77b4',
           'light1, unrewarded': '#aec7e8',
           'light2, rewarded': '#1f77b4',
           'light2, unrewarded': '#aec7e8',
           'sound, rewarded': '#2ca02c',
           'sound, unrewarded': '#98df8a',
           'sound1, rewarded': '#2ca02c',
           'sound1, unrewarded': '#98df8a',
           'sound2, rewarded': '#e377c2',
           'sound2, unrewarded': '#f7b6d2'
           }


def add_datapoints(session, data, rat):
    print(session)

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue[:-1],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial[-1] in ("2", "4") else "unrewarded",
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

    if rat.group == "1":
        if session.number in short_sessions:
            add_data("light1", "trial1", n_missing=8)
            add_data("sound2", "trial1", n_missing=8)
            add_data("light1", "trial2", n_missing=8)
            add_data("sound1", "trial2", n_missing=8)
            add_data("light2", "trial3", n_missing=8)
            add_data("sound1", "trial3", n_missing=8)
            add_data("light2", "trial4", n_missing=8)
            add_data("sound2", "trial4", n_missing=8)
            add_data("baseline", n_missing=32)
        else:
            add_data("light1", "trial1")
            add_data("sound2", "trial1")
            add_data("light1", "trial2")
            add_data("sound1", "trial2")
            add_data("light2", "trial3")
            add_data("sound1", "trial3")
            add_data("light2", "trial4")
            add_data("sound2", "trial4")
            add_data("baseline")

    elif rat.group == "2":
        if session.number in short_sessions:
            add_data("light2", "trial1", n_missing=8)
            add_data("sound2", "trial1", n_missing=8)
        elif rat.rat_id == "R148" and session.number == 25:  # "!2017-05-09"
            add_data("light2", "trial1", n_missing=1)
            add_data("sound2", "trial1", n_missing=1)
        else:
            add_data("light2", "trial1")
            add_data("sound2", "trial1")
        if session.number in short_sessions:
            add_data("light2", "trial2", n_missing=8)
            add_data("sound1", "trial2", n_missing=8)
        elif rat.rat_id == "R148" and session.number in [24, 26]:  # "!2017-05-08", "!2017-05-10"
            add_data("light2", "trial2", n_missing=2)
            add_data("sound1", "trial2", n_missing=2)
        elif rat.rat_id == "R148" and session.number == 28:  # "!2017-05-12"
            add_data("light2", "trial2", n_missing=1)
            add_data("sound1", "trial2", n_missing=1)
        else:
            add_data("light2", "trial2")
            add_data("sound1", "trial2")
        if session.number in short_sessions:
            add_data("light1", "trial3", n_missing=8)
            add_data("sound1", "trial3", n_missing=8)
        elif rat.rat_id == "R148" and session.number == 24:  # "!2017-05-08"
            add_data("light1", "trial3", n_missing=1)
            add_data("sound1", "trial3", n_missing=1)
        elif rat.rat_id == "R148" and session.number == 26:  # "!2017-05-10"
            add_data("light1", "trial3", n_missing=2)
            add_data("sound1", "trial3", n_missing=2)
        else:
            add_data("light1", "trial3")
            add_data("sound1", "trial3")
        if session.number in short_sessions:
            add_data("light1", "trial4", n_missing=8)
            add_data("sound2", "trial4", n_missing=8)
        else:
            add_data("light1", "trial4")
            add_data("sound2", "trial4")
        if session.number in short_sessions:
            add_data("baseline", n_missing=32)
        elif rat.rat_id == "R148" and session.number == 24:  # "!2017-05-08"
            add_data("baseline", n_missing=2)
        elif rat.rat_id == "R148" and session.number == 26:  # "!2017-05-10"
            add_data("baseline", n_missing=4)
        else:
            add_data("baseline")

expt.add_datapoints = add_datapoints
expt.analyze(cached_data=cached_data)

change = [10.5, 20.5, 45.5]

expt.plot_all(cached_data=cached_data, measure="Duration", colours=colours, change=change, filetype="svg")
expt.plot_all(cached_data=cached_data, colours=colours, change=change)
