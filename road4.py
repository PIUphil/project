import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QProgressBar
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt, noshowbase, QRect
from PIL import Image
#from pop.CAN import OmniWheel

#from pop import TempHumi

#from . import mapLine

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#%matplotlib inline
#%%

import time

#omni = OmniWheel()



class RoadmapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roadmap")
        self.init()

    def init(self):
        self.destination = self.now = (14,30)
        
        # 바탕(흰색)
        baseLabel = QLabel(self)
        baseLabel.move(0,0)
        baseLabel.resize(1280,720)
        baseLabel.setPixmap(QPixmap("pic/base.png"))

        # 지도
        self.label = QLabel(self)
        self.label.move(55,20)
        self.label.resize(450,684)

        img = Image.open('../notebook/map.png')
        img_resize = img.resize((int(img.width *1.142), int(img.height *1.142)))
        img_resize.save('map_resize.png')
        self.label.setPixmap(QPixmap("map_resize.png"))  # map, mapLine

        # 레이블
        label_text = QLabel(self)
        label_text.setText(" 지도에서 목적지를 클릭하세요")
        label_text.move(535,10)
        label_text.resize(1000,90)
        label_text.setFont(QFont('MesloLGS NF', 40))

        # 사진
        self.label_pic = QLabel(self)
        self.label_pic.move(530,100)
        self.label_pic.resize(680,480)
        self.label_pic.setPixmap(QPixmap("pic/tomb.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)

        # 안내버튼
        self.guideBt = QPushButton("안내시작 墳",self)
        self.guideBt.move(620,600)
        self.guideBt.resize(500,100)
        self.guideBt.clicked.connect(self.onGuideBtClicked)
        self.guideBt.setStyleSheet("background:#F06292;")
        self.guideBt.setFont(QFont('MesloLGS NF', 45))

        # 종료
        exitBt = QPushButton("X",self)
        exitBt.move(1180,0)
        exitBt.resize(100,100)
        exitBt.clicked.connect(self.onExitBtClicked)
        exitBt.setStyleSheet("background:transparent; border:0px")
        exitBt.setFont(QFont('MesloLGS NF', 25))

        self.destButton()



    def drawRoad(self, now, destination=(14,30)):
        self.destination = destination
        height = 32
        self.runLength = 0              # 주행거리

        way = []
        for i in range(6):
            way.append((10,2+5*i))
        
        fig, ax = plt.subplots(figsize=(6, 12), constrained_layout=True)

        mapImage = plt.imread("../notebook/map.png")
        ax_map = ax.twinx()
        ax_map.set_xlim(ax.get_xlim())
        ax_map.set_ylim(ax.get_ylim())

        om = OffsetImage(mapImage, zoom=1.31)#1.2899, alpha=1)         # 이미지 삽입 준비
        box0 = AnnotationBbox(om, (8*0.96, 16*0.993), frameon=False) # 이미지 삽입 좌표 지정, 테두리 삭제
        ax_map.add_artist(box0)                          # 이미지 삽입

        ax_map.axis(False)                               # 배경 이미지 눈금 안보이게
        ax_map.set_zorder(-1)                            # 배경 이미지 axes를 메인 axes뒤로
        ax.set_facecolor("none") 

        line_color = "blue"
        height=32

        # 테두리
        # ax.plot([0, 16], [0, 32], color="red")
        # ax.plot([0, 16], [32, 0], color="red")
        ax.plot([0, 16], [0, 0], color="black")
        ax.plot([0, 16], [32, 32], color="black")
        ax.plot([0, 0], [0, 32], color="black")
        ax.plot([16, 16], [0, 32], color="black")

        
        # 길 그리기
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

        plt.savefig('mapLine.png')   # 이미지파일 저장

        img = Image.open('mapLine.png')
        img_resize = img.resize((int(img.width *0.6255), int(img.height *0.6255)))
        img_resize.save('mapLine.png')


    # 길 표시
    def loadRoad(self):
        self.label = QLabel(self)
        self.label.move(120,20)
        self.label.resize(500,681)
        self.label.setPixmap(QPixmap("mapLine.png"))  # map, mapLine
        self.label.show()

    
    # 도착지 [클릭]
    def destButton(self):
        self.bt = []
        self.nm = []
        self.nameLabel=['충전소','포토존','화장실\n/ 출구','금제관식', '금귀걸이', '금동대향로', '금제뒤꽂이','무덤모형','기념품샵','체험관2','체험관1','역사관','입구']
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


        for i in range(3):                      # 충전,사진,화장실            
            self.bt[i].move(130+(120*i),20)
            self.nm[i].move(139+(142*i),20)
        
        for i in range(5):                      # 작품,무덤모형
            self.bt[3+i].move(130,130+(105*i))
            self.nm[3+i].move(145,150+(105*i))

        for i in range(4):                      # 기타
            self.bt[8+i].move(400,130+(105*i))
            self.nm[8+i].move(405,150+(105*i))

        self.bt[12].move(355,588)               # 입구
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


    def onButtonClicked(self, btNum):   # 버튼 동작 - 노선 이미지 출력
        destinationList = [(11,29.5), (1.5,1), (8,0.5), (13.5,0.5), (0.5,7), (0.5,12), (0.5,17), (0.5,22), (0.5,27), (14.5,7), (14.5,12), (14.5,17), (14.5,22)]
        pictureNameList = ["start.png", "charge.png", "photo.png", "wc.png", "crown.png", "earring.png", "thurible.png", "headdress.png", "tomb.png", "shop.png", "activity2.png", "activity1.png", "king.png"]

        self.drawRoad(self.now, destinationList[btNum])
        self.loadRoad()
        self.label_pic.setPixmap(QPixmap("pic/"+pictureNameList[btNum]))
        self.label_pic.setAlignment(Qt.AlignCenter)
        self.raiseBt()
        print(pictureNameList[btNum][:-4]+" button clicked")


    def raiseBt(self):                  # 레이블, 버튼을 최상위로 이동
        for i in range(13):
            self.nm[i].raise_()
        for i in range(13):
            self.bt[i].raise_()
            
    
    def guiding(self):                  # 노선에 따라 서봇이미지 이동 - 미구현(실시간으로 표현불가)
        self.label_guide = QLabel(self)
        self.label_guide.move(133+(21.81*self.now[0])-20, 20+(21.094*self.now[1])-30)
        self.label_guide.resize(46,60)
        self.label_guide.setPixmap(QPixmap("pic/serbot1.png"))
        self.label_guide.setAlignment(Qt.AlignCenter)
        self.label_guide.show()
        self.label_guide.raise_()
        time.sleep(.3)

    
    def onGuideBtClicked(self):         # 안내시작버튼 클릭
        print("guide")
        # print(now[0], now[1])

        print("주행거리 :",self.runLength)

        print(self.now, self.destination)

        self.guideBt.setEnabled(False)
        self.guideBt.setStyleSheet("background:Gray; color:White;")
        self.guideBt.show()

        step = tuple(np.round(((self.destination[0]-self.now[0])/100, (self.destination[1]-self.now[1])/100), 3))
        #print(step)

        # self.guiding()

        # 진행도 표시
        progressValue = 0
        self.progressBard = QProgressBar(self)
        self.progressBard.setEnabled(True)
        self.progressBard.setGeometry(QRect(620, 585, 500, 15))
        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: #05B8CC;}"
            )
        self.progressBard.setMaximum(100)
        self.progressBard.setProperty("value", progressValue)
        self.progressBard.setObjectName("progressBard")
        self.progressBard.setTextVisible(False)
        self.progressBard.show()

        while True:            
            self.now = tuple(np.round((self.now[0]+step[0], self.now[1]+step[1]), 3))
            # time.sleep(.03)
            progressValue += 1      #step
            self.progressBard.setProperty("value", progressValue)
            self.progressBard.show()
            time.sleep(self.runLength/201)      # /101
            #print(self.now, self.destination)

            if progressValue == 100:
                time.sleep(.7)

            if tuple(np.round((self.now), 1)) == tuple(np.round((self.destination), 1)):
                self.now = tuple(np.round((self.destination), 1))
                break
            # else:
            #     self.label_guide.destroy()
        
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

        if self.destination   == (0.5,7):   self.explain(0)
        elif self.destination == (0.5,12):  self.explain(1)
        elif self.destination == (0.5,17):  self.explain(2)
        elif self.destination == (0.5,22):  self.explain(3)
        elif self.destination == (14.5,22): self.explain(4)

        self.raiseBt()


    def explain(self,exNum):                    # 작품설명
        explainTime = [16,17,18,19,20]          # 설명시간 - (금제관식,귀걸이,향로,뒤꽂이,무령왕)
        print("설명시간 : {}초".format(explainTime[exNum]))

        startExplainTime = time.time()

        self.guideBt.setText(" 설  명  墳")
        self.guideBt.setStyleSheet("background:Gray; color:White;")
        self.guideBt.setEnabled(False)
        self.guideBt.show()

        time.sleep(.5)
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
            time.sleep(explainTime[exNum]/201)      # /101

        time.sleep(.7)
        self.progressBard.setStyleSheet(
            "QProgressBar {border:transparent;}"
            "QProgressBar::chunk {background-color: white;}"
            )
        self.progressBard.show()

        time.sleep(.1)

        self.guideBt.setEnabled(True)
        self.guideBt.setText("안내시작 墳")
        # self.guideBt.clicked.connect(self.onGuideBtClicked)
        self.guideBt.setStyleSheet("background:#F06292;")
        self.guideBt.show()

        print("실제설명시간 :",time.time()-startExplainTime)

    def onExitBtClicked(self):
        print("Bye")
        QCoreApplication.instance().quit()


    def movingInfo(self, moveStart, moveEnd, speed=0.675):
        # moveStart = (2,2)
        # moveEnd = (1,1)

        if (moveEnd[0]-moveStart[0])==0:
            if moveEnd[1] > moveStart[1]:
                moveAngle = 0 
            else:
                moveAngle = 180
        else:
            angle = int(round(np.arctan((moveEnd[1]-moveStart[1])/(moveEnd[0]-moveStart[0]))*180/np.pi,1))
            moveAngle = 90-angle if angle>180 else 270-angle

        print("이동 ", "{} → {}".format(moveStart,moveEnd))

        print("각도:", moveAngle, end=" / ")

        distance = ((moveEnd[1]-moveStart[1])**2+(moveEnd[0]-moveStart[0])**2)**0.5
        print("거리: %.2f"%distance, end=" / ")

        speed = 0.3
        print("시간: %.2fs"%(distance/speed), "\n\n")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    roadmapWindow = RoadmapWindow()
    roadmapWindow.showFullScreen()
    sys.exit(app.exec_())



# 이미지 출처 :
# 백제 금동대향로 (百濟 金銅大香爐) - 국보 제 287호
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612303&ccbaKdcd=11&ccbaAsno=02870000&ccbaCtcd=34

# 무령왕 금제 관식 (武寧王 金製 冠飾) - 국보 제 154호
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612272&ccbaKdcd=11&ccbaAsno=01540000&ccbaCtcd=34

# 무령왕 금귀걸이 (武寧王 金製耳飾) - 국보 제 156호
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612276&ccbaKdcd=11&ccbaAsno=01560000&ccbaCtcd=34

# 무령왕 금제 뒤꽂이 (武寧王 金製 釵) - 국보 제 159호
# http://www.heritage.go.kr/heri/cul/imgHeritage.do?ccimId=1612282&ccbaKdcd=11&ccbaAsno=01590000&ccbaCtcd=34


# 무령왕 (king)
# https://namu.wiki/w/무령왕

# activity (play)
# http://www.icommune.co.kr/portfolio_page/백제오감체험관-전시관/

# shop
# https://nukilee.tistory.com/entry/백제-문화-유적지-충남-공주-송산리-고분군-무령왕릉-백제오감체험관-유네스코세계유산



# %%
