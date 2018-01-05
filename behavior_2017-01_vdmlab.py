import os
import numpy as np
import pandas as pd
import nept
from core import Experiment, Rat, Session, TrialEpochFromEpoch
import measurements as m

from load_data import correct_sounds, remove_double_inputs

import info.R115d1 as R115d1
import info.R115d2 as R115d2
import info.R115d3 as R115d3
import info.R115d4 as R115d4
import info.R115d5 as R115d5
import info.R115d6 as R115d6
import info.R115d7 as R115d7
import info.R115d8 as R115d8
import info.R115d9 as R115d9
import info.R115d10 as R115d10
import info.R115d11 as R115d11
import info.R115d12 as R115d12
import info.R115d13 as R115d13
import info.R115d14 as R115d14
import info.R115d15 as R115d15
import info.R115d16 as R115d16
import info.R115d17 as R115d17
import info.R115d18 as R115d18
import info.R115d19 as R115d19
import info.R115d20 as R115d20
import info.R115d21 as R115d21
import info.R115d22 as R115d22
import info.R115d23 as R115d23
import info.R115d24 as R115d24
import info.R115d25 as R115d25
import info.R115d26 as R115d26
import info.R115d27 as R115d27
import info.R115d28 as R115d28
import info.R115d29 as R115d29
import info.R115d30 as R115d30
import info.R115d31 as R115d31
import info.R115d32 as R115d32
import info.R115d33 as R115d33
import info.R115d34 as R115d34


