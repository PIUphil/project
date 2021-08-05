import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

import torch
from PIL.ImageQt import ImageQt
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
        self.model.eval()
        self.model.to('cuda')
        
        self.frame = QLabel(self)
        self.frame.resize(1280, 720)
        
        self.deepLabV3()
    
    def deepLabV3(self):
        from torchvision import transforms

        input_image = Image.open("dog.jpg")
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) #create a mini-batch as expected by the model
        
        input_batch = input_batch.to('cuda')
        
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
