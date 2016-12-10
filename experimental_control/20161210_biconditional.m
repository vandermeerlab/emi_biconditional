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

% Steady (cue) light
cue.command = '-SetDigitalIOBit';
cue.port = '0';
cue.pin = '2';
cue.event = 'cue';
cue.ttl = '21'; % ttl numbers are arbitrary 
cue.id = '1'; % id numbers are arbitrary

% Flashing (house) light
house.command = '-SetDigitalIOBit';
house.port = '0';
house.pin = '3';
house.event = 'house';
house.ttl = '22'; % ttl numbers are arbitrary 
house.id = '2'; % id numbers are arbitrary
house.on_duration = 0.1;
          
% Tone sound
tone.command = '-SetDigitalIOBit';
tone.port = '2';
tone.pin = '0';
tone.event = 'tone';
tone.ttl = '23'; % ttl numbers are arbitrary 
tone.id = '3'; % id numbers are arbitrary

% White-noise sound
noise.command = '-SetDigitalIOBit';
noise.port = '2';
noise.pin = '1';
noise.event = 'noise';
noise.ttl = '24'; % ttl numbers are arbitrary 
noise.id = '4'; % id numbers are arbitrary

% Sounds initially on (because they are triggered by being pulled low)
% Here, let's turn them off to initialize for the experiment
sounds.off = @(command, port, pin) NlxSendCommand([command, ' AcqSystem1_0 ', port, ' ' , pin, ' on']);

sounds.off(tone.command, tone.port, tone.pin);
sounds.off(noise.command, noise.port, noise.pin);

% Biconditional experiment parameters
biconditional.light_delay = 0;
biconditional.light_duration = 10;
biconditional.pause_duration = 5;
biconditional.sound_duration = 10;
biconditional.trial_duration = biconditional.light_duration + biconditional.pause_duration + biconditional.sound_duration;

% Initializing timers
control.steady_on_timer = timer('StartDelay', biconditional.light_delay, ...
    'TimerFcn', @(~, ~) set_nlx('on', cue));
control.steady_off_timer = timer('StartDelay', biconditional.light_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', cue));

control.pulse_on_timer = timer('StartDelay', 0, 'Period', house.on_duration*2, ...
    'TimerFcn', @(~, ~) NlxSendCommand([house.command, ' AcqSystem1_0 ', house.port, ' ' , house.pin, ' on']), 'ExecutionMode', 'fixedSpacing');
control.pulse_off_timer = timer('StartDelay', house.on_duration, 'Period', house.on_duration*2, ...
    'TimerFcn', @(~, ~) NlxSendCommand([house.command, ' AcqSystem1_0 ', house.port, ' ' , house.pin, ' off']), 'ExecutionMode', 'fixedSpacing');

control.flash_on_timer = timer('StartDelay', biconditional.light_delay, ...
    'TimerFcn', @(~, ~) pulse(control.pulse_on_timer, control.pulse_off_timer, house));
control.flash_off_timer = timer('StartDelay', biconditional.light_duration, ...
    'TimerFcn', @(~, ~) stop_timer(control.flash_on_timer, control.pulse_on_timer, control.pulse_off_timer, house));

control.tone_on_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', tone));
control.tone_off_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration + biconditional.sound_duration, ...
    'TimerFcn', @(~, ~) set_nlx('on', tone));

control.noise_on_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration, ...
    'TimerFcn', @(~, ~) set_nlx('off', noise));
control.noise_off_timer = timer('StartDelay', biconditional.light_duration + biconditional.pause_duration + biconditional.sound_duration, ...
    'TimerFcn', @(~, ~) set_nlx('on', noise));

control.feeder_timer = timer('StartDelay', biconditional.trial_duration, ...
    'TimerFcn', ['fireFeeder(' feeder.port, ', ', feeder.pin, ', ', feeder.n_pellets, ');']);

control.trial1_event = '-PostEvent "trial1_start" 99 9';
control.trial2_event = '-PostEvent "trial2_start" 88 8';
control.trial3_event = '-PostEvent "trial3_start" 77 7';
control.trial4_event = '-PostEvent "trial4_start" 66 6';


%% Check steady cue light & tone
disp(['Checking the steady light (', num2str(biconditional.light_duration), ' sec)']);
start(control.steady_off_timer);
start(control.steady_on_timer);

disp(['Checking the tone (pause ', num2str(biconditional.light_duration + biconditional.pause_duration), ' sec; on for ', num2str(biconditional.sound_duration), ' sec)']);
start(control.tone_off_timer);
start(control.tone_on_timer);


%% Check flashing house light & white-noise & feeder (2 pellets)

disp(['Checking the flashing light (', num2str(biconditional.light_duration), ' sec)']);
start(control.flash_off_timer);
start(control.flash_on_timer);

