import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
import serial
import time

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
                
                if receiveQuat[1] < 0:
                    receiveQuat[0] *= -1
                    receiveQuat[1] *= -1
                    
                quat[0].value = receiveQuat[0]
                quat[1].value = receiveQuat[1]
                #print(receiveQuat)               
                
                
        except(KeyboardInterrupt):
            break
