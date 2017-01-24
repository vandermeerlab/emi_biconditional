%% Reset & connect to Cheetah
clear all;
initialized = 0;

% Connect to Cheetah
connected = NlxAreWeConnected();
if connected == 1,
    disp 'Cheetah is already connected';
else
    serverName = '192.168.3.100';
    disp(sprintf('Connecting to %s...', serverName));
    success = NlxConnectToServer(serverName);
    if success ~= 1
        disp(sprintf('FAILED connect to %s.', serverName));
        return;
    else
        disp(sprintf('Connected to Cheetah at %s.', serverName));
    end
end

%% Initialize settings for photobeams, feeder, lights, sounds
disp('Initializing settings');

% Photobeam
photobeam.port = 1;

% Feeder (2 pellets)
feeder.port = '0';
feeder.pin = '5';
feeder.n_pellets = '2';

% Steady (left) light
light1.command = '-SetDigitalIOBit';
light1.port = '0';
light1.pin = '2';
light1.event = 'light1';
light1.ttl = '21'; % ttl numbers are arbitrary 
light1.id = '1'; % id numbers are arbitrary

% Flashing (right) light
light2.command = '-SetDigitalIOBit';
light2.port = '0';
light2.pin = '3';
light2.event = 'light2';
light2.ttl = '22'; % ttl numbers are arbitrary 
light2.id = '2'; % id numbers are arbitrary
light2.on_duration = 0.1;
          
% Click sound
sound1.command = '-SetDigitalIOBit';
sound1.port = '2';
sound1.pin = '2';
sound1.event = 'sound1';
sound1.ttl = '23'; % ttl numbers are arbitrary 
sound1.id = '3'; % id numbers are arbitrary

% White-noise sound
sound2.command = '-SetDigitalIOBit';
sound2.port = '2';
sound2.pin = '1';
sound2.event = 'sound2';
sound2.ttl = '24'; % ttl numbers are arbitrary 
sound2.id = '4'; % id numbers are arbitrary

% Sounds initially on (because they are triggered by being pulled low)
% Here, let's turn them off to initialize for the experiment
sounds.off = @(command, port, pin) NlxSendCommand([command, ' AcqSystem1_0 ', port, ' ' , pin, ' on']);

sounds.off(sound1.command, sound1.port, sound1.pin);
sounds.off(sound2.command, sound2.port, sound2.pin);

% Biconditional experiment parameters
biconditional.light_delay = 0;
biconditional.light_duration = 10;
biconditional.pause_duration = 1;
biconditional.sound_duration = 10;
biconditional.feeder_delay = biconditional.light_duration + ...
     biconditional.pause_duration + biconditional.sound_duration; % used in biconditional experiment.
% biconditional.feeder_delay = 0; % used for magazine training

% Initializing timers
control.light1_on_timer = timer('StartDelay', biconditional.light_delay, ...
    'TimerFcn', @(~, ~) set_nlx('on', light1));
control.light1_off_timer = timer('StartDelay', biconditional.light_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', light1));

control.pulse_on_timer = timer('StartDelay', 0, 'Period', light2.on_duration*2, ...
    'TimerFcn', @(~, ~) NlxSendCommand([light2.command, ' AcqSystem1_0 ', light2.port, ' ' , light2.pin, ' on']), 'ExecutionMode', 'fixedSpacing');
control.pulse_off_timer = timer('StartDelay', light2.on_duration, 'Period', light2.on_duration*2, ...
    'TimerFcn', @(~, ~) NlxSendCommand([light2.command, ' AcqSystem1_0 ', light2.port, ' ' , light2.pin, ' off']), 'ExecutionMode', 'fixedSpacing');

control.light2_on_timer = timer('StartDelay', biconditional.light_delay, ...
    'TimerFcn', @(~, ~) pulse(control.pulse_on_timer, control.pulse_off_timer, light2));
control.light2_off_timer = timer('StartDelay', biconditional.light_duration, ...
    'TimerFcn', @(~, ~) stop_timer(control.light2_on_timer, control.pulse_on_timer, control.pulse_off_timer, light2));

control.sound1_on_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', sound1));
control.sound1_off_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration + biconditional.sound_duration, ...
    'TimerFcn', @(~, ~) set_nlx('on', sound1));

control.sound2_on_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', sound2));
control.sound2_off_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration + biconditional.sound_duration, ...
    'TimerFcn', @(~, ~) set_nlx('on', sound2));

