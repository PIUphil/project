import sys      # 시스템 모듈
from PyQt5.QtWidgets import QApplication   # 바이너리파일로 제공 - 자동생성안됨;
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel, QLineEdit

from PyQt5.QtGui import QFont

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.move(300,300)
        # self.resize(400,200)
        #self.showFullScreen()
        self.move(0,0)
        self.resize(1280,720)
        self.setWindowTitle("MyApp")
        self.init()
        self.show()

    def init(self):
        bt1 = QPushButton('Button1', self)
        bt1.move(100,30)
        bt1.resize(200,200)
        bt1.clicked.connect(self.onBt1Clicked)   # '시그널을 설정'한다
        bt1.setFont(QFont('Arial', 30))

        #bt1.show()

        cb1 = QCheckBox('Check1', self)
        cb1.move (500, 30)
        #cb1.resize(100,100)
        cb1.stateChanged.connect(self.onCb1Changed)
        cb1.setFont(QFont('Arial', 50))
        #cb1.show()

        lbl1 = QLabel(self)             # 레이블(글씨)
        lbl1.setText("Motor1")
        lbl1.move(100,500)

        # le1 = QLineEdit(self)           # 입력 상자
        # le1.move(140, 495)
        # le1.setText("100")
        self.le1 = QLineEdit(self)        # 지역변수 -> self를 붙여서 다른곳에서도 사용가능
        self.le1.move(140, 495)
        self.le1.setText("100")
        

    # 메소드 camel표기법 - 동작+이니셜대문자
    def onBt1Clicked(self):         # clicked, push, toggle
        print("Clicked button1")
        ret = self.le1.text()    # text : 문자 읽어옴
        print(int(ret))

    def onCb1Changed(self, state):
        print("changed checkbox1", state)       # 0, 2, 1


if __name__ == '__main__':
    app = QApplication(sys.argv)   # argv : 인자 (리스트; 프로그램이름,옵션들)
    ex = MyApp()
    sys.exit(app.exec_())          # 프로그램(sys) 강제종료

