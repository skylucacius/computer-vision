import cv2
import time
from os import listdir
from os.path import dirname, join
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
wCam, hCam = 640,480
cap.set(3, wCam)
cap.set(4, hCam)

imagePath = join(dirname(__file__), "FingerImages")
myList = listdir(imagePath)
overlayList = []
for imageName in myList:
    image = cv2.imread(join(imagePath, imageName))
    overlayList.append(image)
    # print(imageName)

pTime = 0
detector = htm.handDetector(detectionConfidence=0.75)
tipIds = [4,8,12,16,20]
# print(overlayList)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        fingers = []

        # thumb
        if lmList[3][1] < lmList[4][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # print(lmList)

        # four fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # print(fingers)
        totalFingers = fingers.count(1)
        # print(totalFingers)
        h, w, c = overlayList[0].shape # height, width
        img[0:h, 0:w] = overlayList[totalFingers]

        cv2.rectangle(img, (20,255), (170,425), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime




    cv2.putText(img,f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3) # width, height

    cv2.imshow("Image",img)
    cv2.waitKey(1)