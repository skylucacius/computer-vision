import time
import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################### Parâmetros ##########################
# o driver da camera que testei possui essa resolução máxima, 
# portanto usarei esse valor. Equivalente a 16*40 x 12*40 pixels
wCam, hCam = 640, 480 

#########################################################

cap = cv2.VideoCapture(0)
print(cap.set(3, wCam))
print(cap.set(4, hCam))
# print(cap.get(3))
# print(cap.get(4))
pTime = 0
detector = htm.handDetector(detectionConfidence=0.7)

devices = AudioUtilities.GetSpeakers() # configurações do pycaw
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1],lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range 35 - 260
        # Vol range 

        if length < 50:
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED)

        # Usaremos a lib pycaw para alterar o volume baseado em length (distância entre a ponta dos dedos)






    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)