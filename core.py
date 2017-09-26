import os

import nept
import numpy as np
import pandas as pd

from load_data import assign_label
from plotting import mkdirs, plot_behavior

thisdir = os.path.dirname(os.path.realpath(__file__))


class Experiment:

    def __init__(self, name, cache_key, trial_epochs, measurements, rats, magazine_session,
                 sessionfiles=None, add_datapoints=None):
        self.name = name
        self.cache_key = cache_key
        self.trial_epochs = trial_epochs
        self.measurements = measurements
        self.rats = rats
        self.magazine_session = magazine_session
        self.add_datapoints = add_datapoints

        if sessionfiles is None:
            self.sessionfiles = []
            for filename in sorted(os.listdir(self.data_dir)):
                if filename != self.magazine_session and filename[0] == '!':
                    self.sessionfiles.append(filename)
        else:
            self.sessionfiles = sessionfiles

        self.df = None

        mkdirs(self.cache_dir)
        mkdirs(self.plot_dir)

    @property
    def cache_dir(self):
        return os.path.join(thisdir, 'cache', 'cache', self.name + '-' + self.cache_key)

    @property
    def data_dir(self):
        return os.path.join(thisdir, 'cache', 'data', self.name)

    @property
    def plot_dir(self):
        return os.path.join(thisdir, 'plots', self.name)

    def analyze(self):
        if self.df is not None:
            return

        sessions = []
        for i, filename in enumerate(self.sessionfiles):
            cachefile = os.path.join(self.cache_dir, "%s.pkl" % (filename,))
            if os.path.exists(cachefile):
                print("Loading %s from cache" % (filename,))
                sessions.append(pd.read_pickle(cachefile))
                continue

            session_data = nept.load_medpc(os.path.join(self.data_dir, filename),
                                           assign_label(self.trial_epochs))
            session = Session(i+1, self.measurements)

            for rat in self.rats:
                rat_data = session_data[rat.rat_id]
                session.add_rat(rat.rat_id, rat_data["mags"])
                self.add_datapoints(session, rat_data, rat)
                session.check(rat.rat_id, rat_data)

            sessions.append(session.to_df())
            print("Saving %s to cache" % (filename,))
            session.save(cachefile)

        self.df = pd.concat(sessions, ignore_index=True)
        return self.df

    def plot_all(self, change=None, measure=None):
        self.analyze()
        for rat in self.rats:
            self.plot_rat(rat, change=change, measure=measure, by_outcome=True)

        self.plot_group(self.rats, label="all-rats", change=change, measure=measure, by_outcome=True)
        self.plot_group(self.rats, label="all-rats", change=change, measure=measure, by_outcome=False)

        group1 = [rat for rat in self.rats if rat.group == "1"]
        self.plot_group(group1, label="group1", change=change, measure=measure, by_outcome=True)

        group2 = [rat for rat in self.rats if rat.group == "2"]
        self.plot_group(group2, label="group2", change=change, measure=measure, by_outcome=True)

    def plot_rat(self, rat, by_outcome=True, measure=None, change=None):
        self.analyze()

        filename = "%s_%s%s.png" % (
            rat.rat_id,
            "behavior" if measure is None else measure.lower(),
            "_outcome" if by_outcome else "")
        filepath = os.path.join(self.plot_dir, filename)
        plot_behavior(self.df, [rat], filepath, by_outcome=by_outcome,
                      measure=measure, change_sessions=change)

    def plot_group(self, rats, label, by_outcome=True, measure=None, change=None):
        self.analyze()

        filepath = os.path.join(self.plot_dir, "%s_%s%s.png" % (
            label,
            "behavior" if measure is None else measure.lower(),
            "_outcome" if by_outcome else ""))
        plot_behavior(self.df, rats, filepath, by_outcome=by_outcome, measure=measure, change_sessions=change)

    def plot_feature(self, rat):
        pass


