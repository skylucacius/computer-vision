import cv2
import numpy as np
import time
from os.path import dirname, join
import PoseModule as pm

mediaDir = join(dirname(__file__),"Media")
# imageName = join(mediaDir, "test.jpg")
VideoName = join(mediaDir, "curls.mp4")
cap = cv2.VideoCapture(VideoName)
detector = pm.PoseDetector()
count = 0; dir = 0; pTime = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280,720))
    # img = cv2.imread(imageName)
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img,draw=False)
    if lmList:
        # Braço direito
        # detector.findAngle(img, 12, 14, 16)
        # Braço esquerdo
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (30,150), (0,100))
        bar = np.interp(angle, (30, 150), (650,100))
        # print(angle, per)
        
        # contar curls (ciclos) foram realizados
        color = (255,0,255)
        if per == 100:
            color = (0,255,0)
            if dir == 0:
                count += 0.50
                dir = 1
        if per == 0:
            color = (0,255,0)
            if dir == 1:
                count += 0.50
                dir = 0
        # print(count)

        # mostrar barra
        cv2.rectangle(img, (1100,100), (1175,650), color, 3)
        cv2.rectangle(img, (1100,int(bar)), (1175,650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100,75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'{str(int(fps))}', (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)

    # contagem de curls
    cv2.rectangle(img, (0,450), (250,720), (0,255,0), cv2.FILLED)
    cv2.putText(img, f'{str(int(count))}', (45,670), cv2.FONT_HERSHEY_PLAIN, 15, (255,0,0), 25)

    cv2.imshow("Image", img)
    cv2.waitKey(1)