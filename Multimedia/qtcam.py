import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


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

        self.fram = QLabel(self)
        self.fram.resize(1280,720)

        self.capTimer = QTimer()
        self.capTimer.setInterval(10)            # 16밀리초마다 onReadFrame호출
        self.capTimer.timeout.connect(self.onFrame)
        self.capTimer.start()


    def __del__(self):
        if self.capTimer.isActive():
            self.capTimer.stop()

        self.cam.release()


    def onFrame(self):                  # QT에 카메라 데이터 넣기
        _, frame = self.cam.read()          # BGR파일임. -> RGB로 변환해야함
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h,w,c = img.shape                 # height=720, width=1280, color=3
        qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)  # 포맷(알파브렌딩 안쓰는거,,)
        pixmap = QPixmap.fromImage(qImg)    # 픽스비트맵으로 변환..
        self.fram.setPixmap(pixmap)


if __name__=='__main__':        # 인터프리터에서 실행한게 main이 맞냐,,? 직접실행한거냐..??
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    MainWindow.showFullScreen()
    sys.exit(app.exec_())       # 무한루프를 돌면서 시그널 처리