control.feeder_timer = timer('StartDelay', biconditional.feeder_delay, ...
    'TimerFcn', ['fireFeeder(' feeder.port, ', ', feeder.pin, ', ', feeder.n_pellets, ');']);

control.trial1_event = '-PostEvent trial1_start 99 9';
control.trial2_event = '-PostEvent trial2_start 88 8';
control.trial3_event = '-PostEvent trial3_start 77 7';
control.trial4_event = '-PostEvent trial4_start 66 6';


%% Check steady left light & sound1
disp(['Checking the steady light (', num2str(biconditional.light_duration), ' sec)']);
start(control.light1_off_timer);
start(control.light1_on_timer);

disp(['Checking the click (pause ', num2str(biconditional.light_duration + biconditional.pause_duration), ' sec; on for ', num2str(biconditional.sound_duration), ' sec)']);
start(control.sound1_off_timer);
start(control.sound1_on_timer);


%% Check flashing right light & white-noise & feeder (2 pellets)

disp(['Checking the flashing light (', num2str(biconditional.light_duration), ' sec)']);
start(control.light2_off_timer);
start(control.light2_on_timer);

disp(['Checking the white-noise (pause ', num2str(biconditional.light_duration + biconditional.pause_duration), ' sec; on for ', num2str(biconditional.sound_duration), ' sec)']);
start(control.sound2_off_timer);
start(control.sound2_on_timer);

disp(['Checking the feeder with ', num2str(feeder.n_pellets), ' pellets after ', num2str(biconditional.feeder_delay), ' sec delay']);
start(control.feeder_timer)


%% Check the feeder (2 pellets)
disp('Checking the feeder');
start(control.feeder_timer)


%% Finished initializing
initialized = 1;
disp('Maze initialized. Empty pellets. Ready to start experiment!');

%% Set up daily trials, itis

% n_trials = 32;

% Test
trials = [1, 2, 3, 4, 1, 2, 3, 4, 1];
itis = [2, 2, 2, 2, 5, 5, 5, 5, 5];
n_trials = 4;

% Magazine training
%trials = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
%itis = [150, 210, 330, 330, 150, 210, 270, 270, 330, 150, 270, 150, 270, 210, 330, 210, 150];
% n_trials = 16;

% Session 1
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [330, 150, 270, 210, 210, 150, 330, 270, 210, 150, 330, 270, 210, 330, 150, 270, 150, 270, 210, 330, 330, 270, 150, 210, 210, 330, 150, 270, 270, 150, 210, 330, 150];

