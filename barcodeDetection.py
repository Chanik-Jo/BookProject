# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2


vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

found = set()
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    barcodes = pyzbar.decode(frame) # 캠에 찍힌 바코드가 여러개일 경우 하나씩 불러온다
    print(barcodes)

    for barcode in barcodes:
        print(barcode)
        (x, y, w, h) = barcode.rect
        # frame에 (x,y)에서 (x+w,y+h) 까지 빨간(blue=0,green=0,red=255), 두께 2의 직사각형그린다
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")  # 바코드 데이터를 읽어 온다.
        text = str(barcodeData) #아하 이놈이 데이터로구나.
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) #텍스트를 frame에 넣는다.
        # 만약 아직까지 찾지 않은 바코드면 프린트한다.
        if barcodeData not in found:
            print(barcodeData)
            found.add(barcodeData)
    # 프로세스가 끝나면 frame을 보여준다. 바코드가 있으면 바코드 번호와 직사각형이 보인다.
    cv2.imshow("Barcode Scanner", frame)
    # q를 누르면 바코드 스캔을 끝난다.

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# 정상적으로 종료한다.
cv2.destroyAllWindows()
vs.stop()