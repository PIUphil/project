import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QGroupBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QCoreApplication
from PIL import Image
#from pop.CAN import OmniWheel

#omni = OmniWheel()

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

    # 길 표시
    def loadRoad(self):
        self.label = QLabel(self)
        self.label.move(120,20)
        self.label.resize(500,681)

        img = Image.open('../notebook/mapLine.png')
        img_resize = img.resize((int(img.width *0.87), int(img.height *0.87)))
        img_resize.save('mapLine_resize.png')

        self.label.setPixmap(QPixmap("mapLine_resize.png"))  # map, mapLine
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
            bt.append(QPushButton(btName[i], self))
            bt[i].move(130+(120*i),20)
            bt[i].resize(120,100)
            bt[i].setStyleSheet("background-color: rgba(255, 255, 255, 0%)")#, border-width: 0px")
            # bt[i].hover()
            # bt[i].l.hover.pressed()
            bt[i].clicked.connect(btconnect[i])
        
        for i in range(4):            
            bt.append(QPushButton(btName[3+i], self))
            bt[3+i].move(130,130+(105*i))
            bt[3+i].resize(120,100)
            bt[3+i].setStyleSheet("background:transparent")#"background-color: rgba(255, 255, 255, 0%)")
            bt[3+i].clicked.connect(btconnect[i])

        for i in range(4):            
            bt.append(QPushButton(btName[7+i], self))
            bt[7+i].move(370,130+(105*i))
            bt[7+i].resize(120,100)
            bt[7+i].setStyleSheet("background-color: rgba(255, 255, 255, 0%)")
            bt[7+i].clicked.connect(btconnect[i])
            
    def onChargeBtClicked(self):
        pass
    def onPhotoBtClicked(self):
        pass
    def onWcBtClicked(self):
        pass
    def onEx0BtClicked(self):
        pass
    def onEx1BtClicked(self):
        pass
    def onEx2BtClicked(self):
        pass
    def onEx3BtClicked(self):
        pass
    def oc(self):
        pass
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
