project.py
```
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
import serial
import time
import math

ser = serial.Serial("/dev/ttyUSB0", 115200)
if not ser:
    print("코디네이터가 연결되지 않았습니다")

def location(x,y):
    #print(x,y)
    plt.axis([-10,70,-10,130])
    plt.plot(x, y,'rs')
    plt.show()

wList = np.array([])
quat = np.array([])
# point1 = np.array([])
# point2 = np.array([])
point1 = []
point2 = []
powerList = [np.array([]),np.array([]),np.array([]),np.array([])]
x,y = 0,0


# 신호 세기 측정 (Slider)
# for i in range(4):
#     wList = np.append(wList, widgets.IntSlider(max=100, description='rssi_rout'+str(i+1)))
#     display(wList[i])

# quaternion [0], [3]
quat = np.append(quat, widgets.FloatSlider(min=-1.0, max=1.0, description='quat0'))
quat = np.append(quat, widgets.FloatSlider(min=-1.0, max=1.0, description='quat3'))
display(quat[0])
display(quat[1])

angle = widgets.IntSlider(min=0, max=360, description='angle')
display(angle)

check = True
if check:
    check = not check
    
    start = time.time()
    while True:
        try:
            ret = ser.readline()
            if ret:
                #print(ret.decode()[:-2])        # 제일 뒤의 '\n'을 뺌

                receive = np.array([])
                receive = ret.decode()[:-2].split('#')        # 라우터이름, 신호세기
                #print(receive)
                receiveQuat = np.array([])
                receiveQuat = receive[2].split(',')
                
                receiveQuat[0] = float(receiveQuat[0])
                receiveQuat[1] = float(receiveQuat[1])
                receiveQuat[2] = float(receiveQuat[0])
                
                if receiveQuat[1] < 0:
                    receiveQuat[0] *= -1
                if receiveQuat[2] < 0:
                    receiveQuat[1] *= -1
                    
                quat[0].value = receiveQuat[0]
                quat[1].value = receiveQuat[1]
                #print(receiveQuat)
                q0 = receiveQuat[0]
                q1 = receiveQuat[1]
                
                if receiveQuat[0] > -0.97 and receiveQuat[0] < 0.97:
                    angle.value = int(((np.arccos(float(receiveQuat[0]))*(-2)*(180/math.pi)))%360)
                else:
                    angle.value = int(((np.arcsin(float(receiveQuat[1]))*(-2)*(180/math.pi)))%360)
                    
        except(KeyboardInterrupt):
            break
```

image.py
```
# ![chart](https://user-images.githubusercontent.com/58851945/128623140-f622c82e-aff0-4b2e-aceb-baf0b54a7413.png)

import matplotlib.image as img 
import matplotlib.pyplot as plt
#fileName = "c:\\sample.png" 
fileName = "https://user-images.githubusercontent.com/58851945/128623140-f622c82e-aff0-4b2e-aceb-baf0b54a7413.png"
ndarray = img.imread(fileName) 
plt.imshow(ndarray) 
plt.show()
```

방향조절.py
```
import time
import serial
from pop.Pilot import SerBot
from pop.CAN import OmniWheel
from threading import Thread
from pop.CAN import OmniWheel
import numpy as np

ser = serial.Serial("/dev/ttyUSB0", 115200) 
ret = ser.readline()
omni = OmniWheel()
#map = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
map = np.ones(20)


def getSignal():

    global ret
    while True:
        try:
            ret = ser.readline()
            if ret:
                print(ret.decode()[:-3])        # 제일 뒤의 '\n'을 뺌
        except(KeyboardInterrupt):
            break

    ser.close()


if __name__ == '__main__':

    th = Thread(target=getSignal)
    th.daemon = True      
    th.start()

    time.sleep(1)

    while True:
        if ret:
            direction = float(ret.decode()[-10:-3])
            break
        else:
            time.sleep(0.5)


    while True:
        print("direction : ",direction)
        print("now : ",float(ret.decode()[-10:-3]))
        if direction > float(ret.decode()[-10:-3]):
            if (direction - float(ret.decode()[-10:-3])) > 0.05:
                print("turn left")

                omni.forward([15,15,15])
            else:
                omni.wheel(1,40)
                omni.wheel(2,-41)

        elif direction < float(ret.decode()[-10:-3]):
            if (direction - float(ret.decode()[-10:-3])) < -0.05:
                print("turn right")
                omni.backward([15,15,15])
            else:
                omni.wheel(1,40)
                omni.wheel(2,-41)

            
        else:
            omni.wheel(1,40)
            omni.wheel(2,-41)
```
