import sys
import cv2
from threading import Thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QCoreApplication

import torch
from PIL.ImageQt import ImageQt
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
        self.model.eval()

        cam_cmd = lambda cam_with=320, cam_height=240, win_with=320, win_height=240, rate=30, flip=0 : ('nvarguscamerasrc ! '
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

        self.__is_run = True
        self.dlThread = Thread(target=self.__OnDeepLabV3)
        self.dlThread.daemon = True
        self.dlThread.start()

        self.pbExit = QPushButton('Exit', self)
        self.pbExit.resize(120, 60)
        self.pbExit.setFont(QFont('', 50))
        self.pbExit.clicked.connect(self.onExit)
    
    def onExit(self):
        self.__is_run = False
        self.dlThread.join()
        self.cam.release()
        QCoreApplication.instance().quit()

    def __OnDeepLabV3(self):
        from torchvision import transforms

        while self.__is_run:
            ret, frame = self.cam.read()
            input_image = Image.fromarray(frame)
            preprocess = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

            input_tensor = preprocess(input_image)
            input_batch = input_tensor.unsqueeze(0) #create a mini-batch as expected by the model

            input_batch = input_batch.to('cuda')
            self.model.to('cuda')

            with torch.no_grad():
                output = self.model(input_batch)['out'][0]
            output_predictions = output.argmax(0)

            palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
            colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
            colors = (colors % 255).numpy().astype("uint8")

            r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(input_image.size)
            r.putpalette(colors)

            r = ImageQt(r)

            pixmap = QPixmap.fromImage(r)
            self.frame.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
