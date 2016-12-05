import numpy as np
import vdmlab as vdm
import pandas as pd
from broken_session import fix_missing_trials


def assign_label(data):
    """Assigns events to proper labels.

    Parameters
    ----------
    data: dict

    Returns
    -------
    rats_data: dict
        With mags, pellets, lights1, lights2, sounds1, sounds2, trial1, trial2, trial3, trial4 as keys.
        Each contains vdmlab.Epoch objects

    """
    mag_start = np.array(data[1])
    mag_end = np.array(data[2])
    if len(mag_start) > len(mag_end):
        mag_start = np.array(data[1][:-1])
    pel_start = np.array(data[3])
    pel_end = pel_start + 1
    light1_start = np.array(data[4])
    light1_end = np.array(data[5])
    light2_start = np.array(data[6])
    light2_end = np.array(data[7])
    sound1_start = np.array(data[8])
    sound1_end = np.array(data[9])
    sound2_start = np.array(data[10])
    sound2_end = np.array(data[11])
#     trial1_start = np.array(data[12])
#     trial1_end = np.array(data[13])
#     trial2_start = np.array(data[14])
#     trial2_end = np.array(data[15])
#     trial3_start = np.array(data[16])
#     trial3_end = np.array(data[17])
#     trial4_start = np.array(data[18])
#     trial4_end = np.array(data[19])

    rats_data = {}
    rats_data['mags'] = vdm.Epoch(mag_start, mag_end-mag_start)
    rats_data['pellets'] = vdm.Epoch(pel_start, pel_end-pel_start)
    rats_data['lights1'] = vdm.Epoch(light1_start, light1_end-light1_start)
    rats_data['lights2'] = vdm.Epoch(light2_start, light2_end-light2_start)
    rats_data['sounds1'] = vdm.Epoch(sound1_start, sound1_end-sound1_start)
    rats_data['sounds2'] = vdm.Epoch(sound2_start, sound2_end-sound2_start)
#     rats_data['trial1'] = vdm.Epoch(trial1_start, trial1_end-trial1_start)
#     rats_data['trial2'] = vdm.Epoch(trial2_start, trial2_end-trial2_start)
#     rats_data['trial3'] = vdm.Epoch(trial3_start, trial3_end-trial3_start)
#     rats_data['trial4'] = vdm.Epoch(trial4_start, trial4_end-trial4_start)

    return rats_data


def vdm_assign_label(events):
    """Assigns events to proper labels.

    Parameters
    ----------
    events: dict

    Returns
    -------
    rats_data: dict
        With mags, pellets, lights1, lights2, sounds1, sounds2 as keys.
        Each contains vdmlab.Epoch objects

    """
    mag_start = events['pb_on']
    mag_end = events['pb_off']
    if len(mag_start) > len(mag_end):
        mag_start = np.array(events['pb_on'][:-1])
    pel_start = events['feeder']
    pel_end = pel_start + 1
    light1_start = events['cue_on']
    light1_end = events['cue_off']
    light2_start = events['house_on']
    light2_end = events['house_off']
    sound1_start = events['tone_on']
    sound1_end = events['tone_off']
    sound2_start = events['noise_on']
    sound2_end = events['noise_off']

    rats_data = {}
    rats_data['mags'] = vdm.Epoch(mag_start, mag_end-mag_start)
    rats_data['pellets'] = vdm.Epoch(pel_start, pel_end-pel_start)
    rats_data['lights1'] = vdm.Epoch(light1_start, light1_end-light1_start)
    rats_data['lights2'] = vdm.Epoch(light2_start, light2_end-light2_start)
    rats_data['sounds1'] = vdm.Epoch(sound1_start, sound1_end-sound1_start)
    rats_data['sounds2'] = vdm.Epoch(sound2_start, sound2_end-sound2_start)

    return rats_data


