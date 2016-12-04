% Change this filepath to where this data is located on your computer.
path = '2016-12-04_test';

% Below works on Emily's work computer
filepath = 'E:\data-biconditional\data-working\';
savepath = 'E:\code\emi_biconditional\cache\data\vdmlab\';

%% cd to data
cd([filepath, path]);

%% input events for biconditional 

event.cue = 'cue';
event.house = 'house';
event.feeder = 'feeder';
event.tone = 'tone';
event.noise = 'noise';
event.start = 'start recording';
event.stop = 'stop recording';
event.pb_off = 'pb_off';
event.pb_on = 'pb_on'; 
event.main_off = 'main_off';
event.sound_off = 'sound_off';
event.sound2_off = 'sound2_off';

cfg_evt = [];

cfg_evt.eventList = {'0 2 cue';...
                     '0 3 house'; ...
                     '0 5 feeder'; ...
                     '2 0 tone'; ...
                     '2 1 noise'; ...
                     'Starting Recording'; ...
                     'Stopping Recording'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0050).'; ...
                     'TTL Input on AcqSystem1_0 board 0 port 1 value (0x0054).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 0 value (0x0000).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 2 value (0x0001).'; ...
                     'TTL Output on AcqSystem1_0 board 0 port 2 value (0x0002).'};
                 
cfg_evt.eventLabel = {'cue', 'house', 'feeder', 'tone', 'noise', 'start recording', ...
                      'stop recording', 'pb_off', 'pb_on', 'main_off', 'sound_off', 'sound2_off'};  
              
evt = LoadEvents(cfg_evt);

%%              
evt_type = evt.type;
evt_start = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.start))))};
evt_stop = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.stop))))};
evt_pb_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_off))))};
evt_pb_on = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.pb_on))))};
evt_main_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.main_off))))};
evt_cue = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.cue))))};
evt_house = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.house))))};
evt_feeder = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.feeder))))};
evt_noise = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.noise))))};
evt_tone = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.tone))))};
evt_sound_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.sound_off))))};
evt_sound2_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, event.sound2_off))))};
evt_label = evt.label;

save([savepath, path(1:15), '-event'], ...
     'evt_start', 'evt_stop', 'evt_pb_off', 'evt_pb_on', 'evt_main_off', ...
     'evt_cue', 'evt_house', 'evt_feeder', 'evt_noise', 'evt_tone', ...
     'evt_sound_off', 'evt_sound2_off', 'evt_type', 'evt_label');
 
 
%%
fn = FindFile('*Events.nev');
if isempty(fn)
   error('LoadEvents: no events file found.'); 
end

[EVTimeStamps, EventIDs, TTLs, EVExtras, EventStrings, EVHeader] = Nlx2MatEV(fn,[1 1 1 1 1],1,1,[]);
unique(EventStrings)
%%
figure(1);
clf;
hold on;
plot(noise, ones(length(noise)), 'o')
%%
plot(tone, ones(length(tone)), 'o')
%%
plot(sound_off, ones(length(sound_off)), 'o')

%%
noise = evt.t{find(not(cellfun('isempty', strfind(evt.label, 'noise'))))}(1:10);

tone = evt.t{find(not(cellfun('isempty', strfind(evt.label, 'tone'))))}(1:10);

sound_off = evt.t{find(not(cellfun('isempty', strfind(evt.label, 'sound_off'))))}(1:10);


 