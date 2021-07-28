import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QCoreApplication
import time
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)

saveFile = ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def __del__(self):
        if self.checkTimer.isActive():
            self.checkTimer.stop()

    def init(self):
        self.checkTimer = QTimer()
        self.checkTimer.setInterval(100)
        self.checkTimer.timeout.connect(self.tableTimer)
        self.checkTimer.start()

        lbHeader = ['Time']
        lbHeader += ['D' + str(i) for i in range(10)]

        self.tbDatas = QTableWidget(self)
        self.tbDatas.setColumnCount(10+1)
        self.tbDatas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbDatas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbDatas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbDatas.setHorizontalHeaderLabels(lbHeader)
        self.tbDatas.setFixedHeight(500)
        self.tbDatas.setMinimumWidth(1280)

        # 버튼
        bt = []
        btName=['Start','Stop','Save','Exit']
        btconnect = [self.onStartBtClicked, self.onStopBtClicked, self.onSaveBtClicked, self.onExitBtClicked]
        
        for i in range(4):            
            bt.append(QPushButton(btName[i], self))
            bt[i].move(50+(270*i),530)
            bt[i].resize(225,150)
            bt[i].clicked.connect(btconnect[i])
            bt[i].setFont(QFont('Arial', 50))


    def tableTimer(self):
        ret = ser.readline()
        global saveFile
        
        if ret:
            data = ret.decode()[:-3]
            saveFile += data+"\n"
        
        tt = time.strftime('%y-%m-%d  %H:%M:%S', time.localtime(time.time()))

        self.setTableData(tt, data.split(","))

    def setTwItem(self, row, column, data):
        item = QTableWidgetItem(str(data))
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(90,90,90))
        item.setBackground(QColor(250,250,250))
        item.setFont(QFont('', 20))
        self.tbDatas.setItem(row, column, item)

    def setTableData(self, t, data):               
        row = self.tbDatas.rowCount()
        self.tbDatas.insertRow(row)
        
        self.setTwItem(row, 0, t)        
        for i in range(10): 
            self.setTwItem(row, i+1, data[i])
            
        self.tbDatas.selectRow(row)


    def onStartBtClicked(self):
        self.checkTimer.start()
    
    def onStopBtClicked(self):
        self.checkTimer.stop()

    def onSaveBtClicked(self):
        global saveFile
        tt = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        f = open("/home/soda/Project/python/qt5"+tt+".csv",'a')
        f.write(saveFile)
        f.close()

    def onExitBtClicked(self):
        print("Bye")
        QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
