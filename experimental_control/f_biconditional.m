function f_biconditional(trial, control)

   % Group 1
   % 1. steady -> noise - (light1 -> sound2 -)
   % 2. steady -> tone +  (light1 -> sound1 +)
   % 3. flashing -> tone -  (light2 -> sound1 -)
   % 4. flashing -> noise + (light2 -> sound2 +)
   
   % Group 2
   % 1. flashing -> noise - (light2 -> sound2 -)
   % 2. flashing -> tone +  (light2 -> sound1 +)
   % 3. steady -> tone -  (light1 -> sound1 -)
   % 4. steady -> noise + (light1 -> sound2 +)

	if control.group == 1
	    if trial == 1
	    	% Steady light (10 s), pause (5 s), white-noise (10 s), unrewarded
	        run_trial(control, control.trial1_event, control.steady_on_timer, ...
	        control.steady_off_timer, control.noise_on_timer, control.noise_off_timer, [])
	    elseif trial == 2
	        % Steady light (10 s), pause (5 s), tone (10 s), rewarded
	        run_trial(control, control.trial2_event, control.steady_on_timer, ...
	        control.steady_off_timer, control.tone_on_timer, control.tone_off_timer, control.feeder_timer)
	    elseif trial == 3
	        % Flashing light (10 s), pause (5 s), tone (10 s), unrewarded
	        run_trial(control, control.trial3_event, control.flash_on_timer, ...
	        control.flash_off_timer, control.tone_on_timer, control.tone_off_timer, [])
	    elseif trial == 4
	        % Flashing light (10 s), pause (5 s), white-noise (10 s), rewarded
	        run_trial(control, control.trial4_event, control.flash_on_timer, ...
	        control.flash_off_timer, control.noise_on_timer, control.noise_off_timer, control.feeder_timer)
	    end

    elseif control.group == 2
    	if trial == 1
	    	% Flashing light (10 s), pause (5 s), white-noise (10 s), unrewarded
	        run_trial(control, control.trial1_event, control.flash_on_timer, ...
	        control.flash_off_timer, control.noise_on_timer, control.noise_off_timer, [])
	    elseif trial == 2
	        % Flashing light (10 s), pause (5 s), tone (10 s), rewarded
	        run_trial(control, control.trial2_event, control.flash_on_timer, ...
	        control.flash_off_timer, control.tone_on_timer, control.tone_off_timer, control.feeder_timer)
	    elseif trial == 3
	        % Steady light (10 s), pause (5 s), tone (10 s), unrewarded
	        run_trial(control, control.trial3_event, control.steady_on_timer, ...
	        control.steady_off_timer, control.tone_on_timer, control.tone_off_timer, [])
	    elseif trial == 4
	        % Steady light (10 s), pause (5 s), white-noise (10 s), rewarded
	        run_trial(control, control.trial4_event, control.steady_on_timer, ...
	        control.steady_off_timer, control.noise_on_timer, control.noise_off_timer, control.feeder_timer)
        end

    elseif control.group == 3
        if trial == 1
            run_magazine(control.feeder_timer)
        else
            error('magazine group only has 1 trial')
        end
        
	else
		error('unknown group. Must be 1 or 2 or 3 (magazine training)')
    end

end


function run_trial(control, trial_start_event, light_on_timer, light_off_timer, sound_on_timer, sound_off_timer, feeder_timer)
    stop_all(control);
    
    NlxSendCommand(trial_start_event);
    
    start(light_off_timer);
    start(light_on_timer);
    
    start(sound_off_timer);
    start(sound_on_timer);
    
    if ~isempty(feeder_timer)
    	start(feeder_timer);
    end
    
end


function run_magazine(feeder_timer)
    stop(feeder_timer);

    start(feeder_timer);
    
end



function stop_all(control)
    % Stops all timers
 
    stop(control.steady_off_timer);
    stop(control.flash_off_timer);
    stop(control.tone_off_timer);
    stop(control.noise_off_timer);
    
    stop(control.feeder_timer);
    
    stop(control.steady_on_timer);
    stop(control.flash_on_timer);
    stop(control.tone_on_timer);
    stop(control.noise_on_timer);
    
end