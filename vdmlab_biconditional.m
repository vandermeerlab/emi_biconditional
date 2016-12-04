%% Reset & connect to Cheetah

clear all;
initialized = 0;

if exist('steady_on','var')
    stop(steady_on);
    stop(flashing_on);
end

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
% Photobeam
TTLInputPort_phbeam = 1;

% Feeder
TTLOutputPort_feeder = 0; % 0 refers to something in I/O port
feeder = 2; % 2 refers to some configuration; 2 and 6 for shortcut feeders
n_pellets = 2;
disp('Testing the feeder');
fireFeeder(TTLOutputPort_feeder, feeder, n_pellets);

% Steady light
TTLIOutputPort_led = '2';
pulseDuration = '250';
period_led = 0.1;
LEDOffDelay = 1;

set_light = cat(2, '-SetDigitalIOPulseDuration AcqSystem1_0 ', ...
                 TTLIOutputPort_led, ' ' ,  pulseDuration);
             
[succeeded, cheetahReply] = NlxSendCommand(set_light);

set_light = cat(2, '-DigitalIOTTLPulse AcqSystem1_0 ', ...
                TTLIOutputPort_led, ' ' , num2str(led_ID), ' High');
            
timer_f = @(led_ID) NlxSendCommand(set_light);

steady_on = timer('StartDelay', LEDOffDelay, 'Period', period_led, ...
                     'TimerFcn', 'timer_f(0);', 'ExecutionMode', ...
                     'fixedSpacing');

stop_f = @(timers) stop(timers);

steady_off = timer('StartDelay', LEDOffDelay, 'TimerFcn', ...
                   'stopfun(steady_on)');
               
disp('Testing steady light (5 sec)');
start(steady_on);
pause(5);
start(steady_off);

% Flashing light
TTLIOutputPort_led = '2';
pulseDuration = '250';
period_led = 0.1;
LEDOffDelay = 1;

set_light = cat(2, '-SetDigitalIOPulseDuration AcqSystem1_0 ', ...
                 TTLIOutputPort_led, ' ' ,  pulseDuration);

[succeeded, cheetahReply] = NlxSendCommand(set_light);

set_light = cat(2, '-DigitalIOTTLPulse AcqSystem1_0 ', ...
                TTLIOutputPort_led, ' ' , num2str(led_ID), ' High');
            
timer_f = @(led_ID) NlxSendCommand(set_light);

flashing_on = timer('StartDelay', LEDOffDelay, 'Period', period_led, ...
                     'TimerFcn', 'timer_f(1);', 'ExecutionMode', ...
                     'fixedSpacing');

stop_f = @(timers) stop(timers);

flashing_off = timer('StartDelay', LEDOffDelay, 'TimerFcn', ...
                   'stopfun(flashing_on)');
               
disp('Testing flashing light (5 sec)');
start(flashing_on);
pause(5);
start(flashing_off);

% Tone


% White noise



% Finish initializing
initialized = 1; % this tells RunMaze.m it's OK to go
disp('Maze initialized. Empty pellets. Ready to start experiment!');