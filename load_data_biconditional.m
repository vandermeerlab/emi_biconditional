% Change this filepath to where this data is located on your computer.
path = 'R105-2016-12-10_behavior';

% Below works on Emily's work computer
filepath = 'E:\data-biconditional\data-working\';
savepath = 'E:\code\emi_biconditional\cache\data\vdmlab\';

% cd to data
cd([filepath, path]);

%% input events for biconditional 

% Note: correct event sequence is on then off for lights (pin high for on),
% but off then on for sounds (pin low for on). Correcting variable names
% here.

event.feeder = 'feeder';
event.cue_on = 'cue_on';
event.cue_off = 'cue_off';
event.house_on = 'house_on';
event.house_off = 'house_off';
event.tone_on = 'tone_on';
event.tone_off = 'tone_off';
event.noise_on = 'noise_on';
event.noise_off = 'noise_off';
event.pb_on = 'pb_on'; 
event.pb_off = 'pb_off';
event.start = 'start_recording';
event.stop = 'stop_recording';
event.trial1_start = 'trial1_start';
event.trial1_stop = 'trial1_stop';
event.trial2_start = 'trial2_start';
event.trial2_stop = 'trial2_stop';
event.trial3_start = 'trial3_start';
event.trial3_stop = 'trial3_stop';
event.trial4_start = 'trial4_start';
event.trial4_stop = 'trial4_stop';

cfg_evt = [];

cfg_evt.eventList = {'Starting Recording'; ...
                     'Stopping Recording'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).'; ...
                     'cue_off'; ...
                     'cue_on'; ...
                     'house_off'; ...
                     'house_on'; ...
                     'noise_off'; ...
                     'noise_on'; ...
                     'tone_off'; ...
                     'tone_on'; ...
                     'trial1_start'; ...
                     'trial2_start'; ...
                     'trial3_start'; ...
                     'trial4_start'};
                 
cfg_evt.eventLabel = {'start_recording'; 'stop_recording'; 'pb_on'; 'pb_off'; 'feeder'; ...
                      'cue_off'; 'cue_on'; 'house_off'; 'house_on'; ...
                      'noise_on'; 'noise_off'; 'tone_on'; 'tone_off'; ...
                      'trial1_start'; 'trial2_start'; 'trial3_start'; 'trial4_start'};  
              
evt = LoadEvents(cfg_evt);

% save events in .mat to be read in python             
evt_type = evt.type;
evt_feeder = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.feeder))))});
evt_cue_on = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.cue_on))))});
evt_cue_off = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.cue_off))))});
evt_house_on = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.house_on))))});
evt_house_off = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.house_off))))});
evt_tone_on = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.tone_on))))});
evt_tone_off = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.tone_off))))});
evt_noise_on = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.noise_on))))});
evt_noise_off = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.noise_off))))});
evt_pb_on = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_on))))});
evt_pb_off = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_off))))});
evt_start = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.start))))});
evt_stop = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.stop))))});
evt_trial1_start = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial1_start))))});
evt_trial2_start = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial2_start))))});
evt_trial3_start = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial3_start))))});
evt_trial4_start = unique(evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial4_start))))});
evt_label = evt.label;

save([savepath, path(1:15), '-event'], ...
     'evt_feeder', 'evt_cue_on', 'evt_cue_off', 'evt_house_on', 'evt_house_off', ...
     'evt_tone_on', 'evt_tone_off', 'evt_noise_on', 'evt_noise_off', 'evt_pb_on', ...
     'evt_pb_off', 'evt_start', 'evt_stop', 'evt_type', 'evt_label', ...
     'evt_trial1_start', 'evt_trial2_start', 'evt_trial3_start', 'evt_trial4_start');
 
 
