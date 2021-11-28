from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys,crawling,cliSocket




form_class = uic.loadUiType('untitled.ui')[0]
#Qrc로 이미지 불러올생각 하지말고 에지간하면 qt내부에서 수행하라 . 문제생긴다. no Module 문제로 3시간을 내리 날렸다.

#pyrcc5 resource.qrc -o uiResources_rc.py
class WindowClass(QMainWindow,form_class):

    '''

    IsbnManualInput : QPlainTextEdit
    videoToTextBtn : QButton
    manualSearchBtn : QButton
    camLabel : QLabel

    bookPhotoLabel : QLabel
    BookTitleLabel : QLabel
    BookIsbnLabel : QLabel
    BookPublisherLabel : QLabel
    BookAuthorLabel : QLabel

    nextPageBtn : QButton
    previousPageBtn : QButton

    userListTable : QTableWidget
    userListTitle : QLabel
    stackedWidget : QStackedWidget

    '''


    #일요일날 할일 바코드 시스템 추가.
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("last Project")
        self.stackedWidget.setCurrentIndex(0)#열린페이지 기본값 0
        self.nextPageBtn.clicked.connect(self.gotoPage2)
        self.previousPageBtn.clicked.connect(self.gotoPage1)
        self.userListTable.clicked.connect(self.loadUsers)
        self.bookClipart = QPixmap("bookIcon.png")
        self.bookPhotoLabel.setPixmap(self.bookClipart)
        self.camClipart = QPixmap("scanClipart.jpg")
        self.camLabel.setPixmap(self.camClipart)
        #lambda: self.button3_func(time.strftime("[%H:%M:%S]\n")
        self.manualSearchBtn.clicked.connect(lambda:
                                             self.isbnSearch(self.IsbnManualInput.toPlainText()))#이거 람다식으로 isbn 들어가게 고치기.

        self.BookTitleLabel.setWordWrap(True)
        self.userLIstRefresh.clicked.connect(self.loadUsers)
        self.BookPublisherLabel.setWordWrap(True)
        self.BookAuthorLabel.setWordWrap(True)

        self.userListTable.setHorizontalHeaderLabels(['number', 'name', 'price'])



    def loadUsers(self):
        #self.userListTable.setRowCount(0)#표에있는 모든 내용을 깔끔히 삭제하라.

        cliSocket.retrieveDBDatafromServer(self)#이제 이 클래스에서 전담해서 select 연산을 실행한다.



    def gotoPage2(self):
        self.stackedWidget.setCurrentIndex(1)
    def gotoPage1(self):
        self.stackedWidget.setCurrentIndex(0)

    def isbnSearch(self,searchLetter):
        #"979-11-5839-179-9"

        if(self.IsbnManualInput.toPlainText()==""):
            print("input something inside here")
            return
        try:
            print("isbn Search function")
            self.notificationLabel.setText("잠시 기다려 주세요")
            print(searchLetter)
            title,publisher,author ,image=crawling.isbnOutput(searchLetter)
            #bookImg = QPixmap(image)
            #self.bookPhotoLabel.setPixmap(bookImg) 원래는 이미지를 가져오려 했으나,
            #팝업에서 이미지를 불러오는것에 실패해서 일단은 생략하였다.
            self.BookTitleLabel.setText(title)
            self.BookIsbnLabel.setText(searchLetter)
            self.BookPublisherLabel.setText(publisher)
            self.BookAuthorLabel.setText(author)
            self.notificationLabel.setText("바코드를 인식시켜 주세요.")
            cliSocket.retrieveDBDatafromServer(self,"INSERT INTO 테이블 이름 (name,age)VALUE ({},{})".format(title,author))
        except Exception as e:
            print("예외 발생함.",e)









if __name__=="__main__":

    print("helloworld")
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()