def get_vdm_epochs(filename, session, cue_duration=10, photobeam='zero'):
    """Loads biconditional events. Corrects keys labels.

    Parameters
    ----------
    filename: str
    session: Session
    cue_duration: int
    photobeam: str
        'zero' or 'c' from changed pin configuration in the neuralynx system

    Returns
    -------
    trial_epochs: list of TrialEpochFromEpoch

    """
    labels = dict()
    labels['start'] = 'Starting Recording'
    labels['stop'] = 'Stopping Recording'
    labels['light1_on'] = 'light1_on'
    labels['light1_off'] = 'light1_off'
    labels['light2_on'] = 'light2_on'
    labels['light2_off'] = 'light2_off'
    labels['sound1_on'] = 'sound1_on'
    labels['sound1_off'] = 'sound1_off'
    labels['sound2_on'] = 'sound2_on'
    labels['sound2_off'] = 'sound2_off'
    labels['trial1_start'] = 'trial1_start'
    labels['trial2_start'] = 'trial2_start'
    labels['trial3_start'] = 'trial3_start'
    labels['trial4_start'] = 'trial4_start'
    labels['feeder'] = 'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).'
    if photobeam == 'zero':
        labels['pb_on'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0008).'
        labels['pb_off'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).'
    elif photobeam == 'c':
        labels['pb_off'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).'
        labels['pb_on'] = 'TTL Input on AcqSystem1_0 board 0 port 1 value (0x000C).'
    else:
        raise ValueError("must specify which photobeam used")

    events = nept.load_events(filename, labels)
    events = correct_sounds(events)
    events['pb_on'], events['pb_off'] = remove_double_inputs(events['pb_on'], events['pb_off'])

    if session == 'R115d2':
        events['light2_off'] = np.insert(events['light2_off'], 0, events['light2_on'][0] + cue_duration)
    elif session == 'R115d7':
        events['light2_off'] = np.insert(events['light2_off'], 6, events['light2_on'][6] + cue_duration)
    elif session == 'R115d8':
        events['light2_off'] = np.insert(events['light2_off'], 11, events['light2_on'][11] + cue_duration)
    elif session == 'R115d9':
        events['light2_off'] = np.insert(events['light2_off'], 3, events['light2_on'][3] + cue_duration)
    elif session == 'R115d11':
        events['light2_off'] = np.insert(events['light2_off'], 13, events['light2_on'][13] + cue_duration)
    elif session == 'R115d16':
        events['light2_off'] = np.insert(events['light2_off'], 15, events['light2_on'][15] + cue_duration)
    elif session == 'R115d19':
        events['light2_off'] = np.insert(events['light2_off'], 0, events['light2_on'][0] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 7, events['light2_on'][7] + cue_duration)
    elif session == 'R115d20':
        events['sound1_off'] = np.insert(events['sound1_off'], 14, events['sound1_on'][14] + cue_duration)
        events['sound2_off'] = np.insert(events['sound2_off'], 4, events['sound2_on'][4] + cue_duration)
    elif session == 'R115d21':
        events['light2_off'] = np.insert(events['light2_off'], 3, events['light2_on'][3] + cue_duration)
    elif session == 'R115d22':
        events['light2_off'] = np.insert(events['light2_off'], 4, events['light2_on'][4] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 15, events['light2_on'][15] + cue_duration)
    elif session == 'R115d24':
        events['light2_off'] = np.insert(events['light2_off'], 3, events['light2_on'][3] + cue_duration)
    elif session == 'R115d25':
        events['sound1_on'] = np.insert(events['sound1_on'], 6, events['sound1_off'][6] - cue_duration)
    elif session == 'R115d26':
        events['light2_off'] = np.insert(events['light2_off'], 0, events['light2_on'][0] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 9, events['light2_on'][9] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 14, events['light2_on'][14] + cue_duration)
    elif session == 'R115d28':
        events['light2_off'] = np.insert(events['light2_off'], 6, events['light2_on'][6] + cue_duration)
    elif session == 'R115d29':
        events['light2_off'] = np.insert(events['light2_off'], 10, events['light2_on'][10] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 14, events['light2_on'][14] + cue_duration)
        events['sound2_off'] = np.insert(events['sound2_off'], 10, events['sound2_on'][10] + cue_duration)
    elif session == 'R115d30':
        events['light2_off'] = np.insert(events['light2_off'], 1, events['light2_on'][1] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 9, events['light2_on'][9] + cue_duration)
        events['sound1_on'] = np.insert(events['sound1_on'], 3, events['sound1_off'][3] - cue_duration)
    elif session == 'R115d31':
        events['light2_off'] = np.insert(events['light2_off'], 5, events['light2_on'][5] + cue_duration)
        events['light1_off'] = np.insert(events['light1_off'], 0, events['light1_on'][0] + cue_duration)
    elif session == 'R115d32':
        events['light2_off'] = np.insert(events['light2_off'], 0, events['light2_on'][0] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 7, events['light2_on'][7] + cue_duration)
        events['light2_off'] = np.insert(events['light2_off'], 14, events['light2_on'][14] + cue_duration)
    elif session == 'R115d33':
        events['light1_off'] = np.insert(events['light1_off'], 3, events['light1_on'][3] + cue_duration)
    elif session == 'R115d34':
        events['light2_off'] = np.insert(events['light2_off'], 0, events['light2_on'][0] + cue_duration)


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
data_filepath = os.path.join(thisdir, 'cache', 'data', '201701')
output_filepath = os.path.join(thisdir, 'plots', '201701')

r115_sessions = [R115d1, R115d2, R115d3, R115d4, R115d5, R115d6, R115d7, R115d8, R115d9, R115d10,
                 R115d11, R115d12, R115d13, R115d14, R115d15, R115d16, R115d17, R115d18, R115d19,
                 R115d20, R115d21, R115d22, R115d23, R115d24, R115d25, R115d26, R115d27, R115d28,
                 R115d29, R115d30, R115d31, R115d32, R115d33, R115d34]

r115_expt = Experiment(
    name="201701",
    cache_key="epoch_vdmlab",
    plot_key="vdmlab",
    trial_epochs=[get_vdm_epochs(os.path.join(data_filepath, session.event_file), session.session_id, photobeam=session.photobeam) for session in r115_sessions],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[Rat("R115", group="2")],
    sessionfiles=r115_sessions,
)

r115_expt.add_datapoints = add_nlx_datapoints
df = letsdothis(r115_expt)
for rat in r115_expt.rats:
    r115_expt.plot_rat(rat, colours=colours, by_outcome=False)
