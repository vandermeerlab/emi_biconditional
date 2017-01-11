import os
import numpy as np
import vdmlab as vdm

thisdir = os.path.dirname(os.path.realpath(__file__))
dataloc = os.path.abspath(os.path.join(thisdir, 'cache', 'data', 'vdmlab'))


def remove_double_inputs(on_events, off_events):
    """Removed double on and off input events.

    Parameters
    ----------
    on_events: np.array
    off_events: np.array

    Returns
    -------
    no_double_on_events: np.array
    no_double_off_events: np.array
    """

    all_events = [(on_time, 'on', i) for i, on_time in enumerate(on_events)]
    all_events += [(off_time, 'off', i) for i, off_time in enumerate(off_events)]

    sorted_events = sorted(all_events)

    double_on_idx = []
    double_off_idx = []

    for evt1, evt2 in zip(sorted_events[:-1], sorted_events[1:]):
        if evt1[1] == evt2[1] and evt1[1] == 'on':
            double_on_idx.append(evt1[2])
        if evt1[1] == evt2[1] and evt1[1] == 'off':
            double_off_idx.append(evt2[2])

    no_double_on_events = np.delete(on_events, double_on_idx)
    no_double_off_events = np.delete(off_events, double_off_idx)

    return no_double_on_events, no_double_off_events


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
    trial1_start = np.array(data[12])
    trial1_end = np.array(data[13])
    trial2_start = np.array(data[14])
    trial2_end = np.array(data[15])
    trial3_start = np.array(data[16])
    trial3_end = np.array(data[17])
    trial4_start = np.array(data[18])
    trial4_end = np.array(data[19])

    rats_data = dict()
    rats_data['mags'] = vdm.Epoch(mag_start, mag_end-mag_start)
    rats_data['pellets'] = vdm.Epoch(pel_start, pel_end-pel_start)
    rats_data['lights1'] = vdm.Epoch(light1_start, light1_end-light1_start)
    rats_data['lights2'] = vdm.Epoch(light2_start, light2_end-light2_start)
    rats_data['sounds1'] = vdm.Epoch(sound1_start, sound1_end-sound1_start)
    rats_data['sounds2'] = vdm.Epoch(sound2_start, sound2_end-sound2_start)
    rats_data['trial1'] = vdm.Epoch(trial1_start, trial1_end-trial1_start)
    rats_data['trial2'] = vdm.Epoch(trial2_start, trial2_end-trial2_start)
    rats_data['trial3'] = vdm.Epoch(trial3_start, trial3_end-trial3_start)
    rats_data['trial4'] = vdm.Epoch(trial4_start, trial4_end-trial4_start)

    return rats_data


def assign_medpc_label(data):
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

    rats_data = dict()
    rats_data['mags'] = vdm.Epoch(mag_start, mag_end-mag_start)
    rats_data['pellets'] = vdm.Epoch(pel_start, pel_end-pel_start)
    rats_data['lights1'] = vdm.Epoch(light1_start, light1_end-light1_start)
    rats_data['lights2'] = vdm.Epoch(light2_start, light2_end-light2_start)
    rats_data['sounds1'] = vdm.Epoch(sound1_start, sound1_end-sound1_start)
    rats_data['sounds2'] = vdm.Epoch(sound2_start, sound2_end-sound2_start)

    return rats_data


def vdm_assign_label(events, pellet_duration=1, trial_duration=25, cue_duration=10, min_n_trials=32, max_n_trials=32):
    """Assigns events to proper labels.

    Parameters
    ----------
    events: dict
    pellet_duration: int
        Duration of pellet delivery event.
    trial_duration: int
        Duration of trial event.
    cue_duration: int
    n_trials: int

    Returns
    -------
    rats_data: dict
        With mags, pellets, lights1, lights2, sounds1, sounds2 as keys.
        Each contains vdmlab.Epoch objects

    """
    ons = ['cue_on', 'house_on', 'tone_on', 'noise_on']
    for on in ons:
        if len(events[on]) < (min_n_trials / 2):
            raise ValueError("missing %s event(s). Only %d found" % (on, len(events[on])))
        elif len(events[on]) > (max_n_trials / 2):
            raise ValueError("too many %s events. %d found" % (on, len(events[on])))

    mag_start, mag_end = remove_double_inputs(events['pb_on'], events['pb_off'])
    pel_start = events['feeder']
    pel_end = pel_start + pellet_duration
    light1_start = events['cue_on']
    light1_end = light1_start + cue_duration
    light2_start = events['house_on']
    light2_end = light2_start + cue_duration
    sound1_start = events['tone_on']
    sound1_end = sound1_start + cue_duration
    sound2_start = events['noise_on']
    sound2_end = sound2_start + cue_duration

    trial1_start = events['trial1_start']
    trial1_end = trial1_start + trial_duration
    trial2_start = events['trial2_start']
    trial2_end = trial2_start + trial_duration
    trial3_start = events['trial3_start']
    trial3_end = trial3_start + trial_duration
    trial4_start = events['trial4_start']
    trial4_end = trial4_start + trial_duration

    rats_data = dict()
    rats_data['mags'] = vdm.Epoch(mag_start, mag_end-mag_start)
    rats_data['pellets'] = vdm.Epoch(pel_start, pel_end-pel_start)
    rats_data['lights1'] = vdm.Epoch(light1_start, light1_end-light1_start)
    rats_data['lights2'] = vdm.Epoch(light2_start, light2_end-light2_start)
    rats_data['sounds1'] = vdm.Epoch(sound1_start, sound1_end-sound1_start)
    rats_data['sounds2'] = vdm.Epoch(sound2_start, sound2_end-sound2_start)
    rats_data['trial1'] = vdm.Epoch(trial1_start, trial1_end-trial1_start)
    rats_data['trial2'] = vdm.Epoch(trial2_start, trial2_end-trial2_start)
    rats_data['trial3'] = vdm.Epoch(trial3_start, trial3_end-trial3_start)
    rats_data['trial4'] = vdm.Epoch(trial4_start, trial4_end-trial4_start)

    return rats_data


