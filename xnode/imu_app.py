import serial
import time
from threading import Thread

ser = serial.Serial("/dev/ttyUSB2", 115200) 

def set_cmd():
    while True:
        cmd = input()
        ser.write(cmd.encode())
        time.sleep(.1)

th = Thread(target=set_cmd)
th.daemon = True                # 얘가 죽으면 스레드가 같이 죽음   # 각자 병행해서 작동
th.start()

while True:
    try:
        ret = ser.readline()
        if ret:
            print(ret.decode()[:-2])        # 제일 뒤의 '\n'을 뺌
    except(KeyboardInterrupt):
        break

ser.close()