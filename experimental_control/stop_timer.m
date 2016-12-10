function stop_timer(started_timer, pulse_on_timer, pulse_off_timer, control)
    NlxSendCommand(['-PostEvent "', control.event, '_off" ', control.ttl, ' ', control.id']);
    NlxSendCommand([control.command, ' AcqSystem1_0 ', control.port, ' ' , control.pin, ' off']);
    stop(started_timer);
    stop(pulse_on_timer);
    stop(pulse_off_timer);
end