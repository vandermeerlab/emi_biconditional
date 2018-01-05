import os
import numpy as np
import pandas as pd
import nept
from core import Experiment, Rat, Session, TrialEpochFromEpoch
import measurements as m

from load_data import correct_sounds, remove_double_inputs

import info.RH05d1 as RH05d1
import info.RH05d2 as RH05d2
import info.RH05d3 as RH05d3
import info.RH05d4 as RH05d4
import info.RH05d5 as RH05d5
import info.RH05d6 as RH05d6

# import info.R105d1 as R105d1
import info.R105d2 as R105d2
import info.R105d3 as R105d3
import info.R105d4 as R105d4
import info.R105d5 as R105d5
import info.R105d6 as R105d6


def get_vdm_epochs(filename, session, cue_duration=10):
    """Loads biconditional events. Corrects keys labels.

    Parameters
    ----------
    filename: str
    session: Session
    cue_duration: int

    Returns
    -------
    trial_epochs: list of TrialEpochFromEpoch

    """
    labels = dict()
    labels['start'] = 'Starting Recording'
    labels['stop'] = 'Stopping Recording'
    labels['light1_on'] = 'cue_on'
    labels['light1_off'] = 'cue_off'
    labels['light2_on'] = 'house_on'
    labels['light2_off'] = 'house_off'
    labels['sound1_on'] = 'tone_on'
    labels['sound1_off'] = 'tone_off'
    labels['sound2_on'] = 'noise_on'
    labels['sound2_off'] = 'noise_off'
    labels['trial1_start'] = 'trial1_start'
    labels['trial2_start'] = 'trial2_start'
    labels['trial3_start'] = 'trial3_start'
    labels['trial4_start'] = 'trial4_start'
    labels['feeder'] = 'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).'
    labels['pb_on'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).'
    labels['pb_off'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).'

    events = nept.load_events(filename, labels)
    events = correct_sounds(events)
    events['pb_on'], events['pb_off'] = remove_double_inputs(events['pb_on'], events['pb_off'])

    if session == 'R105d6':
        events['light2_off'] = np.insert(events['light2_off'], 12, events['light2_on'][12] + cue_duration)
    elif session == 'R105d4':
        events['light2_off'] = np.insert(events['light2_off'], 1, events['light2_on'][1] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 2, events['light2_on'][2] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 8, events['light2_on'][8] + cue_duration)
    elif session == 'R105d2':
        events['sound2_off'] = np.insert(events['sound2_off'], 3, events['sound2_on'][3] + cue_duration)
    elif session == 'RH05d3':
        events['light2_off'] = np.insert(events['light2_off'], 11, events['light2_on'][11] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 14, events['light2_on'][14] + cue_duration)
    elif session == 'RH05d4':
        events['light2_off'] = np.insert(events['light2_off'], 3, events['light2_on'][3] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 8, events['light2_on'][8] + cue_duration)

    trial_epochs = [
        TrialEpochFromEpoch("mags", nept.Epoch([events['pb_on'], events['pb_off']])),
        TrialEpochFromEpoch("baseline", nept.Epoch([events['light1_on'] - cue_duration, events['light1_on']])),
        TrialEpochFromEpoch("baseline", nept.Epoch([events['light2_on'] - cue_duration, events['light2_on']])),
        TrialEpochFromEpoch("light1", nept.Epoch([events['light1_on'], events['light1_off']])),
        TrialEpochFromEpoch("light2", nept.Epoch([events['light2_on'], events['light2_off']])),
        TrialEpochFromEpoch("sound1", nept.Epoch([events['sound1_on'], events['sound1_off']])),
        TrialEpochFromEpoch("sound2", nept.Epoch([events['sound2_on'], events['sound2_off']])),
        TrialEpochFromEpoch("trial1", nept.Epoch([events['trial1_start'], events['trial1_start'] + 25])),
        TrialEpochFromEpoch("trial2", nept.Epoch([events['trial2_start'], events['trial2_start'] + 25])),
        TrialEpochFromEpoch("trial3", nept.Epoch([events['trial3_start'], events['trial3_start'] + 25])),
        TrialEpochFromEpoch("trial4", nept.Epoch([events['trial4_start'], events['trial4_start'] + 25])),
    ]

    return trial_epochs


