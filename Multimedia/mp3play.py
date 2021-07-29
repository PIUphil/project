import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
#from PyQt5.QtMultimedia import QMediaPlayer
#import pyglet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stat = False
        self.bt = QPushButton("Play", self)
        self.bt.move(300,100)     
        self.bt.resize(700,500)
        self.bt.setFont(QFont('',100))
        self.bt.clicked.connect(self.onPB)
        #self.song = pyglet.media.load('StairwayToHeaven.mp3')

    def onPB(self):
        self.stat = not self.stat

        #self.bt.setText("Stop" if not self.stat else "Play")
        if not self.stat:
            self.bt.setText("Stop")
            #self.song.play()
        else:
            self.bt.setText("Play")
            #self.song.stop()


if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())