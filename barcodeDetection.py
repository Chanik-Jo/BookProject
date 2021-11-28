import cv2
import pyzbar.pyzbar as pyzbar
from playsound import playsound

used_codes = []
data_list = []

try:
    f = open("qrbarcode_data.txt", "r", encoding="utf8")
    data_list = f.readlines()
except FileNotFoundError:
    pass
else:
    f.close()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

for i in data_list:
    used_codes.append(i.rstrip('\n'))

while True:
    success, frame = cap.read()