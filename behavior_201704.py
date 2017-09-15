import measurements as m
from core import Experiment, Rat, TrialEpoch


expt = Experiment(
    name="201704",
    cache_key="epoch",
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
        Rat('R141', group="1"),
        Rat('R142', group="2"),
        Rat('R143', group="2"),
        Rat('R144', group="1"),
        Rat('R145', group="2"),
        Rat('R146', group="1"),
        Rat('R147', group="1"),
        Rat('R148', group="2"),
    ],
    magazine_session='!2017-04-14',
)


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
# expt.plot_all(change=[11, 21, 46])
expt.plot_all()
