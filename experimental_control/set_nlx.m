function set_nlx(onoff, control)
    NlxSendCommand(['-PostEvent "', control.event, '_', onoff, '" ', control.ttl, ' ', control.id']);
    NlxSendCommand([control.command, ' AcqSystem1_0 ', control.port, ' ' , control.pin, ' ', onoff]);

end