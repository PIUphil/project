import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
#from PyQt5.QtMultimedia import QMediaPlayer
#import pyglet
from popAssist import create_conversation_stream
from popAssist import GAssistant


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 버튼
        self.stat = True
        self.bt = QPushButton("Start", self)
        self.bt.move(300,50)
        self.bt.resize(700,400)
        self.bt.setFont(QFont('',100))
        self.bt.clicked.connect(self.onPB)

        # 레이블
        self.lbl = QLabel(self)
        self.lbl.move(300,480)
        self.lbl.resize(700,200)
        self.lbl.setFont(QFont('',50))


    def onPB(self):
        self.bt.setText("Listening")
        self.bt.setEnabled(False)

        stream = create_conversation_stream()
        ga = GAssistant(stream, local_device_handler=self.onAction)

        ga.assist()

        stream.close()

        self.bt.setText("ReStart")
        self.bt.setEnabled(True)
            

    def onAction(self,text):
        # print(text)
        self.lbl.setText(text)
        return True             # True: 오디오 응답 안함 
    

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())