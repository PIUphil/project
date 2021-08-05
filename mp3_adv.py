from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QDial, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.Qt import Qt

def get_filelist(path, ext='mp3'):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(ext)]


class SliderProxyStyle(QtWidgets.QProxyStyle):
    def pixelMetric(self, metric, option, widget):
        if metric == QtWidgets.QStyle.PM_SliderThickness:
            return 100
        elif metric == QtWidgets.QStyle.PM_SliderLength:
            return 80
        return super().pixelMetric(metric, option, widget)


class MainWindow(QWidget):
    PATH = 'music'

    def __init__(self):
        super().__init__()

        self.setStyleSheet('QWidget {background-color:#afddec}')

        self.playlist = QMediaPlaylist()
        QDir.setCurrent(self.PATH)
        for name in get_filelist('./'):
            url = QUrl.fromLocalFile(QDir.current().absoluteFilePath(name))
            self.playlist.addMedia(QMediaContent(url))
        
        self.playlist.setCurrentIndex(0)
        self.playlist.currentIndexChanged.connect(self.onCurrentIndexChanged)    
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)

        self.player.setVolume(40)
        self.player.mediaStatusChanged.connect(self.onStatusChanged)
        self.player.positionChanged.connect(self.onPositionChanged)
        self.player.durationChanged.connect(self.onDurationChanged)
        self.__duration = 0

        layout = QVBoxLayout()
        inner = QHBoxLayout()

        layout.addItem(inner)

        for title, slot in {'': self.onPrev, '':self.onPlay, '':self.onPause, '':self.onNext, '':self.onStop}.items():
            pb = QPushButton(title)
            pb.clicked.connect(slot)
            pb.setFont(QFont('MesloLGS NF', 130))
            pb.resize(100, 300)
            pb.setStyleSheet('QPushButton {background-color:#5c0da9; color: white}')
            inner.addWidget(pb)
        
        inner2 = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        style = SliderProxyStyle(self.slider.style())
        self.slider.setStyle(style)
        self.slider.valueChanged.connect(self.onSlider)

        self.lbSlider = QLabel('00:00')
        self.lbSlider.setFont(QFont('DS-Digital', 80))
        self.lbSlider.setStyleSheet('QLabel {color: #5c0da9}')
        
        inner2.addWidget(self.slider)
        inner2.addWidget(self.lbSlider)
        layout.addItem(inner2)

        vol = QDial()
        vol.setRange(0, 100)
        vol.setValue(self.player.volume())
        vol.valueChanged.connect(self.onVolum)
        layout.addWidget(vol)

        pb = QPushButton('Exit')
        pb.setStyleSheet('QPushButton {background-color:#5c0da9; color: #afddec}')
        pb.clicked.connect(self.onExit)
        pb.setFont(QFont('DS-Digital', 80))
        layout.addWidget(pb)
        self.setLayout(layout)

    def onCurrentIndexChanged(self, index):
        if index == -1 and self.player.state() == QMediaPlayer.PlayingState:
            self.playlist.setCurrentIndex(0)
            self.player.play()

    def onPositionChanged(self, pos):
        self.slider.setValue(pos)
        millis = int(pos)
        seconds = (millis/1000)%60
        minutes = (millis/(1000*60))%60
        self.lbSlider.setText("%02d:%02d"%(minutes, seconds))
        
    def onStatusChanged(self, stat):
        pass

    def onDurationChanged(self, duration):
        self.__duration = duration
        self.slider.setRange(0, duration)
    
    def onPrev(self):
        self.playlist.previous()

    def onPlay(self):
        self.player.play()

    def onPause(self):
        self.player.pause()

    def onNext(self):
        self.playlist.next()

    def onStop(self):
        self.player.stop()

    def onSlider(self, pos):
        self.player.setPosition(pos)

    def onVolum(self, vol):
        self.player.setVolume(vol)

    def onExit(self):
        if not self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()

        QCoreApplication.instance().quit()

if __name__ == '__main__':
    if True:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.showFullScreen()
        sys.exit(app.exec_())
    else:
        print(get_filelist('music'))