%%
% Testing
event.feeder = 'feeder';
event.cue_on = 'cue_on';
event.cue_off = 'cue_off';
event.house_on = 'house_on';
event.house_off = 'house_off';
event.tone_on = 'tone_on';
event.tone_off = 'tone_off';
event.noise_on = 'noise_on';
event.noise_off = 'noise_off';
event.pb_on = 'pb_on'; 
event.pb_off = 'pb_off';
event.start = 'start_recording';
event.stop = 'stop_recording';
event.trial1_start = 'trial1_start';
event.trial1_stop = 'trial1_stop';
event.trial2_start = 'trial2_start';
event.trial2_stop = 'trial2_stop';
event.trial3_start = 'trial3_start';
event.trial3_stop = 'trial3_stop';
event.trial4_start = 'trial4_start';
event.trial4_stop = 'trial4_stop';
event.zero = 'zero';
event.one = 'one';
event.two = 'two';
event.three = 'three';
event.four = 'four';
event.five = 'five';

cfg_evt = [];

cfg_evt.eventList = {'Starting Recording'; ...
                     'Stopping Recording'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0004).'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0000).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0020).'; ...
                     'cue_off'; ...
                     'cue_on'; ...
                     'house_off'; ...
                     'house_on'; ...
                     'noise_off'; ...
                     'noise_on'; ...
                     'tone_off'; ...
                     'tone_on'; ...
                     'trial1_start'; ...
                     'trial2_start'; ...
                     'trial3_start'; ...
                     'trial4_start'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0000).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0004).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0008).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 2 value (0x0001).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 2 value (0x0002).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 2 value (0x0003).'};
                 
cfg_evt.eventLabel = {'start_recording'; 'stop_recording'; 'pb_on'; 'pb_off'; 'feeder'; ...
                      'cue_off'; 'cue_on'; 'house_off'; 'house_on'; ...
                      'noise_on'; 'noise_off'; 'tone_on'; 'tone_off'; ...
                      'trial1_start'; 'trial2_start'; 'trial3_start'; 'trial4_start'; ...
                      'zero'; 'one'; 'two'; 'three'; 'four'; 'five'};  
              
evt = LoadEvents(cfg_evt);
            
evt_type = evt.type;
evt_feeder = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.feeder))))};
evt_cue_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.cue_on))))};
evt_cue_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.cue_off))))};
evt_house_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.house_on))))};
evt_house_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.house_off))))};
evt_tone_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.tone_on))))};
evt_tone_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.tone_off))))};
evt_noise_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.noise_on))))};
evt_noise_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.noise_off))))};
evt_pb_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_on))))};
evt_pb_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_off))))};
evt_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.start))))};
evt_stop = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.stop))))};
evt_trial1_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial1_start))))};
evt_trial2_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial2_start))))};
evt_trial3_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial3_start))))};
evt_trial4_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.trial4_start))))};
evt_zero = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.zero))))};
evt_one = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.one))))};
evt_two = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.two))))};
evt_three = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.three))))};
evt_four = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.four))))};
evt_five = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.five))))};
evt_label = evt.label;

save([savepath, path(1:15), '-event'], ...
     'evt_feeder', 'evt_cue_on', 'evt_cue_off', 'evt_house_on', 'evt_house_off', ...
     'evt_tone_on', 'evt_tone_off', 'evt_noise_on', 'evt_noise_off', 'evt_pb_on', ...
     'evt_pb_off', 'evt_start', 'evt_stop', 'evt_type', 'evt_label', ...
     'evt_trial1_start', 'evt_trial2_start', 'evt_trial3_start', 'evt_trial4_start', ...
     'evt_zero', 'evt_one', 'evt_two', 'evt_three', 'evt_four', 'evt_five');
 
%%
fn = FindFile('*Events.nev');
if isempty(fn)
   error('LoadEvents: no events file found.'); 
end

[EVTimeStamps, EventIDs, TTLs, EVExtras, EventStrings, EVHeader] = Nlx2MatEV(fn,[1 1 1 1 1],1,1,[]);
unique(EventStrings)
