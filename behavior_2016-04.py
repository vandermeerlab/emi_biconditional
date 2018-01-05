import measurements as m
from core import Experiment, Rat, TrialEpoch

cached_data = True

# rats = ["R099", "R095", "R088", "R094", "R098", "R096", "R101", "R090"]
# TODO: fix plot to reflect missing data from session 2 (2016-04-06)

counterconditioning_sessions = ['!2016-04-25', '!2016-04-26', '!2016-04-27', '!2016-04-28', '!2016-04-29']

expt = Experiment(
    name="201604",
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
        Rat('5', group="1"),
        Rat('6', group="1"),
        Rat('7', group="1"),
        Rat('8', group="1"),
    ],
    ignore_sessions=counterconditioning_sessions,
)

colours = {'baseline, ': '#252525',
           'light, rewarded': '#1f77b4',
           'light, unrewarded': '#aec7e8',
           'sound, rewarded': '#2ca02c',
           'sound, unrewarded': '#98df8a',
           }


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue,
                "trial_type": trial,
                "rewarded": "rewarded" if trial[-1] == "1" else "unrewarded",
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

    add_data("sound", "trial1")
    add_data("sound", "trial2")
    add_data("light", "trial2")
    add_data("baseline")


change = [19.5]
expt.add_datapoints = add_datapoints
expt.plot_all(cached_data=cached_data, change=change, colours=colours)
expt.plot_all(measure="Duration", cached_data=cached_data, change=change, colours=colours)
expt.plot_all(measure="Count", cached_data=cached_data, change=change, colours=colours)
