import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QTimer
import time

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

    def tableTimer(self):
        self.setTableData(time.time(), [1 for _ in range(10)])

    def setTwItem(self, row,  column, data):
        item = QTableWidgetItem(str(data))
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(90,90,90))
        item.setBackground(QColor(250,250,250))
        item.setFont(QFont('', 50))
        self.tbDatas.setItem(row, column, item)

    def setTableData(self, t, data):               
        row = self.tbDatas.rowCount()
        self.tbDatas.insertRow(row)
        
        self.setTwItem(row, 0, t)        
        for i in range(10): 
            self.setTwItem(row, i+1, data[i])
            
        self.tbDatas.selectRow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())
