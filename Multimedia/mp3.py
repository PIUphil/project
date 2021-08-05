import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, QUrl, QtWidgets, QtMultimedia

if __name__ == '__main__':
    app = QApplication(sys.argv)
    filename = 'StairwayToHeaven.mp3'
    fullpath = QDir.current().absoluteFilePath(filename) 
    media = QUrl.fromLocalFile(fullpath)
    content = QMediaContent(media)
    player = QMediaPlayer()
    player.setMedia(content)
    player.play()
    sys.exit(app.exec_())
