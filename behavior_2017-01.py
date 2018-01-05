import measurements as m
from core import Experiment, Rat, TrialEpoch

cached_data = True

expt = Experiment(
    name="201701",
    cache_key="epoch",
    plot_key="",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R114', group="1", gender="male"),
        Rat('R116', group="1", gender="male"),
        Rat('R117', group="2", gender="male"),
        Rat('R118', group="1", gender="male"),
        Rat('R119', group="2", gender="male"),
        Rat('R120', group="1", gender="male"),
        Rat('R121', group="2", gender="male"),
    ],
    ignore_sessions=['!2017-01-17'],
)

colours = {'baseline, ': '#252525',
           'light, rewarded': '#1f77b4',
           'light1, rewarded': '#1f77b4',
           'light2, rewarded': '#1f77b4',
           'light, unrewarded': '#aec7e8',
           'light1, unrewarded': '#aec7e8',
           'light2, unrewarded': '#aec7e8',
           'sound, rewarded': '#2ca02c',
           'sound, unrewarded': '#98df8a',
           'sound1, rewarded': '#2ca02c',
           'sound1, unrewarded': '#98df8a',
           'sound2, rewarded': '#e377c2',
           'sound2, unrewarded': '#f7b6d2',
           }


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:-1],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial[-1] in ("2", "4") else "unrewarded",
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

    if rat.group == "1":
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
        add_data("light2", "trial1")
        add_data("sound2", "trial1")
        add_data("light2", "trial2")
        add_data("sound1", "trial2")
        add_data("light1", "trial3")
        add_data("sound1", "trial3")
        add_data("light1", "trial4")
        add_data("sound2", "trial4")
        add_data("baseline")

expt.add_datapoints = add_datapoints
expt.plot_all(cached_data=cached_data, colours=colours)
