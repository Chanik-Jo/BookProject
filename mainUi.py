import threading
from datetime import time
from stringTest import turnStringToIsbn
import PIL
import cv2
import imutils
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys,crawling,cliSocket

from imutils.video import VideoStream
from pyzbar import pyzbar



result=""
found = set()


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

        self.manualSearchBtn.clicked.connect(lambda:
                                             self.isbnSearch(self.IsbnManualInput.toPlainText()))#이거 람다식으로 isbn 들어가게 고치기.

        self.BookTitleLabel.setWordWrap(True)
        self.userLIstRefresh.clicked.connect(self.loadUsers)
        self.BookPublisherLabel.setWordWrap(True)
        self.BookAuthorLabel.setWordWrap(True)

        self.userListTable.setHorizontalHeaderLabels(['number', 'name', 'price'])
        #threading.Thread(target=self.camViewThread).start()#캠 스레드 발동.
        self.videoToTextBtn.clicked.connect(self.cameraRecgonize)
        self.IsbnManualInput.setPlainText("978-89-8458-217-0")

    def camViewThread(self):
        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        #time.sleep(2.0)
        global result
        while True:
            try:
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                barcodes = pyzbar.decode(frame)  # 캠에 찍힌 바코드가 여러개일 경우 하나씩 불러온다
                #print(barcodes)

                for barcode in barcodes:
                    print(barcode)
                    (x, y, w, h) = barcode.rect
                    # frame에 (x,y)에서 (x+w,y+h) 까지 빨간(blue=0,green=0,red=255), 두께 2의 직사각형그린다
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")  # 바코드 데이터를 읽어 온다.
                    text = str(barcodeData) # 아하 이놈이 데이터로구나.
                    if(text != ""):#빈칸이 아닐때만.
                        result =text#갱신.
                    #cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    # 텍스트를 frame에 넣는다.
                    # 만약 아직까지 찾지 않은 바코드면 프린트한다.
                    if barcodeData not in found:
                        #print(barcodeData)
                        found.add(barcodeData)
                # 프로세스가 끝나면 frame을 보여준다. 바코드가 있으면 바코드 번호와 직사각형이 보인다.
                #cv2.imshow("Barcode Scanner", frame)
                # q를 누르면 바코드 스캔을 끝난다.

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            # 정상적으로 종료한다.


                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                Image = PIL.Image.fromarray(img, 'RGB')
                Image = ImageQt(Image).copy()
                videoWidth = self.camLabel.width()  # 이게 내가알기로는 ui(WindowClass)상에서의 widget 관련 값임.
                videoHeight = self.camLabel.height()
                Image = Image.scaled(videoWidth, videoHeight)  # 출력할 이미지를 위젯크기에 끼워맞추기.

                self.camLabel.setPixmap(QPixmap.fromImage(Image))
            except:
                pass
        cv2.destroyAllWindows()
        vs.stop()


    def cameraRecgonize(self):
        result =""

        if(result==""):
            self.IsbnManualInput.setPlainText("제대로 인식시켜 주세요")
        else:

            result = turnStringToIsbn(result)
            self.IsbnManualInput.setText(result)




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
            print("title publisher author successful")

            #cliSocket.retrieveDBDatafromServer(self,m="insert into custom_table (name,age) values({},{})".format(title,author))
            #만약  english라면
            cliSocket.retrieveDBDatafromServer(self,m="insert into custom_table (name,age) values({},{})".format(title,author))



        except Exception as e:
            print("예외 발생함.",e)









if __name__=="__main__":

    print("helloworld")
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()