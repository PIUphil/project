from pop import xnode, time

while True:
    ni = str(xnode.atcmd('NI'))
    db = str(xnode.atcmd('DB'))
    
    if db:
        xnode.transmit(xnode.ADDR_COORDINATOR, ni+db)

    time.sleep_ms(10)
