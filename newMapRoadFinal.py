import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QProgressBar
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt, noshowbase, QRect
from PIL import Image
import numpy as np
import time
import serial
import subprocess
from pop import LiDAR
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from pop.CAN import OmniWheel
from pop import Pilot
from gtts import gTTS
from random import randint
from popAssist import create_conversation_stream, GAssistant
import pyaudio
from gtts import gTTS
import wave
#%matplotlib inline
#%%

startlocation = 0

class mapping:

    def __init__(self, width = 5, height = 5, map = np.zeros((5,5))):
        self.ser = serial.Serial("/dev/ttyUSB1", 115200)
        self.ser2 = serial.Serial("/dev/ttyUSB2", 115200)
        self.map = np.zeros((width,height))
        self.omni = OmniWheel()
        self.serbot = Pilot.SerBot()
        self.stack = 0
        self.point = [(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
        self.goallist = [(79, 30), (2, 10), (2, 20), (2, 29), (27, 2), (39, 2), (51, 2), (63, 2), (79, 2), (27, 38), (39, 38), (51, 38), (63, 38)]
        self.lidarvalue = [1000,1000,1000,0]
        self.check_wall = False

    def __del__(self):
        self.lidar.stopMotor()
        self.omni.stop()

    def get_signal(self):
        global startlocation
        while True:
            self.ret2 = self.ser2.readline().decode()[:-2].split(',')
            time.sleep(0.01)
            print(self.ret2)
            if self.ret2:
                if self.ret2[0][2:] == 'tect':
                    self.go_goal(0.6,0,8)
                    break
            if self.ret2:
                if self.ret2[0][2:] == 'change':
                    self.go_goal(0.6,1,startlocation)
                    break

    def check_lidar(self):
        self.lidar = LiDAR.Rplidar()
        self.lidar.connect()
        self.lidar.startMotor()
        a = 1000
        b = 1000
        while True:
            vectors = self.lidar.getVectors()
            time.sleep(0.2)
            try:

                if (min(vectors[np.logical_and(330 < vectors[:,0], vectors[:,0] < 360)][:,1])) < (min(vectors[np.logical_and(0 < vectors[:,0], vectors[:,0] < 30)][:,1])):
                    self.lidarvalue[0] = (min(vectors[np.logical_and(330 < vectors[:,0], vectors[:,0] < 360)][:,1]))
                else:
                    self.lidarvalue[0] = (min(vectors[np.logical_and(0 < vectors[:,0], vectors[:,0] < 30)][:,1]))

                self.lidarvalue[1] = min(vectors[np.logical_and(290 < vectors[:,0], vectors[:,0] < 330)][:,1])
                self.lidarvalue[2] = min(vectors[np.logical_and(30 < vectors[:,0], vectors[:,0] < 70)][:,1])
                
                a = (vectors[np.logical_and(80 < vectors[:,0], vectors[:,0] < 100)][:,1]).mean()
                b = (vectors[np.logical_and(260 < vectors[:,0], vectors[:,0] < 280)][:,1]).mean()
                
                if b >2000 or a > 2000:
                    self.lidarvalue[3] = 1
                else:
                    self.lidarvalue[3] = 0
                
            except:
                pass
            
            #print(self.lidarvalue)

    def check_cross(self):
        if self.lidarvalue[3] == 1:  
            self.stack += 1
        else:
            self.stack = 0

    def go_goal(self,travel_time = 0.5, goal = 1, location = 2):
        global startlocation

        self.location = self.goallist[location]
        self.goal = self.goallist[goal]
        self.map[self.location] = 1
        self.map[self.goal] = 2
        self.finish = True 
        remove_list = self.point[:]
        goal_point = self.goal[:]

        for i in remove_list:
            if self.location[0] - self.goal[0] < 0:
                if self.location[0] > i[0]:
                    self.point.remove(i)
            else:
                if self.location[0] < i[0]:
                    self.point.remove(i)

        #print(self.point)
        for i in self.point:
            self.map[i] = 3

        while self.finish:

            self.check_cross()
            print(self.location)

            if self.stack >= 2:
                print(goal_point,"##goal_point##")
                if goal_point:
                    if (self.location[1] == goal_point[1] and abs(self.location[0] - goal_point[0]) <= 4) or (self.location[0] == goal_point[0] and abs(self.location[1] - goal_point[1]) <= 4):
                        self.map[self.location] = 0 
                        self.location = goal_point
                        if self.map[self.location] != 2:
                            self.map[self.location] = 1 

            for i in self.point:
                if self.location == i:
                    self.point.remove(i)

            if 2 in self.map[self.location[0]]:
                goal_point = []
                point_distance = []

                for i in self.point:
                    point_distance.append(abs(self.location[0] - i[0]))
                
                if point_distance:
                    goal_point = self.point[point_distance.index(min(point_distance))]
                    print(goal_point,"##goal_point##")
                if abs(self.location[1] - self.goal[1]) <= 7: ######
                    self.check_wall = True
                    print(abs(self.location[1] - self.goal[1]))

                if self.goal[1] == self.location[1]:
                    #print(self.map[:])

                    self.finish = False
                    if 110 > self.direction and 70 < self.direction:

                        self.omni.forward([10,10,10])
                        self.omni.forward([10,10,10])
                        self.omni.forward([10,10,10])
                        while True:
                            if self.goal == (2,20):
                                if 170 < self.direction and self.direction <190:
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.stack = 0
                                    self.lidarvalue = [1000,1000,1000,0]
                                    self.check_wall = False
                                    self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                    startlocation = self.goallist.index(self.goal)
                                    return
                            elif self.goal == (79,30):
                                if (350 < self.direction and self.direction < 360) or (10 > self.direction and self.direction > 0):
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.stack = 0
                                    self.lidarvalue = [1000,1000,1000,0]
                                    self.check_wall = False
                                    self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                    startlocation = self.goallist.index(self.goal)
                                    return                               


                            time.sleep(0.001)
                            if 260 < self.direction and self.direction <280:
                                self.omni.stop()
                                self.omni.stop()
                                self.omni.stop()
                                self.stack = 0
                                self.lidarvalue = [1000,1000,1000,0]
                                self.check_wall = False
                                self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                startlocation = self.goallist.index(self.goal)
                                return

                    elif 250 < self.direction and 290 > self.direction:
                        self.omni.forward([10,10,10])
                        self.omni.forward([10,10,10])
                        self.omni.forward([10,10,10])
                        while True:
                            time.sleep(0.001)
                            if 80 < self.direction and self.direction <100:
                                self.omni.stop()
                                self.omni.stop()
                                self.omni.stop()
                                self.stack = 0
                                self.lidarvalue = [1000,1000,1000,0]
                                self.check_wall = False
                                self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                startlocation = self.goallist.index(self.goal)
                                return        

                elif self.goal[1] > self.location[1]:                
                    self.move(travel_time, 90)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]+1)
                    if self.map[self.location] != 2:
                        self.map[self.location] = 1
                    #print(self.map[:])

                elif self.goal[1] < self.location[1]:
                    self.move(travel_time, 270)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]-1)
                    if self.map[self.location] != 2:
                        self.map[self.location] = 1
                    #print(self.map[:])

            elif 3 in self.map[:,self.location[1]]:
                goal_point = []
                point_distance = []

                for i in self.point:
                    point_distance.append(abs(self.location[0] - i[0]))
                
                if point_distance:
                    print(self.point,"##self.point##")
                    print(point_distance, "##point_distance##")
                    goal_point = self.point[point_distance.index(min(point_distance))]
                    print(goal_point,"##goal_point##")
                
                if goal_point[0] < self.location[0]:
                    self.move(travel_time, 0)
                    self.map[self.location] = 0
                    self.location = (self.location[0]-1, self.location[1])
                    self.map[self.location] = 1
                    #print(self.map[:])

                elif goal_point[0] > self.location[0]:
                    self.move(travel_time, 180)
                    self.map[self.location] = 0
                    self.location = (self.location[0]+1, self.location[1])
                    self.map[self.location] = 1
                    #print(self.map[:])

            elif 3 in self.map[self.location[0]]:
                goal_point = []
                point_distance = []

                for i in self.point:
                    point_distance.append(abs(self.location[0] - i[0]))
                
                if point_distance:
                    goal_point = self.point[point_distance.index(min(point_distance))]
                    print(goal_point,"##goal_point##")
                if goal_point[1] > self.location[1]:
                    self.move(travel_time, 90)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]+1)
                    self.map[self.location] = 1
                    #print(self.map[:])

                elif goal_point[1] < self.location[1]:
                    self.move(travel_time, 270)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]-1)
                    self.map[self.location] = 1
                    #print(self.map[:])    

            else:
                goal_point = []
                point_distance = []

                for i in self.point:
                    point_distance.append(abs(self.location[0] - i[0]))
                
                if point_distance:
                    goal_point = self.point[point_distance.index(min(point_distance))]
                    print(goal_point,"##goal_point##")

                if goal_point[1] > self.location[1]:
                    self.move(travel_time, 90)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]+1)
                    self.map[self.location] = 1
                    #print(self.map[:])

                elif goal_point[1] < self.location[1]:
                    self.move(travel_time, 270)
                    self.map[self.location] = 0
                    self.location = (self.location[0], self.location[1]-1)
                    self.map[self.location] = 1
                    #print(self.map[:])

    def move(self,travel_time, direction):
        global startlocation

        print(self.direction)
        delay_t = 0
        start_t = time.time()
        end_t = start_t
        turn = False

        while (start_t - end_t)>=-travel_time:
            #print(self.lidarvalue)
            if not turn:
                if self.lidarvalue[0]< 270:
                    if self.check_wall:
                        if (110 > self.direction) and (70 < self.direction):
                            self.omni.forward([10,10,10])
                            self.omni.forward([10,10,10])
                            self.omni.forward([10,10,10])
                            while True:
                                time.sleep(0.001)
                                if (260 < self.direction) and (self.direction <280):
                                    self.map[self.location] = 0 
                                    self.location = self.goal
                                    if self.map[self.location] != 2:
                                        self.map[self.location] = 1
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.stack = 0
                                    self.lidarvalue = [1000,1000,1000,0]
                                    self.check_wall = False
                                    self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                    startlocation = self.goallist.index(self.goal)
                                    self.finish = False
                                    return
                                

                        elif 250 < self.direction and 290 > self.direction:
                            self.omni.forward([10,10,10])
                            self.omni.forward([10,10,10])
                            self.omni.forward([10,10,10])
                            while True:
                                time.sleep(0.001)
                                if 80 < self.direction and self.direction <100:
                                    self.map[self.location] = 0 
                                    self.location = self.goal
                                    if self.map[self.location] != 2:
                                        self.map[self.location] = 1
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.omni.stop()
                                    self.stack = 0
                                    self.lidarvalue = [1000,1000,1000,0]
                                    self.check_wall = False
                                    self.point =[(2, 26), (27, 26), (39, 26), (51, 26), (63, 26), (79, 26)]
                                    startlocation = self.goallist.index(self.goal)
                                    self.finish = False
                                    return 
                            
                    else:
                        print("area[0] <270")
                        self.omni.stop()
                        time.sleep(0.5)
                        delay_t = travel_time + (start_t - end_t)
                        print(delay_t,"##????????????##")
                        travel_time = delay_t
                        start_t = time.time()
                        end_t = start_t
                        turn = False
                        continue      

                elif self.lidarvalue[1] < self.lidarvalue[2] and self.lidarvalue[1] <240:
                    print("area[1] < area[2] and area[1] < 240")
                    self.serbot.move(90,30)
                    time.sleep(0.3)
                    delay_t = travel_time + (start_t - end_t)
                    print(delay_t,"##????????????##")
                    travel_time = delay_t
                    start_t = time.time()
                    end_t = start_t
                    turn = False
                    continue  


                elif self.lidarvalue[1] > self.lidarvalue[2] and self.lidarvalue[2] <230:
                    print("area[2] > area[1] and area[2] < 230")
                    self.serbot.move(270,30)
                    time.sleep(0.3)
                    delay_t = travel_time + (start_t - end_t)
                    print(delay_t,"##????????????##")
                    travel_time = delay_t
                    start_t = time.time()
                    end_t = start_t
                    turn = False
                    continue  

            if self.direction > 180:
                t_direction = 360 - self.direction
            else:
                t_direction = self.direction
            
            if direction > 180:
                g_direction = 360 - direction
            else:
                g_direction = direction

            if (t_direction - g_direction)**2 > 30:
                turn = True
                if (self.direction-direction)%360 < 180:
                    self.omni.forward([10,10,10])
                    if (t_direction - g_direction)**2 < 25:
                        if (t_direction - g_direction)**2 > 8:
                            if (self.direction-direction)%360 < 180:
                                turn = False
                                self.omni.wheel(1,40)
                                self.omni.wheel(2,-55.5)                              
                                end_t = time.time()
                                
                            else:
                                turn = False
                                self.omni.wheel(1,55)
                                self.omni.wheel(2,-40.5)                                
                                end_t = time.time()

                        else:
                            turn = False
                            self.omni.wheel(1,40)
                            self.omni.wheel(2,-40.5)
                            
                            end_t = time.time()
                else:
                    self.omni.backward([10,10,10])
                    if (t_direction - g_direction)**2 < 25:
                        if (t_direction - g_direction)**2 > 8:
                            if (self.direction-direction)%360 < 180:
                                turn = False
                                self.omni.wheel(1,40)
                                self.omni.wheel(2,-55.5)                             
                                end_t = time.time()
                            else:
                                turn = False
                                self.omni.wheel(1,55)
                                self.omni.wheel(2,-40.5)                               
                                end_t = time.time()

                        else:
                            turn = False
                            self.omni.wheel(1,40)
                            self.omni.wheel(2,-40.5)                            
                            end_t = time.time()
     
            else:
                turn = True
                if (t_direction - g_direction)**2 > 8:
                    if (self.direction-direction)%360 < 180:
                        turn = False
                        self.omni.wheel(1,40)
                        self.omni.wheel(2,-55.5)                      
                        end_t = time.time()
                    else:
                        turn = False
                        self.omni.wheel(1,55)
                        self.omni.wheel(2,-40.5)                        
                        end_t = time.time()

                else:
                    turn = False
                    self.omni.wheel(1,40)
                    self.omni.wheel(2,-40.5)              
                    end_t = time.time()

    def getAngle(self):
        while True:
            time.sleep(0.01)
            try:
                while True:
                    time.sleep(0.01)
                    self.ret = self.ser.readline()

                    if self.ret:
                        if len(self.ret.decode()[:-3]) > 82:      
                            break
                
                self.signal = self.ret.decode()[:-3].split(',&')
                self.direction_n = self.signal[2].split(',')
                direction = [0,0,0]


                direction[0] = float(self.direction_n[0])
                direction[1] = float(self.direction_n[3])
                direction[2] = float(self.direction_n[0])

                if direction[1] < 0:
                    direction[0] *= -1
                if direction[2] < 0:
                    direction[1] *= -1
                
                if direction[0] > -0.72 and direction[0] < 0.72:
                    self.direction = ((np.arccos(float(direction[0]))*(-2)*(180/math.pi)))%360
                else:
                    self.direction = ((np.arcsin(float(direction[1]))*(-2)*(180/math.pi)))%360 

            except ValueError:
               break
            #print(self.direction)
        self.ser.close()