class Session:
    def __init__(self, number, measurements):
        self.number = number
        self.measurements = measurements
        self.epochs_of_interest = {}
        self.data = []
        self._df = None

    def add_rat(self, rat_id, epoch_of_interest):
        self._df = None
        self.epochs_of_interest[rat_id] = epoch_of_interest

    def add_epoch_data(self, rat_id, epoch, info=None):
        self._df = None
        for measurement in self.measurements:
            self.data.append(EpochDataPoint(
                session_number=self.number,
                rat_id=rat_id,
                values=measurement(epoch, self.epochs_of_interest[rat_id]),
                measure=measurement.label,
                info=info,
            ))

    def add_binned_data(self, rat_id, epoch, binsize, info=None):
        self._df = None

        for trial, ep in enumerate(epoch):
            starts = np.arange(ep.start, ep.stop, binsize)
            binned_ep = nept.Epoch(starts, duration=np.ones(len(starts))*binsize)

            for measurement in self.measurements:
                self.data.append(BinnedDataPoint(
                    session_number=self.number,
                    trial_number=trial+1,
                    rat_id=rat_id,
                    values=measurement(binned_ep, self.epochs_of_interest[rat_id]),
                    measure=measurement.label,
                    binsize=binsize,
                    info=info,
                ))

    def check(self, rat_id, rat_data):
        print(rat_id, "session:", self.number)
        for key in rat_data:
            print(key, str(rat_data[key].n_epochs))

    def save(self, path):
        self.to_df().to_pickle(path)

    def to_df(self):
        # TODO: check that all datapoints are of the same type
        if self._df is None:
            self._df = pd.concat([dp.to_df() for dp in self.data], ignore_index=True)
        return self._df


    # def add_missing_trial(self, cue, trial_type):
    #     """Adds trial placeholders for missing trials.
    #
    #     Parameters
    #     ----------
    #     cue: str
    #         Typically either 'light' or 'sound'
    #     trial_type: int
    #         Typically 1, 2, 3, or 4
    #     """
    #     self.trials.append(
    #         Trial(cue=cue,
    #               trial_type=trial_type,
    #               durations=np.nan,
    #               numbers=np.nan,
    #               latency=np.nan,
    #               responses=np.nan))


class EpochDataPoint:
    def __init__(self, session_number, rat_id, values, measure, info):
        self.session_number = session_number
        self.rat_id = rat_id
        self.values = values
        self.measure = measure
        self.info = info

    def to_df(self):
        data = self.info.copy()
        data.update({
            "session": self.session_number,
            "rat": self.rat_id,
            "value": self.values,
            "trial": np.arange(len(self.values))+1,
            "measure": self.measure,
        })
        return pd.DataFrame(data)


class BinnedDataPoint:
    def __init__(self, session_number, trial_number, rat_id, values, measure, binsize, info):
        self.session_number = session_number
        self.trial_number = trial_number
        self.rat_id = rat_id
        self.values = values
        self.measure = measure
        self.binsize = binsize
        self.info = info

    def to_df(self):
        data = self.info.copy()
        data.update({
            "session": self.session_number,
            "trial": self.trial_number,
            "rat": self.rat_id,
            "value": self.values,
            "measure": self.measure,
            "time_start": np.arange(len(self.values)) * self.binsize,
            "duration": len(self.values) * self.binsize,
        })
        return pd.DataFrame(data)


class TrialEpoch:
    def __init__(self, name, start_idx, stop_idx=None, duration=None, min_duration=0.027):
        assert stop_idx is not None or duration is not None, "Must specify one"
        assert stop_idx is None or duration is None, "Cannot specify both"

        self.name = name
        self.start_idx = start_idx
        self.stop_idx = stop_idx
        self.duration = duration
        self.min_duration = min_duration

        #TODO: modify to allow for buffer before and after epoch

    def load(self, data):
        start = np.array(data[self.start_idx])

        if self.stop_idx is not None:
            stop = np.array(data[self.stop_idx])
        else:
            stop = start + self.duration

        if self.duration is not None and self.duration < 0:
            start, stop = stop, start

        if len(start) > len(stop):
            start = start[:-1]
        epoch = nept.Epoch(start, stop-start)
        return epoch[epoch.durations > self.min_duration]


class Rat:
    def __init__(self, rat_id, group):
        self.rat_id = rat_id
        self.group = group

#
# def fix_missing_trials(df):
#     """Replaces nan values with mean for that trial type
#
#     Parameters
#     ----------
#     df: pd.DataFrame
#
#     Note: this is a hack to handle sessions where there were fewer trials than expected.
#     This function finds those trials and replaces the values with the mean for that
#     trial type across the session.
#
#     """
#     nan_idx = np.where(np.isnan(df['value']))[0]
#     for idx in nan_idx:
#         row = df.loc[idx]
#         value = df.loc[(df['rat'] == row['rat']) &
#                        (df['session'] == row['session']) &
#                        (df['condition'] == row['condition']) &
#                        (df['measure'] == row['measure'])].mean()['value']
#
#         df.set_value(idx, 'value', value)
