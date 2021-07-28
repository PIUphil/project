import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class MainWindow(QMainWindow):    # QMainWindow에서 상속해옴
    def __init__(self):
        super().__init__()        # 부모 초기화
        self.init()


    def init(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1280,600)       # move를 생략하면 (0,0)으로 들어감
        self.tableWidget.setRowCount(20)          # 열(줄)의 개수
        self.tableWidget.setColumnCount(10)       # 행(칸)의 개수
        
        #self.tableWidget.setItem(0, 0, QTableWidgetItem("Hi, PyQt Example"))   # 행, 열, 테이블위젯아이템(문자열)
        for i in range(20):
            for j in range(10):
                self.tableWidget.setItem(i,j,QTableWidgetItem(str(i+j)))

if __name__ =='__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showFullScreen()
    # r = app.exec_()             # 종료 (시그널 처리)
    # sys.exit(r)                 # 종료 (이벤트 처리)
    sys.exit(app.exec_())

    # 파이썬 인터프리터
    # 큐티 - 바이너리파일 접근
    # 위 두개가 돌아가고있음.. 둘다 죽여야함