# class Voice:


# def userAction(text): 
#     # global filename # ????????????
#     # global stream

#     action = False
#     print(text) 

#     def callback(in_data, frame_count, time_info, status):
#         data = w.readframes(frame_count)
#         return (data, pyaudio.paContinue)


#     if text.find("??????") != -1 or text.find("??????") != -1 or text.find("??????") != -1 or text.find("????????????") != -1:
        
#         text = "????????? ???????????????"
#         filename = "start.mp3"
#         tts = gTTS(text, lang='ko')
#         tts.save(filename)
        
#         w = wave.open("10.wav", "rb")       ## ????????????
#         p = pyaudio.PyAudio()
        
#         stream = p.open(format=p.get_format_from_width(w.getsampwidth()), channels=w.getnchannels(),
#                         rate=w.getframerate(), output=True, stream_callback=callback) 

#         with subprocess.Popen(['play', filename]) as p:           ## gtts?????? ??????
#             p.wait()


#     #    while stream.is_active():                  ##????????????
#         # print("main work...")
#     #        time.sleep(0.1)
        
#         stream.start_stream()

#         # bot.forward()
#         action = True
    
        

#     ###

#     if text.find("??????") != -1 or text.find("??????") != -1:
#         text = "?????????????????????."
#         filename2 = "stop.mp3"
#         tts = gTTS(text, lang='ko')
#         tts.save(filename2)