class Session:
    def __init__(self, mags, pellets):
        self.mags = mags
        self.pellets = pellets
        self.trials = []

    def add_trial(self, epoch, cue, trial_type):
        cue_mag = epoch.intersect(self.mags)

        self.trials.append(
            Trial(cue=cue,
                  trial_type=trial_type,
                  durations=np.sum(cue_mag.durations),
                  numbers=cue_mag.n_epochs,
                  latency=cue_mag.start - epoch.start if cue_mag.n_epochs > 0 else 10.0,
                  responses=1 if cue_mag.n_epochs > 0 else 0))

    def add_missing_trial(self, cue, trial_type):
        self.trials.append(
            Trial(cue=cue,
                  trial_type=trial_type,
                  durations=np.nan,
                  numbers=np.nan,
                  latency=np.nan,
                  responses=np.nan))


class Trial:
    def __init__(self, cue, trial_type, durations, numbers, latency, responses):
        self.cue = cue
        self.trial_type = trial_type
        self.durations = durations
        self.numbers = numbers
        self.latency = latency
        self.responses = responses


class Rat:
    group1 = ['1', '3', '5', '7']
    group2 = ['2', '4', '6', '8']

    def __init__(self, rat_id):
        self.rat_id = rat_id
        self.sessions = []

        self.sound_trials = {1: 'sounds2',
                             2: 'sounds1',
                             3: 'sounds1',
                             4: 'sounds2'}

        if rat_id in Rat.group1:
            self.light_trials = {1: 'lights1',
                                 2: 'lights1',
                                 3: 'lights2',
                                 4: 'lights2'}
        elif rat_id in Rat.group2:
            self.light_trials = {1: 'lights2',
                                 2: 'lights2',
                                 3: 'lights1',
                                 4: 'lights1'}
        else:
            raise ValueError("rat id is incorrect. Should be one of 1-8")

    def add_session(self, mags, pellets, lights1, lights2, sounds1, sounds2, n_unique=8, delay=5.02, tolerance=1e-08):
        session = Session(mags, pellets)

        for trial in [1, 2, 3, 4]:
            if self.light_trials[trial] == 'lights1':
                light_cues = lights1
            elif self.light_trials[trial] == 'lights2':
                light_cues = lights2
            if self.sound_trials[trial] == 'sounds1':
                sound_cues = sounds1
            elif self.sound_trials[trial] == 'sounds2':
                sound_cues = sounds2

            n_trials = 0
            for light in light_cues:
                for sound in sound_cues:
                    if np.allclose(sound.start - light.stop, delay, atol=tolerance):
                        session.add_trial(light, 'light', trial)
                        session.add_trial(sound, 'sound', trial)
                        n_trials += 1

            for _ in range(n_unique - n_trials):
                session.add_missing_trial('light', trial)
                session.add_missing_trial('sound', trial)

        self.sessions.append(session)


def f_analyze(trial, measure):
    if measure == 'durations':
        output = trial.durations
    if measure == 'numbers':
        output = trial.numbers
    if measure == 'latency':
        output = trial.latency
    if measure == 'responses':
        output = trial.responses * 100.

    return output


def combine_rats(data, rats, n_sessions, only_sound=False):
    """Combines behavioral measures from multiple rats, sessions and trials.

    data: dict
        With rat (str) as key, contains Rat objects for each rat
    rats: list
        With rat_id (str)
    n_sessions: int
    only_sound: boolean

    Returns
    -------
    df: pd.DataFrame

    """
    measures = ['durations', 'numbers', 'latency', 'responses']
    together = dict(trial=[], rat=[], session=[], trial_type=[], rewarded=[],
                    cue=[], value=[], measure=[], condition=[])

    for session in range(n_sessions):
        for rat in rats:
            for i, trial in enumerate(data[rat].sessions[session].trials):
                for measure in measures:
                    if not only_sound or trial.cue == 'sound':
                        together['trial'].append("%s, %d" % (rat, i))
                        together['rat'].append(rat)
                        together['session'].append(session+1)
                        together['trial_type'].append(trial.trial_type)
                        together['rewarded'].append("%s %s" %
                                                    (trial.cue, 'rewarded' if trial.trial_type % 2 == 0 else 'unrewarded'))
                        together['cue'].append(trial.cue)
                        together['condition'].append("%s %d" % (trial.cue, trial.trial_type))
                        together['measure'].append(measure)
                        together['value'].append(f_analyze(trial, measure))

    df = pd.DataFrame(data=together)

    fix_missing_trials(df)

    return df
