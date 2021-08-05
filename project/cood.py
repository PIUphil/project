from pop import xnode, time

while True:
    #xnode.transmit(xnode.ADDR_BROADCAST, "hello")

    packet = xnode.receive()
    if packet:
        print(str(packet['payload'])[2:-1])

    time.sleep_ms(10)
