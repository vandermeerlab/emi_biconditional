import os
import numpy as np
import measurements as m
from core import Experiment, Rat, TrialEpoch
from plotting import plot_overtime

cached_data = False

plot_occset = False
plot_counterconditioning = False
plot_biconditional = False
plot_altoccset = False
plot_jointoccset = True

magazine_session = ['!2017-09-20']
occset_tone = ["!2017-09-%02d"
               % date for date in np.arange(21, 31, 1)
               ] + ["!2017-10-%02d"
                    % date for date in np.arange(1, 7, 1)
                    ] + ["!2017-10-%02d"
                         % date for date in np.arange(21, 32, 1)
                         ] + ["!2017-11-%02d"
                              % date for date in np.arange(1, 5, 1)
                              ] + ["!2017-11-%02d"
                                   % date for date in np.arange(21, 31, 1)
                                   ]
counterconditioning_sessions = ["!2017-10-%02d" % date for date in np.arange(7, 20, 1)]
biconditional_sessions = ["!2017-11-%02d" % date for date in np.arange(5, 21, 1)]
tone_only_sessions = ["!2017-12-02", "!2017-12-04", "!2017-12-06", "!2017-12-09", "!2017-12-11a",
                      "!2017-12-12b", "!2017-12-13a", "!2017-12-14b", "!2017-12-17", "!2017-12-18a"]
noise_only_sessions = ["!2017-12-01", "!2017-12-03", "!2017-12-05", "!2017-12-07", "!2017-12-10",
                       "!2017-12-11b", "!2017-12-12a", "!2017-12-13b", "!2017-12-14a", "!2017-12-15a",
                       "!2017-12-15b", "!2017-12-16", "!2017-12-18b", "!2017-12-19a", "!2017-12-19b"]
jointoccset_sessions = ["!2017-12-20a", "!2017-12-20b", "!2017-12-21a", "!2017-12-21b", "!2017-12-22a",
                        "!2017-12-22b", "!2017-12-23a", "!2017-12-23b", "!2017-12-24a", "!2017-12-24b",
                        "!2017-12-26a", "!2017-12-26b", "!2017-12-27a", "!2017-12-27b", "!2017-12-28a",
                        "!2017-12-28b"]

# Occasion setting
epoch_expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="occset",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + biconditional_sessions + noise_only_sessions,
    sessionfiles=occset_tone
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" else "unrewarded",
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

    if session.number > 42:
        if rat.group == "1":
            add_data("light1end", "trial1", n_missing=1)
            add_data("light2end", "trial2", n_missing=1)
            add_data("sound1", "trial1", n_missing=1)
            add_data("sound1", "trial2", n_missing=1)
            add_data("baseline", n_missing=2)

        elif rat.group == "2":
            add_data("light2end", "trial1", n_missing=1)
            add_data("light1end", "trial2", n_missing=1)
            add_data("sound1", "trial1", n_missing=1)
            add_data("sound1", "trial2", n_missing=1)
            add_data("baseline", n_missing=2)
    else:
        if rat.group == "1":
            add_data("light1end", "trial1")
            add_data("light2end", "trial2")
            add_data("sound1", "trial1")
            add_data("sound1", "trial2")
            add_data("baseline")

        elif rat.group == "2":
            add_data("light2end", "trial1")
            add_data("light1end", "trial2")
            add_data("sound1", "trial1")
            add_data("sound1", "trial2")
            add_data("baseline")

binned_expt = Experiment(
    name="201709",
    cache_key="binned",
    plot_key="occset",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("prelight1", start_idx=4, duration=-20),
        TrialEpoch("prelight2", start_idx=6, duration=-20),
    ],
    measurements=[m.Duration(), m.Count()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + biconditional_sessions + noise_only_sessions,
    sessionfiles=occset_tone
)

conditioning_colours = {'baseline, ': '#252525',
                        'light, rewarded': '#1f77b4',
                        'light1end, rewarded': '#1f77b4',
                        'light2end, rewarded': '#1f77b4',
                        'light, unrewarded': '#aec7e8',
                        'light1end, unrewarded': '#aec7e8',
                        'light2end, unrewarded': '#aec7e8',
                        'sound, rewarded': '#2ca02c',
                        'sound, unrewarded': '#98df8a',
                        'sound1, rewarded': '#2ca02c',
                        'sound1, unrewarded': '#98df8a'
                        }

overtime_colours = {'light1': '#9970ab',
                    'light2': '#5aae61'}


