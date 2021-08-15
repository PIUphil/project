import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QGroupBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from PIL import Image
#from pop.CAN import OmniWheel

#from . import mapLine

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#%matplotlib inline
#%%

#omni = OmniWheel()

now = (14,30)


def drawRoad(now, destination):    
    height = 32
    way = {}
    for i in range(6):
        way[i] = (10,2+5*i)
    
    fig, ax = plt.subplots(figsize=(6, 12), constrained_layout=True)

    mapImage = plt.imread("https://user-images.githubusercontent.com/58851945/129303985-904380be-ac20-4147-af66-098ed1f06b47.png")
    #mapImage = plt.imread("map.png")
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
    ax.fill([now[0], now[0], now[0]+1, now[0]+1], [height-now[1]-1, height-now[1], height-now[1], height-now[1]-1], color='red')              # now
    ax.text(now[0]+0.17, height-now[1]-1-0.4, 'Now', fontdict={'family':'serif', 'color':'black', 'weight':'bold'})

    up = False
    go_way = []
    if now[1] >= destination[1]:
        up = True

    for i in list(way.values()):
        if up:
            if now[1] >= i[1]:
                go_way.append(i)
        else:
            if now[1] <= i[1]:
                go_way.append(i)

    length_way_now = [((now[0]-i[0])**2+(now[1]-i[1])**2)**0.5 for i in go_way]#list(way.values())]
    min_length_way_now = min(length_way_now)
    way_now = go_way[np.argmin(length_way_now)]

    length_way_ex = [((destination[0]-i[0])**2+(destination[1]-i[1])**2)**0.5 for i in list(way.values())]
    min_length_way_ex = min(length_way_ex)
    way_ex = way[np.argmin(length_way_ex)]


    line_color = "blue"

    if (way_now==way_ex) and (now[1]-destination[1])**2<5:
        ax.plot([now[0]+0.5, destination[0]+0.5], [height-now[1]-1+0.5, height-destination[1]-1+0.5], color=line_color)
    else:
        ax.plot([now[0]+0.5, way_now[0]+0.5], [height-now[1]-1+0.5, height-way_now[1]-1+0.5], color=line_color)
        ax.plot([way_now[0]+0.5, way_ex[0]+0.5], [height-way_now[1]-1+0.5, height-way_ex[1]-1+0.5], color=line_color)
        ax.plot([destination[0]+0.5, way_ex[0]+0.5], [height-destination[1]-1+0.5, height-way_ex[1]-1+0.5], color=line_color)

    plt.xlim(-0.5,16.5)
    plt.ylim(-0.5,32.5)
    ax.axis('off')

    plt.savefig('mapLine.png')   # 이미지파일 저장

    img = Image.open('mapLine.png')
    #img_resize = img.resize((int(img.width *0.87), int(img.height *0.87)))
    img_resize = img.resize((int(img.width *0.6255), int(img.height *0.6255)))
    img_resize.save('mapLine.png')
    #plt.show()

    return





class RoadmapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roadmap")
        self.init()


    def init(self):
        self.label = QLabel(self)
        self.label.move(55,20)
        self.label.resize(450,684)

        img = Image.open('../notebook/map.png')
        img_resize = img.resize((int(img.width *1.142), int(img.height *1.142)))
        img_resize.save('map_resize.png')

        self.label.setPixmap(QPixmap("map_resize.png"))  # map, mapLine
        self.label.show()

        self.destButton()

        # 레이블
        label_text = QLabel(self)
        label_text.setText(" 지도에서 목적지를 클릭하세요")
        label_text.move(550,10)
        label_text.resize(1000,90)
        label_text.setFont(QFont('Arial', 45))

        # 사진
        self.label_pic = QLabel(self)
        self.label_pic.move(530,120)
        self.label_pic.resize(680,480)
        self.label_pic.setPixmap(QPixmap("pic/tomb.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)
        self.label_pic.show()

        # 안내버튼
        startBt = QPushButton("안내시작",self)
        startBt.move(620,600)
        startBt.resize(500,100)
        startBt.clicked.connect(self.onExitBtClicked)
        startBt.setStyleSheet("background:#F06292;")
        startBt.setFont(QFont('Arial', 30))

        # 종료
        exitBt = QPushButton("X",self)
        exitBt.move(1180,0)
        exitBt.resize(100,100)
        exitBt.clicked.connect(self.onExitBtClicked)
        exitBt.setStyleSheet("background:transparent; border:0px")
        exitBt.setFont(QFont('Arial', 30))


    # 길 표시
    def loadRoad(self):
        self.label = QLabel(self)
        self.label.move(120,20)
        self.label.resize(500,681)
        self.label.setPixmap(QPixmap("mapLine.png"))  # map, mapLine
        self.label.show()

    
    # 도착지 [클릭]
    def destButton(self):
        bt = []
        exhibit = ['crown', 'earring', 'thurible', 'knife','','','','']
        btName=['charge','photo','wc']+exhibit
        btconnect = [self.onChargeBtClicked, self.onPhotoBtClicked, self.onWcBtClicked,
         self.onEx0BtClicked, self.onEx1BtClicked, self.onEx2BtClicked, self.onEx3BtClicked,
         self.oc,self.oc,self.oc,self.oc]
        
        for i in range(3):            
            bt.append(QPushButton(self))
            bt[i].move(130+(120*i),20)
            # bt[i].resize(120,100)
            # bt[i].setStyleSheet("background:transparent; border:0px")
            # bt[i].clicked.connect(btconnect[i])
        
        for i in range(4):            
            bt.append(QPushButton(self))
            bt[3+i].move(130,130+(105*i))
            # bt[3+i].resize(120,100)
            # bt[3+i].setStyleSheet("background:transparent; border:0px")#"background-color: rgba(255, 255, 255, 0%)")
            # bt[3+i].clicked.connect(btconnect[3+i])

        for i in range(4):            
            bt.append(QPushButton(self))
            bt[7+i].move(370,130+(105*i))

        for i in range(11):
            bt[i].resize(120,100)
            bt[i].setStyleSheet("background:transparent; border:0px")
            bt[i].clicked.connect(btconnect[i])
            
    def onChargeBtClicked(self):
        print("charge clicked")
        drawRoad(now, (2.5,2))
        self.loadRoad()
        self.destButton()

    def onPhotoBtClicked(self):
        print("photozone clicked")
        drawRoad(now, (8,0.5))
        self.loadRoad()
        self.destButton()

    def onWcBtClicked(self):
        print("wc clicked")
        drawRoad(now, (13.5,0.5))
        self.loadRoad()
        self.destButton()

    def onEx0BtClicked(self):
        print("ex0 clicked")
        drawRoad(now, (0.5,7))
        self.loadRoad()
        self.destButton()
        self.label_pic.setPixmap(QPixmap("pic/crown.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)


    def onEx1BtClicked(self):
        print("ex1 clicked")
        drawRoad(now, (0.5,12))
        self.loadRoad()
        self.destButton()
        self.label_pic.setPixmap(QPixmap("pic/earring.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)
        

    def onEx2BtClicked(self):
        print("ex2 clicked")
        drawRoad(now, (0.5,17))
        self.loadRoad()
        self.destButton()
        self.label_pic.setPixmap(QPixmap("pic/thurible.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)


    def onEx3BtClicked(self):
        print("ex3 clicked")
        drawRoad(now, (0.5,22))
        self.loadRoad()
        self.destButton()
        self.label_pic.setPixmap(QPixmap("pic/headdress.png"))
        self.label_pic.setAlignment(Qt.AlignCenter)

    def oc(self):
        pass


    def onExitBtClicked(self):
        print("Bye")
        QCoreApplication.instance().quit()


    #     #그룹위젯(테두리)
    #     gb1 = QGroupBox(self)
    #     gb1.setStyleSheet("color: blue;"
    #                    "background-color: #87CEFA;"
    #                    "border-style: dashed;"
    #                    "border-width: 3px;"
    #                    "border-color: #1E90FF")
    #     gb1.move(20,35)
    #     gb1.resize(750, 600)

    #     gb2 = QGroupBox(self)
    #     gb2.setStyleSheet("color: green;"
    #                    "background-color: #6FE392;"
    #                    "border-style: dashed;"
    #                    "border-width: 3px;"
    #                    "border-color: #1A863A")
    #     gb2.move(783,35)
    #     gb2.resize(477, 600)


    #     # 체크박스
    #     self.cb = QCheckBox("  Forward", self)      # Clockwise
    #     self.cb.move (50, 60)
    #     self.cb.setFont(QFont('Arial', 50))
    #     self.cb.setStyleSheet("QCheckBox::indicator {width : 50px; height : 50px;}")
    #     self.cb.stateChanged.connect(self.onCbChanged)
    #     #self.cb1.show()

    #     self.motorEdit = []

    #     # 레이블
    #     lbl = []
    #     for i in range(3):
    #         lbl.append(QLabel(self))             # 레이블(글씨)
    #         lbl[i].setText("Motor"+str(i+1))
    #         lbl[i].move(50,150)
    #         lbl[i].setFont(QFont('Arial', 50))

    #     lbl2 = QLabel(self)            
    #     lbl2.setText("Motor2")
    #     lbl2.move(50,250)
    #     lbl2.setFont(QFont('Arial', 50))

    #     lbl3 = QLabel(self)             
    #     lbl3.setText("Motor3")
    #     lbl3.move(50,350)
    #     lbl3.setFont(QFont('Arial', 50))

    #     # 라인edit
    #     self.le1 = QLineEdit(self)
    #     self.le1.move(320, 145)
    #     self.le1.setText("20")
    #     self.le1.setFont(QFont('Arial', 50))

    #     self.le2 = QLineEdit(self)
    #     self.le2.move(320, 245)
    #     self.le2.setText("20")
    #     self.le2.setFont(QFont('Arial', 50))

    #     self.le3 = QLineEdit(self)
    #     self.le3.move(320, 345)
    #     self.le3.setText("20")
    #     self.le3.setFont(QFont('Arial', 50))


    #     # 버튼
    #     bt = []
    #     btName=['start','stop','exit']
    #     btconnect = [self.onStartBtClicked, self.onStopBtClicked, self.onExitBtClicked]
        
    #     for i in range(3):            
    #         bt.append(QPushButton(btName[i], self))
    #         bt[i].move(50+(238*i),460)
    #         bt[i].resize(225,150)
    #         bt[i].clicked.connect(btconnect[i])
    #         bt[i].setFont(QFont('Arial', 50))


    #     # 숫자키패드
    #     self.btNum = []
    #     for i in range(12):
    #         setNum = ['1','2','3','4','5','6','7','8','9','←','0','▼'] 
    #         self.btNum.append(QPushButton(setNum[i], self))
    #         self.btNum[i].move(804+(150*(i%3)),60+(140*(i//3)))
    #         self.btNum[i].resize(140,130)
    #         self.btNum[i].setFont(QFont('Arial', 50))

    
    # def onStartBtClicked(self):
    #     print("Clicked Start Button")
    #     SPEED = [int(self.le1.text()), int(self.le2.text()), int(self.le3.text())]

    #     if(self.clockwise):
    #         omni.forward(SPEED)
    #         fb = "Forward"
    #     else:
    #         omni.backward(SPEED)
    #         fb = "Backward"

    #     print("START " + fb + " " + str(SPEED))
    
    # def onStopBtClicked(self):
    #     omni.stop()
    #     print("STOP")

    # def onExitBtClicked(self):
    #     print("Bye")
    #     QCoreApplication.instance().quit()


    # def onCbChanged(self, state):
    #     print("changed checkbox1", state)       # 0, 2, 1
    #     self.clockwise = state/2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    roadmapWindow = RoadmapWindow()
    roadmapWindow.showFullScreen()
    sys.exit(app.exec_())
