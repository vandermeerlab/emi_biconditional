import numpy as np
import nept
import measurements as m
from core import Experiment, Rat, TrialEpoch

cached_data = False

for plot_extended in [True, False]:
    extended_sessions = ['!2016-12-06', '!2016-12-07a', '!2016-12-07b', '!2016-12-08', '!2016-12-09']
    extended_rats = [Rat('5', group="1"),
                     Rat("8", group="2")]
    all_rats = [
        Rat('1', group="1"),
        Rat('2', group="2"),
        Rat('3', group="1"),
        Rat('4', group="2"),
        Rat('5', group="1"),
        Rat('6', group="2"),
        Rat('7', group="1"),
        Rat('8', group="2")]
    magazine = ['!2016-10-18']
    ignore = magazine + ['!2016-10-19a1']

    expt = Experiment(
        name="201610",
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
        ],
        measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
        rats=[extended_rats if not plot_extended else all_rats][0],
        ignore_sessions=[ignore + extended_sessions if not plot_extended else ignore][0],
    )

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
               'sound2, unrewarded': '#f7b6d2',
               }


    def add_datapoints(session, data, rat):

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

        def add_data_notrials(feature, target, trial_num, delay=5.02, n_missing=0):
            feature_starts = []
            feature_stops = []
            target_starts = []
            target_stops = []
            for feature_start, feature_stop in zip(data[feature].starts, data[feature].stops):
                for target_start, target_stop in zip(data[target].starts, data[target].stops):
                    if np.allclose(target_start - feature_stop, delay):
                        meta_feature = {"cue_type": feature[:-1],
                                        "trial_type": trial_num,
                                        "rewarded": "rewarded" if trial_num in ("2", "4") else "unrewarded",
                                        "cue": feature,
                                        }
                        meta_target = {"cue_type": target[:-1],
                                       "trial_type": trial_num,
                                       "rewarded": "rewarded" if trial_num in ("2", "4") else "unrewarded",
                                       "cue": target,
                                       }
                        feature_starts = feature_starts + [feature_start]
                        feature_stops = feature_stops + [feature_stop]
                        target_starts = target_starts + [target_start]
                        target_stops = target_stops + [target_stop]
            session.add_epoch_data(rat.rat_id, nept.Epoch([feature_starts, feature_stops]), meta_feature, n_missing)
            session.add_epoch_data(rat.rat_id, nept.Epoch([target_starts, target_stops]), meta_target, n_missing)

        if session.number == 1:
            if rat.group == "1":
                add_data_notrials("light1", "sound2", trial_num="1", n_missing=1)
                add_data_notrials("light1", "sound1", trial_num="2", n_missing=2)
                add_data_notrials("light2", "sound1", trial_num="3", n_missing=2)
                add_data_notrials("light2", "sound2", trial_num="4", n_missing=1)
                add_data("baseline", n_missing=12)
            elif rat.group == "2":
                add_data_notrials("light1", "sound2", trial_num="4", n_missing=1)
                add_data_notrials("light1", "sound1", trial_num="3", n_missing=2)
                add_data_notrials("light2", "sound1", trial_num="2", n_missing=2)
                add_data_notrials("light2", "sound2", trial_num="1", n_missing=1)
                add_data("baseline", n_missing=12)
        else:
            if rat.group == "1":
                add_data_notrials("light1", "sound2", trial_num="1")
                add_data_notrials("light1", "sound1", trial_num="2")
                add_data_notrials("light2", "sound1", trial_num="3")
                add_data_notrials("light2", "sound2", trial_num="4")
                add_data("baseline")
            elif rat.group == "2":
                add_data_notrials("light1", "sound2", trial_num="4")
                add_data_notrials("light1", "sound1", trial_num="3")
                add_data_notrials("light2", "sound1", trial_num="2")
                add_data_notrials("light2", "sound2", trial_num="1")
                add_data("baseline")


    expt.add_datapoints = add_datapoints
    if plot_extended:
        change = [35.5, 46.5, 51.5]
        expt.analyze(cached_data=cached_data)
        for rat in expt.rats:
            expt.plot_rat(rat, change=change, colours=colours, by_outcome=True)
            expt.plot_rat(rat, change=change, colours=colours, by_outcome=False)
            expt.plot_rat(rat, measure="Duration", change=change, colours=colours)
            expt.plot_rat(rat, measure="Count", change=change, colours=colours)
    else:
        change = [35.5, 46.5]
        expt.plot_all(cached_data=cached_data, change=change, colours=colours)
        expt.plot_all(measure="Duration", cached_data=cached_data, change=change, colours=colours)
        expt.plot_all(measure="Count", cached_data=cached_data, change=change, colours=colours)