disp(['Checking the white-noise (pause ', num2str(biconditional.light_duration + biconditional.pause_duration), ' sec; on for ', num2str(biconditional.sound_duration), ' sec)']);
start(control.noise_off_timer);
start(control.noise_on_timer);

disp(['Checking the feeder with ', num2str(feeder.n_pellets), ' pellets after ', num2str(biconditional.trial_duration), ' sec delay']);
start(control.feeder_timer)


%% Finished initializing
initialized = 1;
disp('Maze initialized. Empty pellets. Ready to start experiment!');

%% Set up daily trials, itis

% % Test
% trials = [1, 2, 3, 4, 1, 2, 3, 4, 1];
% itis = [5, 5, 5, 5, 5, 5, 5, 5, 5];

% % Session 1
trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1];
itis = [330, 210, 270, 210, 150, 270, 150, 330, 210, 150, 210, 330, 150, 270, 270, 330, 210, 330, 150, 210, 270, 270, 330, 150, 270, 210, 150, 330, 150, 270, 210, 330, 150];

% % Session 2
% trials = [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [150, 330, 270, 150, 210, 270, 210, 330, 330, 330, 150, 270, 270, 210, 150, 210, 210, 330, 210, 150, 270, 150, 330, 270, 270, 330, 270, 210, 330, 150, 150, 210, 150];

% % Session 3
% trials = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1];
% itis = [150, 270, 210, 270, 330, 150, 210, 330, 270, 270, 330, 210, 210, 150, 330, 150, 150, 150, 210, 270, 270, 210, 330, 330, 210, 330, 330, 150, 270, 210, 270, 150, 150];

% % Session 4
% trials = [1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [150, 210, 330, 330, 150, 270, 210, 270, 210, 330, 150, 270, 210, 330, 150, 270, 210, 210, 270, 270, 150, 330, 150, 330, 210, 330, 270, 210, 150, 270, 330, 150, 150];

% % Session 5
% trials = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [210, 210, 330, 270, 150, 270, 150, 330, 210, 330, 150, 330, 210, 270, 270, 150, 330, 150, 210, 270, 330, 150, 270, 210, 210, 210, 150, 150, 330, 270, 330, 270, 150];

% % Session 6
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [210, 270, 330, 330, 210, 150, 270, 150, 210, 270, 150, 210, 150, 330, 330, 270, 270, 210, 210, 330, 330, 150, 270, 150, 330, 270, 150, 150, 330, 210, 270, 210, 150];

% % Session 7
% trials = [2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 1];
% itis = [270, 330, 150, 150, 210, 330, 270, 210, 330, 270, 330, 210, 150, 210, 150, 270, 330, 330, 150, 210, 270, 270, 210, 150, 150, 330, 270, 330, 210, 150, 270, 210, 150];

% % Session 8
% trials = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1];
% itis = [210, 150, 270, 210, 330, 270, 150, 330, 330, 270, 270, 330, 210, 150, 210, 150, 150, 330, 150, 270, 270, 210, 330, 210, 270, 210, 330, 330, 270, 150, 210, 150, 150];

% % Session 9
% trials = [4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 1];
% itis = [210, 150, 270, 270, 150, 330, 330, 210, 210, 210, 270, 270, 150, 330, 330, 150, 330, 330, 270, 210, 270, 150, 150, 210, 150, 210, 330, 150, 270, 210, 270, 330, 150];

% % Session 10
% trials = [3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 1, 2, 2, 2, 2, 1];
% itis = [330, 150, 270, 150, 330, 270, 210, 210, 270, 270, 150, 210, 330, 210, 150, 330, 330, 330, 270, 270, 150, 150, 210, 210, 150, 270, 270, 210, 330, 210, 330, 150, 150];


n_trials = 32;

if length(trials) < (n_trials + 1)
	error('Too few trials!')
end

if length(itis) < (n_trials + 1)
	error('Too few itis!')
end

control.group = 2;


%% Run biconditional experiment

if ~exist('initialized','var') || ~initialized
   error('you MUST initialize first!'); 
end

disp('Experiment started. See figure for details!');

figure(1);
h_title = title('Setting up...'); set(h_title, 'Interpreter', 'none');
axis off;

tic;
while toc < itis(1)
    set(h_title,'String',sprintf('time %.1f, ITI %d', toc, itis(1)));
    drawnow;
end

count = 1;

while count <= n_trials
    
    this_trial = trials(count);
    this_iti = itis(count + 1);
    
    f_biconditional(this_trial, control)
    
    tic; 
    while toc < this_iti + biconditional.trial_duration
        set(h_title,'String',sprintf('time %.1f, ITI %.1d, next_trial: %d, n_trials %d',...
            toc, this_iti + biconditional.trial_duration, trials(count + 1), count));
        drawnow;
    end

    count = count + 1;
end

disp('Done experiment!');