if plot_occset:
    epoch_expt.add_datapoints = add_datapoints


    def add_datapoints(session, data, rat):
        session.add_binned_data(rat.rat_id, data["light1"], binsize=5, info={'cue': 'light1'})
        session.add_binned_data(rat.rat_id, data["light2"], binsize=5, info={'cue': 'light2'})

    binned_expt.add_datapoints = add_datapoints
    binned_df = binned_expt.analyze(cached_data=cached_data)
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

    for measure in ["Duration", "Count"]:
        if measure == "Duration":
            labels = "Duration in food cup (s)"
        elif measure == "Count":
            labels = "Number of entries"
        group1 = [rat for rat in binned_expt.rats if rat.group == "1"]
        filepath = os.path.join(binned_expt.plot_dir, 'group1_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=group1, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        group2 = [rat for rat in binned_expt.rats if rat.group == "2"]
        filepath = os.path.join(binned_expt.plot_dir, 'group2_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=group2, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        filepath = os.path.join(binned_expt.plot_dir, 'all-rats_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=binned_expt.rats, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        for rat in binned_expt.rats:
            filepath = os.path.join(binned_expt.plot_dir, rat.rat_id + '_' +
                                    measure.lower() + '_binned.png')
            plot_overtime(binned_df, rats=[rat], filepath=filepath, measure=measure,
                          labels=labels, colours=overtime_colours)

    change = [16.5, 32.5, 44]

    epoch_expt.plot_all(cached_data=cached_data, measure="Count", labels=["Number of entries"],
                        colours=conditioning_colours, change=change)
    epoch_expt.plot_all(cached_data=cached_data, measure="Duration", labels=["Duration in food cup (s)"],
                        colours=conditioning_colours, change=change)
    epoch_expt.plot_all(cached_data=cached_data, colours=conditioning_colours, change=change)


# Counterconditioning
epoch_expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="counterconditioning",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("pellets", start_idx=3, duration=1),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("probe1", start_idx=8, stop_idx=9),
        TrialEpoch("probe2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.DurationPerSecond(), m.CountPerSecond()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session,
    sessionfiles=counterconditioning_sessions,
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if (trial == "trial1") | (trial == "trial3") else "unrewarded",
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
        add_data("light2", "trial2")
        add_data("probe1", "trial3")
        add_data("probe2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light1", "trial2")
        add_data("light2", "trial1")
        add_data("probe1", "trial4")
        add_data("probe2", "trial3")
        add_data("baseline")

conditioning_colours = {'baseline, ': '#252525',
                        'light1, rewarded': '#1f77b4',
                        'light1, unrewarded': '#aec7e8',
                        'light2, rewarded': '#1f77b4',
                        'light2, unrewarded': '#aec7e8',
                        'probe1, rewarded': 'c',
                        'probe1, unrewarded': 'm',
                        'probe2, rewarded': 'c',
                        'probe2, unrewarded': 'm',
                        }

if plot_counterconditioning:
    epoch_expt.add_datapoints = add_datapoints
    epoch_expt.analyze(cached_data=cached_data)

    epoch_expt.plot_all(cached_data=cached_data, colours=conditioning_colours)


# Biconditional discrimination
epoch_expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="biconditional",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + tone_only_sessions + noise_only_sessions,
    sessionfiles=biconditional_sessions
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" or trial == "trial4" else "unrewarded",
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
        add_data("light1end", "trial1")
        add_data("light2end", "trial2")
        add_data("light2end", "trial3")
        add_data("light1end", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2end", "trial1")
        add_data("light1end", "trial2")
        add_data("light1end", "trial3")
        add_data("light2end", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

binned_expt = Experiment(
    name="201709",
    cache_key="binned",
    plot_key="biconditional",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("prelight1", start_idx=4, duration=-20),
        TrialEpoch("prelight2", start_idx=6, duration=-20),
    ],
    measurements=[m.Duration(), m.Count()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions,
    sessionfiles=biconditional_sessions,
)

conditioning_colours = {'baseline, ': '#252525',
                        'light, rewarded': '#1f77b4',
                        'light1end, rewarded': '#1f77b4',
                        'light2end, rewarded': '#1f77b4',
                        'light, unrewarded': '#aec7e8',
                        'light1end, unrewarded': '#aec7e8',
                        'light2end, unrewarded': '#aec7e8',
                        'sound, rewarded': '#2ca02c',
                        'sound, unrewarded': '#98df8a',
                        'sound1, rewarded': '#2ca02c',
                        'sound1, unrewarded': '#98df8a',
                        'sound2, rewarded': '#e377c2',
                        'sound2, unrewarded': '#f7b6d2'
                        }

overtime_colours = {'light1': '#9970ab',
                    'light2': '#5aae61'}

if plot_biconditional:
    epoch_expt.add_datapoints = add_datapoints


    def add_datapoints(session, data, rat):
        session.add_binned_data(rat.rat_id, data["light1"], binsize=5, info={'cue': 'light1'})
        session.add_binned_data(rat.rat_id, data["light2"], binsize=5, info={'cue': 'light2'})

    binned_expt.add_datapoints = add_datapoints
    binned_df = binned_expt.analyze(cached_data=cached_data)
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

    for measure in ["Duration", "Count"]:
        if measure == "Duration":
            labels = "Duration in food cup (s)"
        elif measure == "Count":
            labels = "Number of entries"
        group1 = [rat for rat in binned_expt.rats if rat.group == "1"]
        filepath = os.path.join(binned_expt.plot_dir, 'group1_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=group1, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        group2 = [rat for rat in binned_expt.rats if rat.group == "2"]
        filepath = os.path.join(binned_expt.plot_dir, 'group2_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=group2, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        filepath = os.path.join(binned_expt.plot_dir, 'all-rats_' +
                                measure.lower() + '_binned.png')
        plot_overtime(binned_df, rats=binned_expt.rats, filepath=filepath, measure=measure,
                      labels=labels, colours=overtime_colours)

        for rat in binned_expt.rats:
            filepath = os.path.join(binned_expt.plot_dir, rat.rat_id + '_' +
                                    measure.lower() + '_binned.png')
            plot_overtime(binned_df, rats=[rat], filepath=filepath, measure=measure,
                          labels=labels, colours=overtime_colours)

    # epoch_expt.plot_all(cached_data=cached_data, change=change, measure="Count", labels=["Number of entries"],
    #                     colours=conditioning_colours)
    # epoch_expt.plot_all(cached_data=cached_data, change=change, measure="Duration", labels=["Duration in food cup (s)"],
    #                     colours=conditioning_colours)
    # epoch_expt.plot_all(cached_data=cached_data, change=change, colours=conditioning_colours)

    epoch_expt.analyze(cached_data=cached_data)
    for rat in epoch_expt.rats:
        epoch_expt.plot_rat(rat, colours=conditioning_colours, by_outcome=False)


# Alternating occasion setting
tone_expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="altoccset_tone",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + biconditional_sessions,
    sessionfiles=tone_only_sessions
)


def add_tone_datapoints(session, data, rat):

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" or trial == "trial4" else "unrewarded",
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

    conditioning_colours = {'baseline, ': '#252525',
                            'light, rewarded': '#1f77b4',
                            'light, unrewarded': '#aec7e8',
                            'sound, rewarded': '#2ca02c',
                            'sound, unrewarded': '#98df8a'
                            }

    if rat.group == "1":
        add_data("light1end", "trial1")
        add_data("light2end", "trial2")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2end", "trial1")
        add_data("light1end", "trial2")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("baseline")

noise_expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="altoccset_noise",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + biconditional_sessions,
    sessionfiles=noise_only_sessions
)


def add_noise_datapoints(session, data, rat):

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" or trial == "trial4" else "unrewarded",
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

    conditioning_colours = {'baseline, ': '#252525',
                            'light, rewarded': '#1f77b4',
                            'light, unrewarded': '#aec7e8',
                            'sound, rewarded': '#2ca02c',
                            'sound, unrewarded': '#98df8a'
                            }

    if rat.group == "1":
        add_data("light2end", "trial3")
        add_data("light1end", "trial4")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light1end", "trial3")
        add_data("light2end", "trial4")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

if plot_altoccset:
    tone_expt.add_datapoints = add_tone_datapoints
    # tone_expt.plot_all(cached_data=cached_data, colours=conditioning_colours)
    tone_expt.analyze(cached_data=cached_data)
    for rat in tone_expt.rats:
        tone_expt.plot_rat(rat, colours=conditioning_colours, by_outcome=False)

    noise_expt.add_datapoints = add_noise_datapoints
    # noise_expt.plot_all(cached_data=cached_data, colours=conditioning_colours)
    noise_expt.analyze(cached_data=cached_data)
    for rat in noise_expt.rats:
        noise_expt.plot_rat(rat, colours=conditioning_colours, by_outcome=False)


# Joint occasion setting
expt = Experiment(
    name="201709",
    cache_key="epoch",
    plot_key="jointoccset",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("light1end", start_idx=5, duration=-10),
        TrialEpoch("light2end", start_idx=7, duration=-10),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('R155', group="1", gender="male"),
        Rat('R156', group="2", gender="female"),
        Rat('R157', group="2", gender="male"),
        Rat('R158', group="1", gender="female"),
        Rat('R159', group="2", gender="male"),
        Rat('R160', group="1", gender="female"),
        Rat('R161', group="1", gender="male"),
        Rat('R162', group="2", gender="female"),
    ],
    ignore_sessions=magazine_session + counterconditioning_sessions + biconditional_sessions,
    sessionfiles=jointoccset_sessions
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None, n_missing=0):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" or trial == "trial4" else "unrewarded",
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

    conditioning_colours = {'baseline, ': '#252525',
                            'light, rewarded': '#1f77b4',
                            'light, unrewarded': '#aec7e8',
                            'sound, rewarded': '#2ca02c',
                            'sound, unrewarded': '#98df8a'
                            }

    if rat.group == "1":
        add_data("light1end", "trial1")
        add_data("light2end", "trial2")
        add_data("light2end", "trial3")
        add_data("light1end", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2end", "trial1")
        add_data("light1end", "trial2")
        add_data("light1end", "trial3")
        add_data("light2end", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

if plot_jointoccset:
    expt.add_datapoints = add_datapoints
    # expt.plot_all(cached_data=cached_data, colours=conditioning_colours)
    expt.analyze(cached_data=cached_data)
    for rat in expt.rats:
        expt.plot_rat(rat, colours=conditioning_colours, by_outcome=False)
