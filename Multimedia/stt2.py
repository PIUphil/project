import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont
from popAssist import create_conversation_stream
from popAssist import GAssistant

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bl = QLabel('', self)
        self.bl.move(30, 500)
        self.bl.resize(1000, 100)
        self.bl.setFont(QFont('', 80))

        self.bt = QPushButton("Start", self)
        self.bt.move(300, 100)
        self.bt.resize(700, 300)
        self.bt.setFont(QFont('', 100))
        self.bt.clicked.connect(self.onPB)
        
        self.ga = GAssistant(create_conversation_stream(), local_device_handler=self.onAction)

    def onPB(self):
        self.ga.assist(self.onStart, self.onStop)

    def onAction(self, text):
        print("call onAction...")
        self.bl.setText(text)

        return True

    def onStart(self):
        print("call onStart...")
        self.bt.setText("Listen...")  #BUG - assist에서 join삭제
 
    def onStop(self):
        print("call onStop")
        self.bt.setText("ReStart")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())