def add_nlx_datapoints(session, data, rat):
    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:5],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial == "trial2" else "unrewarded",
                "cue": cue,
            }
            trial = [trial_data for trial_data in data if trial_data.name == trial][0]
            cue = [cue_data for cue_data in data if cue_data.name == cue][0]
            session.add_epoch_data(rat.rat_id, trial.epoch.intersect(cue.epoch), meta)
        else:
            meta = {
                "cue_type": cue,
                "trial_type": "",
                "rewarded": "",
                "cue": cue,
            }
            session.add_epoch_data(rat.rat_id, [cue_data.epoch for cue_data in data if cue_data.name == cue][0], meta)

    if rat.group == "1":
        add_data("light1", "trial1")
        add_data("light2", "trial2")
        add_data("light2", "trial3")
        add_data("light1", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2", "trial1")
        add_data("light1", "trial2")
        add_data("light1", "trial3")
        add_data("light2", "trial4")
        add_data("sound1", "trial1")
        add_data("sound1", "trial2")
        add_data("sound2", "trial3")
        add_data("sound2", "trial4")
        add_data("baseline")


def letsdothis(expt):
    sessions = []
    for i, session_data in enumerate(expt.trial_epochs):
        session = Session(i + 1, expt.measurements)

        for rat in expt.rats:
            session.add_rat(rat.rat_id, [mag_data.epoch for mag_data in session_data if mag_data.name == "mags"][0])
            expt.add_datapoints(session, session_data, rat)
        sessions.append(session.to_df())

    expt.df = pd.concat(sessions, ignore_index=True)
    expt.df.isnull().values.any()
    return expt.df

colours = {'baseline, ': '#252525',
           'light, rewarded': '#1f77b4',
           'light, unrewarded': '#aec7e8',
           'light1, unrewarded': '#aec7e8',
           'light2, unrewarded': '#aec7e8',
           'sound, rewarded': '#2ca02c',
           'sound, unrewarded': '#98df8a',
           'sound1, rewarded': '#2ca02c',
           'sound2, unrewarded': '#98df8a',
           }

thisdir = '/home/emily/code/emi_biconditional'
data_filepath = os.path.join(thisdir, 'cache', 'data', '201610')
output_filepath = os.path.join(thisdir, 'plots', '201610')

r105_sessions = [R105d2, R105d3, R105d4, R105d5, R105d6]

r105_expt = Experiment(
    name="201610",
    cache_key="epoch_vdmlab",
    plot_key="vdmlab",
    trial_epochs=[get_vdm_epochs(os.path.join(data_filepath, session.event_file), session.session_id) for session in r105_sessions],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[Rat("R105", group="2")],
    sessionfiles=r105_sessions,
)

r105_expt.add_datapoints = add_nlx_datapoints
df = letsdothis(r105_expt)
for rat in r105_expt.rats:
    r105_expt.plot_rat(rat, colours=colours, by_outcome=False)

rh05_sessions = [RH05d1, RH05d2, RH05d3, RH05d4, RH05d5, RH05d6]

rh05_expt = Experiment(
    name="201610",
    cache_key="epoch_vdmlab",
    plot_key="vdmlab",
    trial_epochs=[get_vdm_epochs(os.path.join(data_filepath, session.event_file), session.session_id) for session in rh05_sessions],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[Rat("RH05", group="1")],
    sessionfiles=rh05_sessions,
)

rh05_expt.add_datapoints = add_nlx_datapoints
df = letsdothis(rh05_expt)
for rat in rh05_expt.rats:
    rh05_expt.plot_rat(rat, colours=colours, by_outcome=False)
