function pulse(pulse_on_timer, pulse_off_timer, control)
    NlxSendCommand(['-PostEvent "', control.event, '_on" ', control.ttl, ' ', control.id']);
    start(pulse_off_timer)
    start(pulse_on_timer)
end