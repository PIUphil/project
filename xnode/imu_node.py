from pop import IMU, xnode, time
from serial import Serial

DEBUG = True

imu = IMU()
cmd = b'A'

if DEBUG:
    ser = Serial()

while True:
    data = ""

    if cmd == b'A':    
        for d in imu.accel(), imu.gyro():
            data += ("%.2f," * 3)%(d)
        data += ("%.2f," * 4)%(imu.quat()) 
    elif cmd == b'a':
        data = ("%.2f," * 3)%(imu.accel())
    elif cmd == b'g':
        data = ("%.2f," * 3)%(imu.gyro())
    elif cmd == b'q':
        data = ("%.2f," * 4)%(imu.quat()) 
    else:
        data = "Unknown command"
        
    data += '\n'
    xnode.transmit(xnode.ADDR_COORDINATOR, data)
    if DEBUG:
        ser.write(data)
    
    packet = xnode.receive()
    if packet:
        cmd = packet['payload']
    
    if DEBUG:
        t = ser.read()    
        if t:
            cmd = t
    
    time.sleep(0.1)