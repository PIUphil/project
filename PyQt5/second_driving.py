import sys 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
from pop.CAN import OmniWheel

omni = OmniWheel()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        #self.showFullScreen()
        self.move(0,0)
        self.resize(1280,720)
        self.setWindowTitle("Drive")
        self.init()
        self.show()

    def init(self):

        #그룹위젯(테두리)
        gb1 = QGroupBox(self)
        gb1.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        gb1.move(20,35)
        gb1.resize(750, 600)

        gb2 = QGroupBox(self)
        gb2.setStyleSheet("color: green;"
                       "background-color: #6FE392;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1A863A")
        gb2.move(783,35)
        gb2.resize(477, 600)


        # 체크박스
        self.cb = QCheckBox("  Forward", self)      # Clockwise
        self.cb.move (50, 60)
        self.cb.setFont(QFont('Arial', 50))
        self.cb.setStyleSheet("QCheckBox::indicator {width : 50px; height : 50px;}")
        self.cb.stateChanged.connect(self.onCbChanged)
        #self.cb1.show()

        self.motorEdit = []

        # 레이블
        lbl = []
        for i in range(3):
            lbl.append(QLabel(self))             # 레이블(글씨)
            lbl[i].setText("Motor"+i+1)
            lbl[i].move(50,150)
            lbl[i].setFont(QFont('Arial', 50))

        lbl2 = QLabel(self)            
        lbl2.setText("Motor2")
        lbl2.move(50,250)
        lbl2.setFont(QFont('Arial', 50))

        lbl3 = QLabel(self)             
        lbl3.setText("Motor3")
        lbl3.move(50,350)
        lbl3.setFont(QFont('Arial', 50))

        # 라인edit
        self.le1 = QLineEdit(self)
        self.le1.move(320, 145)
        self.le1.setText("20")
        self.le1.setFont(QFont('Arial', 50))

        self.le2 = QLineEdit(self)
        self.le2.move(320, 245)
        self.le2.setText("20")
        self.le2.setFont(QFont('Arial', 50))

        self.le3 = QLineEdit(self)
        self.le3.move(320, 345)
        self.le3.setText("20")
        self.le3.setFont(QFont('Arial', 50))


        # 버튼
        bt = []
        btName=['start','stop','exit']
        btconnect = [self.onStartBtClicked, self.onStopBtClicked, self.onExitBtClicked]
        
        for i in range(3):            
            bt.append(QPushButton(btName[i], self))
            bt[i].move(50+(238*i),460)
            bt[i].resize(225,150)
            bt[i].clicked.connect(btconnect[i])
            bt[i].setFont(QFont('Arial', 50))


        # 숫자키패드
        self.btNum = []
        for i in range(12):
            setNum = ['1','2','3','4','5','6','7','8','9','←','0','▼'] 
            self.btNum.append(QPushButton(setNum[i], self))
            self.btNum[i].move(804+(150*(i%3)),60+(140*(i//3)))
            self.btNum[i].resize(140,130)
            self.btNum[i].setFont(QFont('Arial', 50))

    
    def onStartBtClicked(self):
        print("Clicked Start Button")
        SPEED = [int(self.le1.text()), int(self.le2.text()), int(self.le3.text())]

        if(self.clockwise):
            omni.forward(SPEED)
            fb = "Forward"
        else:
            omni.backward(SPEED)
            fb = "Backward"

        print("START " + fb + " " + str(SPEED))
    
    def onStopBtClicked(self):
        omni.stop()
        print("STOP")

    def onExitBtClicked(self):
        print("Bye")
        QCoreApplication.instance().quit()


    def onCbChanged(self, state):
        print("changed checkbox1", state)       # 0, 2, 1
        self.clockwise = state/2


if __name__ == '__main__':
    app = QApplication(sys.argv)   # argv : 인자 (리스트; 프로그램이름,옵션들)
    ex = MyApp()
    sys.exit(app.exec_())          # 프로그램(sys) 강제종료