def load_biconditional_events(filename):
    """Loads biconditional events. Corrects keys labels.

    Parameters
    ----------
    filename: str

    Returns
    -------
    events: dict

    """
    cues = ['Starting Recording', 'Stopping Recording',
            'cue_on', 'cue_off', 'house_on', 'house_off',
            'tone_on', 'tone_off', 'noise_on', 'noise_off',
            'trial1_start', 'trial2_start', 'trial3_start', 'trial4_start',
            'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).',
            'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).',
            'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).']

    events = vdm.load_events(filename, cues)
    events = correct_sounds(events)

    return events


def correct_sounds(events):
    """Corrects on/off labels for sound cues.

    Parameters
    ----------
    events: dict

    Returns
    -------
    renamed_events: dict
        With appropriate keys.

    """
    renamed_events = dict()
    renamed_events['cue_on'] = events['cue_on']
    renamed_events['cue_off'] = events['cue_off']
    renamed_events['house_on'] = events['house_on']
    renamed_events['house_off'] = events['house_off']
    renamed_events['tone_on'] = events['tone_off']
    renamed_events['tone_off'] = events['tone_on']
    renamed_events['noise_on'] = events['noise_off']
    renamed_events['noise_off'] = events['noise_on']
    renamed_events['feeder'] = events['TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).']
    renamed_events['pb_on'] = events['TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).']
    renamed_events['pb_off'] = events['TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).']
    renamed_events['start_recording'] = events['Starting Recording']
    renamed_events['stop_recording'] = events['Stopping Recording']
    renamed_events['trial1_start'] = events['trial1_start']
    renamed_events['trial2_start'] = events['trial2_start']
    renamed_events['trial3_start'] = events['trial3_start']
    renamed_events['trial4_start'] = events['trial4_start']

    return renamed_events


def remove_trial_events(events, remove_trial, trial_duration=25):
    """Removes light and sound events during a given trial.

    Parameters
    -----------
    events: dict
        With trial1_start, trial2_start, trial3_start, trial4_start,
        'cue_on', 'cue_off', 'house_on', 'house_off', 'tone_on',
        'tone_off', 'noise_on', 'noise_off', each a np.array
    remove_trial: str
        'trial1', 'trial2', 'trial3', 'trial4'
    trial_duration: int
        Default set to 25 seconds

    Returns
    -------
    filtered: dict

    """

    valid_trials = ['trial1', 'trial2', 'trial3', 'trial4']

    if remove_trial not in valid_trials:
        raise ValueError("remove_trial must be one of 'trial1', 'trial2', 'trial3', 'trial4'")

    cues = ['cue_on', 'cue_off', 'house_on', 'house_off']

    trial1_start = events['trial1_start']
    trial1_stop = trial1_start + trial_duration
    trial2_start = events['trial2_start']
    trial2_stop = trial2_start + trial_duration
    trial3_start = events['trial3_start']
    trial3_stop = trial3_start + trial_duration
    trial4_start = events['trial4_start']
    trial4_stop = trial4_start + trial_duration

    rats_data = dict()
    rats_data['trial1'] = vdm.Epoch(trial1_start, trial1_stop-trial1_start)
    rats_data['trial2'] = vdm.Epoch(trial2_start, trial2_stop-trial2_start)
    rats_data['trial3'] = vdm.Epoch(trial3_start, trial3_stop-trial3_start)
    rats_data['trial4'] = vdm.Epoch(trial4_start, trial4_stop-trial4_start)

    filtered = events

    for cue in cues:
        remove_idx = []
        for i, event in enumerate(events[cue]):
            if rats_data[remove_trial].contains(event):
                remove_idx.append(i)
        filtered[cue] = np.delete(events[cue], remove_idx)

    return filtered
