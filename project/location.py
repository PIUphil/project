import numpy as np
import time
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
import serial
import matplotlib.pyplot as plt


ser = serial.Serial("/dev/ttyUSB0", 115200)

#npa = np.array(['a', 'b', 'c'])
#npa = np.append(npa, np.array(['d']))

def location(x,y):
    #print(x,y)
    plt.axis([-10,70,-10,130])
    plt.plot(x, y,'rs')
    plt.show()

wList = np.array([])
# point1 = np.array([])
# point2 = np.array([])
point1 = []
point2 = []
powerList = [np.array([]),np.array([]),np.array([]),np.array([])]

for i in range(4):
    wList = np.append(wList, widgets.IntSlider(max=100, description='rssi_rout'+str(i+1)))
    display(wList[i])

signalPower = np.ones(4)
x,y=0,0


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
                receive = ret.decode()[:-2].split('#') 

                if receive[0]=="Rout01":
                    wList[0].value = int(receive[1])
                    powerList[0] = np.append(powerList[0], np.array([int(receive[1])]))

                elif receive[0]=="Rout02":
                    wList[1].value = int(receive[1])
                    powerList[1] = np.append(powerList[1], np.array([int(receive[1])]))

                elif receive[0]=="Rout03":
                    wList[2].value = int(receive[1])
                    powerList[2] = np.append(powerList[2], np.array([int(receive[1])]))

                elif receive[0]=="IMURout":
                    wList[3].value = int(receive[1])
                    powerList[3] = np.append(powerList[3], np.array([int(receive[1])]))
                else:
                    pass
                #time.sleep(.1)
                signalPower -= 20     # 최소거리

                if time.time()-start>5:
                    break
                    
        except(KeyboardInterrupt):
            break

    #print(powerList)
            
    for i in range(4):
        wList[i] = int(powerList[i].mean())
    #wList = np.array([i.mean() for i in powerList])
    print(wList)
    
    
    rr1 = wList[1] / (wList[1]+wList[3])
    rr2 = wList[0] / (wList[0]+wList[2])
    
    for i in range(60):
        for j in range(120):
            length1 = (i**2 + j**2)**(1/2)
            length3 = ((64.1-i)**2 + (129.1-j)**2)**(1/2)

            if (rr1*length1 - (1-rr1)*length3)**2 < 0.3 :
                  #point1 = np.append(point1, np.array([(i,j)]))
                point1.append((i,j))

            length0 = (i**2 + (129.1-j)**2)**(1/2)
            length2 = ((64.1-i)**2 + j**2)**(1/2)

            if (rr2*length0 - (1-rr2)*length2)**2 < 0.3 :
                  #point2 = np.append(point2, np.array([(i,j)]))
                point2.append((i,j))
     
    for i in point1:
        for j in point2:
            if i==j:
                print(i)
                x,y = i[0],i[1]                
                

#r = [r1,r2,r3,r4] = [1,1,1,1]
#x,y=0,0
# x = widgets.IntSlider(min=0, max=70, description='x')
# y = widgets.IntSlider(min=0, max=120, description='y')

interact(location, x=x, y=y)
