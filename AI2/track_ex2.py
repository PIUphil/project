import sys
import cv2
from threading import Thread


from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication

from pop import Pilot 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        cam_cmd = lambda cam_width=640, cam_height=480, win_width=640, win_height=480, rate=60, flip=0 : ('nvarguscamerasrc ! '
                    'video/x-raw(memory:NVMM), '
                    'width={0}, height={1}, '
                    'format=NV12, framerate={2}/1 ! '
                    'nvvidconv flip-method={3} ! '
                    'video/x-raw, width={4}, height={5}, '
                    'format=BGRx ! '
                    'videoconvert ! appsink').format(cam_width, cam_height, rate, flip, win_width, win_height)

        self.cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)
        self.bot = Pilot.SerBot() 

        self.of = Pilot.Object_Follow2(self.cam, 640, 480)
        self.of.load_model()
        
        self.frame = QLabel(self)
        self.frame.resize(1280, 720)

        self.__is_run = True
        self.thread = Thread(target=self.__onObjectFollow2)
        self.thread.daemon = True
        self.thread.start()

        self.pbExit = QPushButton('Exit', self)
        self.pbExit.resize(120, 60)
        self.pbExit.setFont(QFont('', 50))
        self.pbExit.clicked.connect(self.onExit)
    
    def onExit(self):
        self.__is_run = False
        self.thread.join()
        self.cam.release()
        
        self.bot.stop()

        QCoreApplication.instance().quit()


    def __onObjectFollow2(self):
        while self.__is_run:
            a, image = self.of.detect(index='person')
        
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
            h,w,c = image.shape
            pixmap = QPixmap.fromImage(QImage(image.data, w, h, w * c, QImage.Format_RGB888))
            self.frame.setPixmap(pixmap)
        
            if a is not None: 
                steer = a['x'] * 4 
                if steer > 1:
                    steer = 1
                elif steer < -1:
                    steer = -1
                
                self.bot.steering = steer

                if a['size_rate'] < 0.2:
                    self.bot.forward(50)
                else:
                    self.bot.stop()
            else:
                self.bot.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