#         stream.stop_stream()
#         stream.close()
        
#         # p = pyaudio.PyAudio() # ????????????
        
#         p.terminate()
        
#         filename2 = "stop.mp3" 
        
        
#         with subprocess.Popen(['play', filename2]) as p:  
#             p.wait()

#         # bot.stop() 
#         action = True

#     return True


# stream = create_conversation_stream()
# ga = GAssistant(stream, local_device_handler=userAction)



class RoadmapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roadmap")

        self.baseLabel = QLabel(self)
        self.baseLabel.move(0,0)
        self.baseLabel.resize(1280,720)
        self.baseLabel.setPixmap(QPixmap("pic/base.png"))
        self.baseLabel.show()

        self.intro0 = QLabel(self)
        self.intro0.move(280,20)
        self.intro0.resize(1000,600)
        self.intro0.setText("(O) (O)\n(???'???'???)")
        self.intro0.setFont(QFont('MesloLGS NF', 170))
        self.intro0.show()

        self.intro1 = QLabel(self)
        self.intro1.move(280,20)
        self.intro1.resize(1000,600)
        self.intro1.setText("\n ???   ??? ")
        self.intro1.setFont(QFont('MesloLGS NF', 170))
        self.intro1.setStyleSheet("color:#FF6FB7")
        self.intro1.show()

        self.introText = QLabel(self)
        self.introText.move(300,530)
        self.introText.resize(1000,200)
        self.introText.setText("????????? ???????????? ????????? ??????????????????")
        self.introText.setFont(QFont('MesloLGS NF', 40))
        self.introText.show()

        self.introBt = QPushButton(self)
        self.introBt.move(0,0)
        self.introBt.resize(1280,720)
        self.introBt.clicked.connect(self.init)
        self.introBt.setStyleSheet("background:transparent; border:0px")
        
        self.exitBt = QPushButton("X",self)
        self.exitBt.move(1180,0)
        self.exitBt.resize(100,100)
        self.exitBt.clicked.connect(self.onExitBtClicked)
        self.exitBt.setStyleSheet("background:transparent; border:0px; color:#F0F0F0")
        self.exitBt.setFont(QFont('MesloLGS NF', 25))
        self.exitBt.raise_()


        thIntro = Thread(target=self.intro)
        thIntro.daemon = True
        thIntro.start()

        # self.init()

    def intro(self):
        time.sleep(1)
        with subprocess.Popen(['play', "voice/mainVoice0.mp3"]) as p:    # "???????????????"
            p.wait()


    def init(self):
        self.destination = self.now = (14,30)
        
        # ??????(??????)
        self.baseLabel.raise_()

        # ??????
        self.label = QLabel(self)
        self.label.move(55,20)
        self.label.resize(450,684)

        img = Image.open('../notebook/map.png')
        img_resize = img.resize((int(img.width *1.142), int(img.height *1.142)))
        img_resize.save('map_resize.png')
        self.label.setPixmap(QPixmap("map_resize.png"))  # map, mapLine
        self.label.show()
    
        # ?????????
        label_text = QLabel(self)
        label_text.setText("??? ???????????? ???????????? ???????????????")
        label_text.move(535,10)
        label_text.resize(1000,90)
        label_text.setFont(QFont('MesloLGS NF', 40))
        label_text.show()

        # ??????
        self.label_pic = QLabel(self)
        self.label_pic.move(530,100)
        self.label_pic.resize(680,480)
        self.label_pic.setPixmap(QPixmap("pic/tomb.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)
        self.label_pic.show()

        # ????????????
        self.guideBt = QPushButton("???????????? ???",self)
        self.guideBt.move(620,600)
        self.guideBt.resize(500,100)
        self.guideBt.clicked.connect(self.onGuideBtClicked)
        self.guideBt.setStyleSheet("background:#F06292;")
        self.guideBt.setFont(QFont('MesloLGS NF', 45))
        self.guideBt.show()

        # ??????
        self.exitBt.raise_()

        self.destButton()






    def drawRoad(self, now, destination=(14,30)):
        self.destination = destination
        height = 32
        self.runLength = 0              # ????????????

        way = []
        for i in range(6):
            way.append((10,2+5*i))
        
        fig, ax = plt.subplots(figsize=(6, 12), constrained_layout=True)

        mapImage = plt.imread("../notebook/map.png")
        ax_map = ax.twinx()
        ax_map.set_xlim(ax.get_xlim())
        ax_map.set_ylim(ax.get_ylim())

        om = OffsetImage(mapImage, zoom=1.31)#1.2899, alpha=1)         # ????????? ?????? ??????
        box0 = AnnotationBbox(om, (8*0.96, 16*0.993), frameon=False) # ????????? ?????? ?????? ??????, ????????? ??????
        ax_map.add_artist(box0)                          # ????????? ??????

        ax_map.axis(False)                               # ?????? ????????? ?????? ????????????
        ax_map.set_zorder(-1)                            # ?????? ????????? axes??? ?????? axes??????
        ax.set_facecolor("none") 

        line_color = "blue"
        height=32

        # ?????????
        # ax.plot([0, 16], [0, 32], color="red")
        # ax.plot([0, 16], [32, 0], color="red")
        ax.plot([0, 16], [0, 0], color="black")
        ax.plot([0, 16], [32, 32], color="black")
        ax.plot([0, 0], [0, 32], color="black")
        ax.plot([16, 16], [0, 32], color="black")

        
        # ??? ?????????
        #plt.rcParams["font.family"] = 'NanumGothic'
        ax.fill([now[0], now[0], now[0]+1, now[0]+1], [height-now[1]-1, height-now[1], height-now[1], height-now[1]-1], color='red')              # now
        ax.text(now[0]+0.17, height-now[1]-1-0.4, 'now', fontdict={'family':'serif', 'color':'black', 'weight':'bold'})

        up = False
        go_way = []

        if now[1] > destination[1]:
            up = True
        else:
            up = False

        for i in way:#list(way.values()):
            if up:
                if now[1] >= i[1]:
                    go_way.append(i)
            else:
                if now[1] <= i[1]:
                    go_way.append(i)
            
        if go_way == []:
            go_way.append(way[0])
            go_way.append(way[5])

        length_way_now = [((now[0]-i[0])**2+(now[1]-i[1])**2)**0.5 for i in go_way]#list(way.values())]
        min_length_way_now = min(length_way_now)
        way_now = go_way[np.argmin(length_way_now)]

        length_way_ex = [((destination[0]-i[0])**2+(destination[1]-i[1])**2)**0.5 for i in way]#list(way.values())]
        min_length_way_ex = min(length_way_ex)
        way_ex = way[np.argmin(length_way_ex)]

        print(now, destination)
        #print(go_way)
        print(way_now, way_ex)

        line_color = "blue"

        if (way_now==way_ex) and (now[1]-destination[1])**2<5:
            ax.plot([now[0]+0.5, destination[0]+0.5], [height-now[1]-1+0.5, height-destination[1]-1+0.5], color=line_color)
            self.runLength += ((now[0]-destination[0])**2+(now[1]-destination[1])**2)**0.5
        else:
            ax.plot([now[0]+0.5, way_now[0]+0.5], [height-now[1]-1+0.5, height-way_now[1]-1+0.5], color=line_color)
            ax.plot([way_now[0]+0.5, way_ex[0]+0.5], [height-way_now[1]-1+0.5, height-way_ex[1]-1+0.5], color=line_color)
            ax.plot([destination[0]+0.5, way_ex[0]+0.5], [height-destination[1]-1+0.5, height-way_ex[1]-1+0.5], color=line_color)
            self.runLength += min_length_way_now
            self.runLength += ((way_now[0]-way_ex[0])**2+(way_now[1]-way_ex[1])**2)**0.5
            self.runLength += min_length_way_ex

        plt.xlim(-0.5,16.5)
        plt.ylim(-0.5,32.5)
        ax.axis('off')

        plt.savefig('mapLine.png')   # ??????????????? ??????

        img = Image.open('mapLine.png')
        img_resize = img.resize((int(img.width *0.6255), int(img.height *0.6255)))
        img_resize.save('mapLine.png')


    # ??? ??????
    def loadRoad(self):
        self.label = QLabel(self)
        self.label.move(120,20)
        self.label.resize(500,681)
        self.label.setPixmap(QPixmap("mapLine.png"))  # map, mapLine
        self.label.show()

    
    # ????????? [??????]
    def destButton(self):
        self.bt = []
        self.nm = []
        self.nameLabel=['?????????','?????????','?????????\n/ ??????','????????????', '????????????', '???????????????', '???????????????','????????????','????????????','?????????2','?????????1','?????????','??????']
        btconnect = [self.onChargeBtClicked, self.onPhotoBtClicked, self.onWcBtClicked,
         self.onEx0BtClicked, self.onEx1BtClicked, self.onEx2BtClicked, self.onEx3BtClicked, self.onInfoBtClicked,
         self.onShopBtClicked,self.onActivity2BtClicked,self.onActivity1BtClicked,self.onHistoryBtClicked, self.onStartBtClicked]
        
        for i in range(len(btconnect)):
            self.bt.append(QPushButton(self))
            self.bt[i].resize(120,100)
            self.bt[i].setStyleSheet("background:transparent; border:0px")
            self.bt[i].clicked.connect(btconnect[i])

            self.nm.append(QLabel(self))
            self.nm[i].setText(self.nameLabel[i])
            self.nm[i].setFont(QFont('MesloLGS NF', 18))


        for i in range(3):                      # ??????,??????,?????????            
            self.bt[i].move(130+(120*i),20)
            self.nm[i].move(139+(142*i),20)
        
        for i in range(5):                      # ??????,????????????
            self.bt[3+i].move(130,130+(105*i))
            self.nm[3+i].move(145,150+(105*i))

        for i in range(4):                      # ??????
            self.bt[8+i].move(400,130+(105*i))
            self.nm[8+i].move(405,150+(105*i))

        self.bt[12].move(355,588)               # ??????
        self.nm[12].move(384,628)
        self.nm[2].resize(100,48)
        self.raiseBt()
       


    def onStartBtClicked(self):    self.onButtonClicked(0)
    def onChargeBtClicked(self):   self.onButtonClicked(1)
    def onPhotoBtClicked(self):    self.onButtonClicked(2)
    def onWcBtClicked(self):       self.onButtonClicked(3)
    def onEx0BtClicked(self):      self.onButtonClicked(4)
    def onEx1BtClicked(self):      self.onButtonClicked(5)
    def onEx2BtClicked(self):      self.onButtonClicked(6)
    def onEx3BtClicked(self):      self.onButtonClicked(7)
    def onInfoBtClicked(self):     self.onButtonClicked(8)
    def onShopBtClicked(self):     self.onButtonClicked(9)
    def onActivity2BtClicked(self):self.onButtonClicked(10)
    def onActivity1BtClicked(self):self.onButtonClicked(11)
    def onHistoryBtClicked(self):  self.onButtonClicked(12)


    def onButtonClicked(self, btNum):   # ?????? ?????? - ?????? ????????? ??????
        self.destinationList = [(11,29.5), (1.5,1), (8,0.5), (13.5,0.5), (0.5,7), (0.5,12), (0.5,17), (0.5,22), (0.5,27), (14.5,7), (14.5,12), (14.5,17), (14.5,22)]
        pictureNameList = ["start.png", "charge.png", "photo.png", "wc.png", "crown.png", "earring.png", "thurible.png", "headdress.png", "tomb.png", "shop.png", "activity2.png", "activity1.png", "king.png"]

        self.drawRoad(self.now, self.destinationList[btNum])
        self.loadRoad()
        self.label_pic.setPixmap(QPixmap("pic/"+pictureNameList[btNum]))
        self.label_pic.setAlignment(Qt.AlignCenter)
        self.raiseBt()
        print(pictureNameList[btNum][:-4]+" button clicked")
        self.btNum = btNum


    def raiseBt(self):                  # ?????????, ????????? ???????????? ??????
        for i in range(13):
            self.nm[i].show()
            self.nm[i].raise_()
        for i in range(13):
            self.bt[i].show()
            self.bt[i].raise_()
            
    
    # def guiding(self):                  # ????????? ?????? ??????????????? ?????? - ?????????(??????????????? ?????????????) - label ??????????????? matplotlib ?????? ????????? ?????????...
    #     self.label_guide = QLabel(self)
    #     self.label_guide.move(133+(21.81*self.now[0])-20, 20+(21.094*self.now[1])-30)
    #     self.label_guide.resize(46,60)
    #     self.label_guide.setPixmap(QPixmap("pic/serbot1.png"))
    #     self.label_guide.setAlignment(Qt.AlignCenter)
    #     self.label_guide.show()
    #     self.label_guide.raise_()
    #     time.sleep(.3)

    
    def onGuideBtClicked(self):         # ?????????????????? ??????
        print("guide")
        # print(now[0], now[1])

        self.voice(self.btNum)


        def callback(in_data, frame_count, time_info, status):
            data = w.readframes(frame_count)
            return (data, pyaudio.paContinue)

        w = wave.open("music/music{}.wav".format(randint(1,8)), "rb")                # ????????????
        self.p = pyaudio.PyAudio()
        
        self.stream = self.p.open(format=self.p.get_format_from_width(w.getsampwidth()), channels=w.getnchannels(),
                        rate=w.getframerate(), output=True, stream_callback=callback) 
        
        self.stream.start_stream()


        print("???????????? :",self.runLength)

        print("????????????:",self.now, " / ????????????:",self.destination)

        # ?????? ????????????
        self.guideBt.setEnabled(False)
        self.guideBt.setStyleSheet("background:Gray; color:White;")
        self.guideBt.show()

        # step = tuple(np.round(((self.destination[0]-self.now[0])/100, (self.destination[1]-self.now[1])/100), 3))
        #print(step)

        # self.guiding()

        # ????????? ??????
        self.progressBard = QProgressBar(self)
        self.progressBard.setEnabled(True)
        self.progressBard.setGeometry(QRect(620, 585, 500, 15))

        self.rtime = self.runLength * 1.0   # ????????????

        thDrive = Thread(target=self.thRun)#, args=int(exNum))
        thDrive.daemon = True
        thDrive.start()
        # thDrive.join() 

        destinationList = [(11,29.5), (1.5,1), (8,0.5), (13.5,0.5), (0.5,7), (0.5,12), (0.5,17), (0.5,22), (0.5,27), (14.5,7), (14.5,12), (14.5,17), (14.5,22)]
        idxDest = destinationList.index(self.destination)
        map.go_goal(0.6,idxDest,startlocation)


        # while True:            
        #     self.now = tuple(np.round((self.now[0]+step[0], self.now[1]+step[1]), 3))
            # time.sleep(.03)
            # progressValue += 1      #step
            # self.progressBard.setProperty("value", progressValue)
            # self.progressBard.show()
            # time.sleep(self.runLength/501)      # /101
            

            # if progressValue == 100:
            #     time.sleep(.7)

            # if tuple(np.round((self.now), 1)) == tuple(np.round((self.destination), 1)):
            #     self.now = tuple(np.round((self.destination), 1))
            #     break
            # else:
            #     self.label_guide.destroy()

        time.sleep(1)
        self.now = self.destination
        
        self.guideBt.setEnabled(True)
        self.guideBt.setStyleSheet("background:#F06292; color:Black;")
        # self.guideBt.setFont(QFont('MesloLGS NF', 45))
        self.guideBt.show()

        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: white;}"
            )
        self.progressBard.show()

        self.drawRoad(self.now, self.now)
        self.loadRoad()

        self.stream.stop_stream()       # ????????????
        self.stream.close()
        self.p.terminate()

        if self.destination   == (0.5,7):   self.explain(0)
        elif self.destination == (0.5,12):  self.explain(1)
        elif self.destination == (0.5,17):  self.explain(2)
        elif self.destination == (0.5,22):  self.explain(3)
        elif self.destination == (14.5,22): self.explain(4)

        self.raiseBt()


    def explain(self,exNum):                    # ????????????

        explainTime = [15.6, 17.7, 15.8, 21.9, 23.7]    # ???????????? - (????????????,?????????,??????,?????????,?????????)
        print("???????????? : {}???".format(explainTime[exNum]))

        startExplainTime = time.time()

        self.guideBt.setText(" ???  ???  ???")
        self.guideBt.setStyleSheet("background:Gray; color:White;")
        self.guideBt.setEnabled(False)
        self.guideBt.show()

        time.sleep(.5)

        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: white;}"
            )
        self.progressBard.show()

        time.sleep(.1)


        print("prgVoice start")

        self.etime = explainTime[exNum]

        thExp = Thread(target=self.thExplain)#, args=int(exNum))            # ?????? ?????????
        thExp.daemon = True
        thExp.start()
        # thExp.join()                           

        with subprocess.Popen(['play', "explain{}.mp3".format(exNum)]) as p:  
            p.wait()

        print("prgVoice end")

        time.sleep(.7)
        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: white;}"
            )
        self.progressBard.show()

        time.sleep(.1)

        self.guideBt.setEnabled(True)
        self.guideBt.setText("???????????? ???")
        # self.guideBt.clicked.connect(self.onGuideBtClicked)
        self.guideBt.setStyleSheet("background:#F06292;")
        self.guideBt.show()

        print("?????????????????? :",time.time()-startExplainTime)


    def thRun(self):                              # ?????? Thread - progress_bar
        print("????????????(thread): ", self.rtime)

        progressValue = 0
        self.progressBard.setEnabled(True)
        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: #05B8CC;}"
            )
        self.progressBard.setMaximum(100)
        self.progressBard.setProperty("value", progressValue)
        self.progressBard.setObjectName("progressBard")
        self.progressBard.setTextVisible(False)
        self.progressBard.show()

        while progressValue <= 100:
            self.progressBard.setProperty("value", progressValue)
            self.progressBard.show()
            progressValue += 1
            
            # step = tuple(np.round(((self.destination[0]-self.now[0])/100, (self.destination[1]-self.now[1])/100), 3))
            # self.now = tuple(np.round((self.now[0]+step[0], self.now[1]+step[1]), 3))

            # print("??????:",self.now, "/ ?????????:",self.destination)

            time.sleep(self.rtime/101)


    def thExplain(self):#, exNum):                  # ?????? Thread - progress_bar
        print("????????????(thread): ", self.etime)

        progressValue = 0
        self.progressBard.setEnabled(True)
        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: pink;}"
            )
        self.progressBard.setMaximum(100)
        self.progressBard.setProperty("value", progressValue)
        self.progressBard.setObjectName("progressBard")
        self.progressBard.setTextVisible(False)
        self.progressBard.show()

        while progressValue <= 100:
            self.progressBard.setProperty("value", progressValue)
            self.progressBard.show()
            progressValue += 1
            time.sleep(self.etime/101)
        

    def onExitBtClicked(self):
        print("Bye")
        QCoreApplication.instance().quit()


    # def movingInfo(self, moveStart, moveEnd, speed=0.675):    # ????????????
    #     # moveStart = (2,2)
    #     # moveEnd = (1,1)

    #     if (moveEnd[0]-moveStart[0])==0:
    #         if moveEnd[1] > moveStart[1]:
    #             moveAngle = 0 
    #         else:
    #             moveAngle = 180
    #     else:
    #         angle = int(round(np.arctan((moveEnd[1]-moveStart[1])/(moveEnd[0]-moveStart[0]))*180/np.pi,1))
    #         moveAngle = 90-angle if angle>180 else 270-angle

    #     print("?????? ", "{} ??? {}".format(moveStart,moveEnd))

    #     print("??????:", moveAngle, end=" / ")

    #     distance = ((moveEnd[1]-moveStart[1])**2+(moveEnd[0]-moveStart[0])**2)**0.5
    #     print("??????: %.2f"%distance, end=" / ")

    #     speed = 0.3
    #     print("??????: %.2fs"%(distance/speed), "\n\n")


    def userAction(self, text):
        print(text)

        if text.find("??????") != -1 or text.find("??????") != -1: self.voice(0); self.onButtonClicked(0)
        elif text.find("??????") != -1: self.voice(1); self.onButtonClicked(1)
        elif text.find("??????") != -1 or text.find("??????") != -1: self.voice(2); self.onButtonClicked(2)
        elif text.find("??????") != -1 or text.find("??????") != -1 : self.voice(3); self.onButtonClicked(3)
        elif text.find("??????") != -1: self.voice(4); self.onButtonClicked(4)
        elif text.find("?????????") != -1: self.voice(5); self.onButtonClicked(5)
        elif text.find("??????") != -1: self.voice(6); self.onButtonClicked(6)
        elif text.find("?????????") != -1: self.voice(7); self.onButtonClicked(7)
        elif text.find("??????") != -1 or text.find("??????") != -1 : self.voice(8); self.onButtonClicked(8)
        elif text.find("?????????") != -1: self.voice(9); self.onButtonClicked(9)
        elif text.find("??????") != -1: self.voice(11); self.onButtonClicked(11)
        elif text.find("??????") != -1: self.voice(12); self.onButtonClicked(12)
        elif text.find("??????") != -1: 
            self.voice((self.nowNum+1)%13)
            self.onButtonClicked((self.nowNum+1)%13)

        if text.find("??????") != -1 or text.find("??????") != -1 or text.find("??????") != -1 or text.find("????????????") != -1 or text.find("??????") != -1 or text.find("??????") != -1 or text.find("??????") != -1 or text.find("??????") != -1:

            self.onGuideBtClicked()

            # bot.forward()
            # action = True

        # return True

    def voice(self, voiceNum):
        self.nowNum = voiceNum

        voiceName = "voice/voiceDest{}.mp3".format(voiceNum)#self.btNum)
        with subprocess.Popen(['play', voiceName]) as p:        # gtts?????? ?????? - '??????'???
            p.wait()

        with subprocess.Popen(['play', "voice/mainVoice1.mp3"]) as p1:  # ???????????????
            p1.wait()

    def gAssist(self):
        self.stream = create_conversation_stream()
        self.ga = GAssistant(self.stream, local_device_handler=self.userAction)

    def gA(self):
        try:
            while True:
                self.ga.assist(self.onStart)
        except:
            pass

    def onStart(self): 
        print(">>> Start recording....")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = mapping(width = 80, height = 40)

    th0 = Thread(target=map.getAngle)
    th1 = Thread(target=map.check_lidar)
    th2 = Thread(target=map.get_signal)
    th0.daemon = True
    th1.daemon = True
    th2.daemon = True
    th0.start()
    th1.start()
    th2.start()
    th2.join()

    time.sleep(1)
    
    roadmapWindow = RoadmapWindow()
    roadmapWindow.showFullScreen()
    sys.exit(app.exec_())



# ????????? ?????? :
# ?????? ??????????????? (?????? ???????????????) - ?????? ??? 287???
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612303&ccbaKdcd=11&ccbaAsno=02870000&ccbaCtcd=34

# ????????? ?????? ?????? (????????? ?????? ??????) - ?????? ??? 154???
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612272&ccbaKdcd=11&ccbaAsno=01540000&ccbaCtcd=34

# ????????? ???????????? (????????? ????????????) - ?????? ??? 156???
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612276&ccbaKdcd=11&ccbaAsno=01560000&ccbaCtcd=34

# ????????? ?????? ????????? (????????? ?????? ???) - ?????? ??? 159???
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612282&ccbaKdcd=11&ccbaAsno=01590000&ccbaCtcd=34


# ????????? (king)
# https://namu.wiki/w/?????????

# activity (play)
# http://www.icommune.co.kr/portfolio_page/?????????????????????-?????????/

# shop
# https://nukilee.tistory.com/entry/??????-??????-?????????-??????-??????-?????????-?????????-????????????-?????????????????????-????????????????????????



# %%
