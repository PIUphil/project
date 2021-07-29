
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap, QFont

IS_TIMER = False # Timer Event vs thread

if IS_TIMER:
    from PyQt5.QtCore import QTimer
else:
    from threading import Thread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        cam_cmd = lambda cam_with=1280, cam_height=720, win_with=1280, win_height=720, rate=30, flip=0 : ('nvarguscamerasrc ! '
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

        self.pbExit = QPushButton('Exit', self)
        self.pbExit.resize(120, 60)
        self.pbExit.setFont(QFont('', 50))
        self.pbExit.clicked.connect(self.onExit)

        if IS_TIMER:
            self.capTimer = QTimer()
            self.capTimer.setInterval(10)
            self.capTimer.timeout.connect(self.onFrame)
            self.capTimer.start()
        else:
            self._is_run = True
            self.frameThread = Thread(target=self.__onFrame)
            self.frameThread.daemon = True
            self.frameThread.start()

    def __del__(self):
        if IS_TIMER:
            if self.capTimer.isActive():
                self.capTimer.stop()

    def onExit(self):
        if not IS_TIMER:
            self._is_run = False
            self.frameThread.join()
        self.cam.release()
        QCoreApplication.instance().quit()

    def onFrame(self):
        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        h,w,c = frame.shape
        pixmap = QPixmap.fromImage(QImage(frame.data, w, h, w * c, QImage.Format_RGB888))
        self.frame.setPixmap(pixmap)

    def __onFrame(self):
        while self._is_run:
            self.onFrame()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
