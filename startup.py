import scipy.io as sio

def load_events(matfile):
    loading_events = sio.loadmat(matfile)
    print(loading_events['evt_tone_on'])
    events = dict()
    events['start_recording'] = loading_events['evt_start'][0]
    events['stop_recording'] = loading_events['evt_stop'][0]
    events['pb_off'] = loading_events['evt_pb_off'][0]
    events['pb_on'] = loading_events['evt_pb_on'][0]
    events['cue_on'] = loading_events['evt_cue_on'][0]
    events['cue_off'] = loading_events['evt_cue_off'][0]
    events['house_on'] = loading_events['evt_house_on'][0]
    events['house_off'] = loading_events['evt_house_off'][0]
    events['feeder'] = loading_events['evt_feeder'][0]
    events['noise_on'] = loading_events['evt_noise_on'][0]
    events['noise_off'] = loading_events['evt_noise_off'][0]
    events['tone_on'] = loading_events['evt_tone_on'][0]
    events['tone_off'] = loading_events['evt_tone_off'][0]
    events['trial1_start'] = loading_events['evt_trial1_start'][0]
    events['trial2_start'] = loading_events['evt_trial2_start'][0]
    events['trial3_start'] = loading_events['evt_trial3_start'][0]
    events['trial4_start'] = loading_events['evt_trial4_start'][0]
    events['type'] = loading_events['evt_type'][0]
    events['label'] = []
    for label in loading_events['evt_label'][0]:
        events['label'].extend(label)
    return events


def load_events_old(matfile):
    loading_events = sio.loadmat(matfile)
    events = dict()
    events['start_recording'] = loading_events['evt_start'][0]
    events['stop_recording'] = loading_events['evt_stop'][0]
    events['pb_off'] = loading_events['evt_pb_off'][0]
    events['pb_on'] = loading_events['evt_pb_on'][0]
    events['main_off'] = loading_events['evt_main_off'][0]
    events['cue'] = loading_events['evt_cue'][0]
    events['house'] = loading_events['evt_house'][0]
    events['feeder'] = loading_events['evt_feeder'][0]
    events['noise_off'] = loading_events['evt_noise_off'][0]
    events['tone_off'] = loading_events['evt_tone_off'][0]
    events['noise_on'] = loading_events['evt_noise_on'][0]
    events['tone_on'] = loading_events['evt_tone_on'][0]
    events['type'] = loading_events['evt_type'][0]
    events['label'] = []
    for label in loading_events['evt_label'][0]:
        events['label'].extend(label)
    return events
