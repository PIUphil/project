from pop import time

ser = Serial()

while True:
    packet = xnode.receive()
    if packet:
        data = packet['payload']
        ser.write(data)
    
    cmd = ser.read()
    if cmd:
        #xnode.transmit(xnode.ADDR_BROADCAST, cmd)    # IMURoutMAC; b'0013A20041AEF480'
        xnode.transmit(xnode.b'\x00\x13\xA2\x00\x41\xAE\xF4\x80', cmd)    # IMURoutMAC
    
    time.sleep(.1)