% % Session 2
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [210, 150, 330, 270, 150, 210, 330, 270, 150, 210, 270, 330, 210, 330, 150, 270, 150, 330, 210, 270, 210, 270, 330, 150, 210, 330, 270, 150, 270, 210, 330, 150, 150];
% 
% % Session 3
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [330, 270, 210, 150, 270, 210, 150, 330, 150, 270, 330, 210, 150, 210, 330, 270, 270, 150, 330, 210, 210, 330, 150, 270, 210, 330, 150, 270, 150, 330, 210, 270, 150];
% 
% % Session 4
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [210, 330, 270, 150, 270, 330, 210, 150, 210, 150, 270, 330, 150, 270, 210, 330, 330, 210, 150, 270, 330, 270, 150, 210, 330, 210, 150, 270, 270, 150, 330, 210, 150];
% 
% % Session 5
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [210, 330, 270, 150, 150, 270, 330, 210, 330, 150, 210, 270, 210, 330, 150, 270, 210, 270, 330, 150, 210, 150, 270, 330, 330, 270, 210, 150, 150, 270, 210, 330, 150];
% 
% % Session 6
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [330, 210, 150, 270, 330, 150, 270, 210, 150, 210, 270, 330, 150, 270, 210, 330, 210, 270, 150, 330, 210, 330, 150, 270, 270, 210, 330, 150, 150, 270, 330, 210, 150];
% 
% % Session 7
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [210, 330, 150, 270, 210, 270, 330, 150, 330, 150, 210, 270, 270, 330, 210, 150, 150, 210, 270, 330, 210, 270, 150, 330, 270, 330, 210, 150, 330, 150, 210, 270, 150];
% 
% % Session 8
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [330, 270, 150, 210, 330, 210, 150, 270, 330, 150, 270, 210, 210, 270, 330, 150, 150, 210, 270, 330, 270, 150, 210, 330, 270, 330, 150, 210, 210, 150, 330, 270, 150];
% 
% % Session 9
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [330, 270, 210, 150, 150, 270, 330, 210, 330, 210, 150, 270, 330, 150, 210, 270, 330, 150, 210, 270, 330, 150, 210, 270, 150, 330, 270, 210, 270, 330, 150, 210, 150];
% 
% % Session 10
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [270, 330, 210, 150, 150, 330, 210, 270, 150, 210, 330, 270, 210, 270, 150, 330, 210, 150, 330, 270, 150, 270, 210, 330, 270, 210, 330, 150, 270, 210, 150, 330, 150];
% 
% % Session 11
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 1];
% itis = [150, 330, 210, 270, 330, 210, 270, 150, 270, 330, 150, 210, 150, 330, 210, 270, 210, 270, 330, 150, 210, 330, 270, 150, 210, 330, 270, 150, 270, 330, 150, 210, 150];
% 
% % Session 12
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [150, 210, 330, 270, 330, 270, 210, 150, 270, 330, 150, 210, 210, 270, 330, 150, 150, 330, 210, 270, 330, 150, 270, 210, 150, 270, 330, 210, 270, 330, 150, 210, 150];
% 
% % Session 13
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [330, 270, 210, 150, 210, 150, 270, 330, 210, 270, 330, 150, 210, 270, 150, 330, 330, 210, 270, 150, 330, 210, 150, 270, 210, 150, 330, 270, 210, 270, 330, 150, 150];
% 
% % Session 14
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [150, 210, 330, 270, 330, 150, 270, 210, 330, 210, 150, 270, 210, 330, 270, 150, 210, 270, 150, 330, 150, 330, 210, 270, 210, 270, 330, 150, 210, 330, 150, 270, 150];
% 
% % Session 15
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [150, 330, 210, 270, 150, 270, 210, 330, 210, 150, 270, 330, 150, 330, 210, 270, 150, 270, 330, 210, 330, 150, 210, 270, 150, 330, 270, 210, 330, 210, 150, 270, 150];
% 
% % Session 16
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [210, 150, 330, 270, 150, 210, 270, 330, 210, 150, 270, 330, 210, 330, 270, 150, 330, 270, 150, 210, 270, 330, 150, 210, 150, 210, 330, 270, 330, 210, 270, 150, 150];
% 
% % Session 17
% trials = [1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [210, 150, 330, 270, 150, 330, 270, 210, 210, 150, 270, 330, 150, 210, 330, 270, 270, 150, 330, 210, 270, 150, 330, 210, 270, 210, 330, 150, 330, 210, 150, 270, 150];
% 
% % Session 18
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [330, 270, 150, 210, 270, 330, 210, 150, 150, 270, 210, 330, 210, 150, 330, 270, 150, 330, 270, 210, 210, 330, 270, 150, 270, 330, 150, 210, 330, 270, 210, 150, 150];
% 
% % Session 19
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1];
% itis = [150, 270, 210, 330, 330, 210, 150, 270, 270, 210, 150, 330, 330, 150, 210, 270, 330, 150, 210, 270, 150, 330, 270, 210, 150, 270, 330, 210, 210, 150, 270, 330, 150];
% 
% % Session 20
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [330, 270, 210, 150, 330, 210, 270, 150, 270, 330, 210, 150, 210, 330, 150, 270, 270, 150, 330, 210, 210, 270, 330, 150, 210, 150, 270, 330, 270, 210, 330, 150, 150];
% 
% % Session 21
% trials = [1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1];
% itis = [330, 150, 210, 270, 210, 330, 270, 150, 210, 330, 150, 270, 210, 270, 150, 330, 270, 210, 330, 150, 270, 210, 150, 330, 330, 210, 270, 150, 330, 150, 270, 210, 150];
% 
% % Session 22
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [270, 330, 210, 150, 210, 270, 150, 330, 330, 210, 150, 270, 210, 150, 330, 270, 330, 150, 270, 210, 270, 150, 210, 330, 330, 210, 150, 270, 210, 270, 150, 330, 150];
% 
% % Session 23
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [150, 270, 330, 210, 270, 150, 210, 330, 330, 150, 270, 210, 330, 270, 210, 150, 330, 270, 150, 210, 150, 210, 330, 270, 270, 330, 210, 150, 150, 330, 270, 210, 150];
% 
% % Session 24
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [210, 330, 270, 150, 270, 330, 210, 150, 210, 330, 150, 270, 150, 210, 270, 330, 150, 210, 270, 330, 330, 270, 210, 150, 150, 330, 270, 210, 330, 150, 270, 210, 150];
% 
% % Session 25
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [210, 150, 270, 330, 270, 210, 330, 150, 150, 330, 210, 270, 330, 210, 150, 270, 150, 270, 330, 210, 330, 150, 210, 270, 330, 210, 150, 270, 270, 330, 210, 150, 150];
% 
% % Session 26
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [150, 210, 270, 330, 330, 150, 270, 210, 150, 270, 210, 330, 270, 150, 210, 330, 210, 270, 150, 330, 210, 270, 330, 150, 210, 330, 270, 150, 330, 270, 150, 210, 150];
% 
% % Session 27
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [150, 270, 210, 330, 210, 270, 150, 330, 150, 210, 330, 270, 330, 270, 210, 150, 330, 270, 210, 150, 270, 210, 330, 150, 330, 270, 150, 210, 330, 210, 150, 270, 150];
% 
% % Session 28
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [270, 150, 210, 330, 150, 210, 330, 270, 330, 270, 150, 210, 330, 210, 150, 270, 330, 210, 150, 270, 210, 270, 150, 330, 210, 270, 330, 150, 210, 150, 330, 270, 150];
% 
% % Session 29
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [330, 270, 210, 150, 150, 330, 270, 210, 270, 330, 210, 150, 210, 270, 330, 150, 270, 150, 330, 210, 270, 330, 150, 210, 330, 210, 150, 270, 210, 330, 150, 270, 150];
% 
% % Session 30
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [270, 330, 150, 210, 210, 270, 150, 330, 270, 210, 150, 330, 150, 270, 330, 210, 270, 150, 210, 330, 330, 270, 210, 150, 270, 210, 330, 150, 270, 210, 330, 150, 150];
% 
% % Session 31
% trials = [1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [210, 150, 330, 270, 270, 210, 150, 330, 330, 210, 270, 150, 330, 150, 270, 210, 150, 330, 210, 270, 210, 150, 330, 270, 210, 330, 150, 270, 150, 330, 270, 210, 150];
% 
% % Session 32
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [210, 150, 270, 330, 330, 150, 210, 270, 270, 210, 330, 150, 270, 330, 210, 150, 150, 330, 270, 210, 270, 330, 150, 210, 150, 210, 270, 330, 210, 330, 150, 270, 150];
% 
% % Session 33
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [330, 150, 210, 270, 330, 150, 270, 210, 210, 270, 150, 330, 150, 330, 270, 210, 150, 210, 270, 330, 330, 270, 150, 210, 270, 210, 330, 150, 270, 210, 330, 150, 150];
% 
% % Session 34
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [330, 150, 270, 210, 330, 150, 270, 210, 150, 210, 330, 270, 330, 150, 210, 270, 150, 330, 270, 210, 270, 210, 150, 330, 270, 330, 210, 150, 210, 330, 150, 270, 150];
% 
% % Session 35
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [210, 270, 150, 330, 210, 270, 330, 150, 150, 210, 330, 270, 330, 270, 210, 150, 210, 150, 270, 330, 150, 210, 330, 270, 150, 330, 270, 210, 330, 210, 150, 270, 150];
% 
% % Session 36
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [210, 150, 270, 330, 270, 330, 150, 210, 150, 330, 210, 270, 150, 330, 270, 210, 330, 150, 210, 270, 210, 330, 270, 150, 150, 210, 330, 270, 150, 270, 330, 210, 150];
% 
% % Session 37
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [270, 150, 330, 210, 210, 270, 150, 330, 330, 210, 270, 150, 150, 330, 270, 210, 210, 150, 330, 270, 210, 270, 150, 330, 330, 150, 210, 270, 330, 270, 210, 150, 150];
% 
% % Session 38
% trials = [1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1];
% itis = [210, 330, 150, 270, 150, 270, 210, 330, 270, 150, 210, 330, 270, 210, 150, 330, 270, 150, 330, 210, 270, 210, 150, 330, 270, 210, 150, 330, 330, 270, 210, 150, 150];
% 
% % Session 39
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [150, 270, 210, 330, 330, 210, 150, 270, 330, 270, 210, 150, 330, 270, 150, 210, 270, 150, 330, 210, 150, 330, 210, 270, 330, 210, 270, 150, 270, 150, 330, 210, 150];
% 
% % Session 40
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [150, 270, 210, 330, 150, 210, 330, 270, 330, 150, 270, 210, 210, 330, 270, 150, 150, 330, 270, 210, 150, 270, 330, 210, 270, 210, 330, 150, 270, 210, 330, 150, 150];
% 
% % Session 41
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [150, 270, 210, 330, 270, 150, 210, 330, 150, 330, 270, 210, 270, 330, 210, 150, 150, 210, 330, 270, 270, 210, 150, 330, 330, 270, 210, 150, 210, 150, 330, 270, 150];
% 
% % Session 42
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [270, 150, 330, 210, 210, 330, 150, 270, 270, 330, 150, 210, 210, 330, 150, 270, 210, 330, 150, 270, 330, 270, 150, 210, 270, 330, 210, 150, 150, 330, 210, 270, 150];
% 
% % Session 43
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [150, 270, 210, 330, 330, 270, 210, 150, 270, 150, 210, 330, 150, 330, 270, 210, 210, 270, 330, 150, 210, 330, 150, 270, 330, 150, 270, 210, 330, 270, 210, 150, 150];
% 
% % Session 44
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [210, 270, 150, 330, 330, 270, 210, 150, 150, 330, 210, 270, 210, 270, 150, 330, 270, 210, 150, 330, 330, 270, 150, 210, 150, 270, 210, 330, 270, 330, 150, 210, 150];
% 
% % Session 45
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 1];
% itis = [210, 330, 150, 270, 210, 150, 270, 330, 210, 330, 150, 270, 330, 270, 210, 150, 150, 210, 330, 270, 330, 210, 270, 150, 210, 330, 270, 150, 330, 150, 270, 210, 150];
% 
% % Session 46
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1];
% itis = [330, 270, 210, 150, 150, 210, 270, 330, 210, 330, 150, 270, 270, 210, 150, 330, 210, 330, 270, 150, 150, 270, 210, 330, 210, 270, 330, 150, 270, 210, 330, 150, 150];
% 
% % Session 47
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [330, 150, 270, 210, 150, 210, 330, 270, 330, 270, 210, 150, 210, 330, 270, 150, 270, 330, 210, 150, 270, 210, 330, 150, 330, 150, 210, 270, 150, 270, 330, 210, 150];
% 
% % Session 48
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
% itis = [210, 270, 150, 330, 330, 150, 210, 270, 150, 330, 270, 210, 150, 330, 210, 270, 150, 210, 330, 270, 270, 210, 150, 330, 210, 270, 150, 330, 270, 210, 330, 150, 150];
% 
% % Session 49
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [330, 270, 150, 210, 150, 330, 210, 270, 270, 150, 330, 210, 210, 270, 150, 330, 330, 150, 270, 210, 330, 270, 210, 150, 150, 270, 210, 330, 330, 270, 150, 210, 150];
% 
% % Session 50
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [270, 150, 210, 330, 150, 270, 210, 330, 270, 210, 330, 150, 150, 270, 330, 210, 330, 150, 210, 270, 150, 210, 330, 270, 330, 210, 150, 270, 210, 330, 150, 270, 150];


if length(trials) < (n_trials + 1)
	error('Too few trials!')
end

if length(itis) < (n_trials + 1)
	error('Too few itis!')
end

control.group = 2; % Group 1/2 for biconditional cue combinations; Group 3 for magazine training.


%% Run biconditional experiment

if ~exist('initialized', 'var') || ~initialized
   error('you MUST initialize first!'); 
end

disp('Experiment started. See figure for details!');

figure(1);
h_title = title('Setting up...'); set(h_title, 'Interpreter', 'none');
axis off;

tic;
while toc < itis(1)
    set(h_title, 'String', sprintf('time %.1f, ITI %d', toc, itis(1)));
    drawnow;
end

count = 1;

while count <= n_trials
    
    this_trial = trials(count);
    this_iti = itis(count + 1);
    
    f_biconditional(this_trial, control)
    
    tic; 
    while toc < this_iti + biconditional.feeder_delay
        set(h_title,'String',sprintf('time %.1f, ITI %.1d, next_trial: %d, n_trials %d',...
            toc, this_iti + biconditional.feeder_delay, trials(count + 1), count));
        drawnow;
    end

    count = count + 1;
end

disp('Done experiment!');
