import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
#from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
from threading import Thread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        cam_cmd = lambda cam_with=1280, cam_height=720, win_with=1280, win_height=720, rate=60, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)

        self.cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)

        self.frame = QLabel(self)
        self.frame.resize(1280, 720)

        def timer():
            while True:
                self.onFrame()
        
        th = Thread(target=timer)
        th.daemon = True
        th.start()

        # 버튼
        self.bt = QPushButton("X", self)
        self.bt.move(1180,0)
        self.bt.resize(100,100)
        self.bt.setFont(QFont('',70))
        self.bt.clicked.connect(self.onPB)        

    def __del__(self):
        pass
        # if self.capTimer.isActive():
        #     self.capTimer.stop()
        # self.cam.release()
        # QCoreApplication.instance().quit()


    def onFrame(self):
        ret, frame = self.cam.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        h,w,c = img.shape
        qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.frame.setPixmap(pixmap)

    def onPB(self):
        # if self.capTimer.isActive():
        #     self.capTimer.stop()
        self.cam.release()
        QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())