import scipy.io as sio

def load_events(matfile):
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
    events['noise'] = loading_events['evt_noise'][0]
    events['tone'] = loading_events['evt_tone'][0]
    events['sound_off'] = loading_events['evt_sound_off'][0]
    events['sound2_off'] = loading_events['evt_sound2_off'][0]
    events['type'] = loading_events['evt_type'][0]
    events['label'] = []
    for label in loading_events['evt_label'][0]:
        events['label'].extend(label)
    return events
