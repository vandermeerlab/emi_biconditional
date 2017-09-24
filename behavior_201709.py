import os
import measurements as m
from core import Experiment, Rat, TrialEpoch
from plotting import plot_overtime


epoch_expt = Experiment(
    name="201709",
    cache_key="epoch",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
        TrialEpoch("light1start", start_idx=4, duration=10),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2start", start_idx=6, duration=10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1"),
        Rat('R156', group="2"),
        Rat('R157', group="2"),
        Rat('R158', group="1"),
        Rat('R159', group="2"),
        Rat('R160', group="1"),
        Rat('R161', group="1"),
        Rat('R162', group="2"),
    ],
    magazine_session='!2017-09-20',
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

    if rat.group == "1":
        add_data("light1start", "trial1")
        add_data("light1end", "trial1")
        add_data("sound1", "trial1")
        add_data("light2start", "trial2")
        add_data("light2end", "trial2")
        add_data("sound1", "trial2")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2start", "trial1")
        add_data("light2end", "trial1")
        add_data("sound1", "trial1")
        add_data("light1start", "trial2")
        add_data("light1end", "trial2")
        add_data("sound1", "trial2")
        add_data("baseline")


epoch_expt.add_datapoints = add_datapoints


binned_expt = Experiment(
    name="201709",
    cache_key="binned",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
    ],
    measurements=[m.Duration()],
    rats=[
        Rat('R155', group="1"),
        Rat('R156', group="2"),
        Rat('R157', group="2"),
        Rat('R158', group="1"),
        Rat('R159', group="2"),
        Rat('R160', group="1"),
        Rat('R161', group="1"),
        Rat('R162', group="2"),
    ],
    magazine_session='!2017-09-20',
    sessionfiles=['!2017-09-23',
                  '!2017-09-24']
)


def add_datapoints(session, data, rat):
    session.add_binned_data(rat.rat_id, data["light1"], binsize=5, info={'cue': 'light1'})
    session.add_binned_data(rat.rat_id, data["light2"], binsize=5, info={'cue': 'light2'})

binned_expt.add_datapoints = add_datapoints
binned_df = binned_expt.analyze()
binned_df = binned_df.drop(binned_df.loc[(binned_df.duration == 155) &
                                         (binned_df.time_start == 150)].index)
binned_df = binned_df.drop(binned_df.loc[(binned_df.duration == 185) &
                                         (binned_df.time_start == 180)].index)
binned_df = binned_df.drop(binned_df.loc[(binned_df.duration == 215) &
                                         (binned_df.time_start == 210)].index)
binned_df = binned_df.drop(binned_df.loc[(binned_df.duration == 245) &
                                         (binned_df.time_start == 240)].index)
binned_df = binned_df.drop(binned_df.loc[(binned_df.duration == 275) &
                                         (binned_df.time_start == 270)].index)

binned_df.loc[binned_df.duration == 155, 'duration'] = 150
binned_df.loc[binned_df.duration == 185, 'duration'] = 180
binned_df.loc[binned_df.duration == 215, 'duration'] = 210
binned_df.loc[binned_df.duration == 245, 'duration'] = 240
binned_df.loc[binned_df.duration == 275, 'duration'] = 270

group1 = [rat for rat in binned_expt.rats if rat.group == "1"]
filepath = os.path.join(binned_expt.plot_dir, 'group1_binned.png')
plot_overtime(binned_df, rats=group1, filepath=filepath)

group2 = [rat for rat in binned_expt.rats if rat.group == "2"]
filepath = os.path.join(binned_expt.plot_dir, 'group2_binned.png')
plot_overtime(binned_df, rats=group2, filepath=filepath)

filepath = os.path.join(binned_expt.plot_dir, 'all-rats_binned.png')
plot_overtime(binned_df, rats=binned_expt.rats, filepath=filepath)

epoch_expt.plot_all(measure="Duration")
epoch_expt.plot_all()
