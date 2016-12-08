import os

from startup import load_events, load_events_medpc


thisdir = os.path.dirname(os.path.realpath(__file__))
dataloc = os.path.abspath(os.path.join(thisdir, 'cache', 'data', 'vdmlab'))

def get_events(event_mat):
    return load_events(os.path.join(dataloc, event_mat))
