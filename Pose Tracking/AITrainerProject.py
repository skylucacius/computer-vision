import cv2
import numpy as np
import time
from os.path import dirname, join
import PoseModule as pm

mediaDir = join(dirname(__file__),"Media")
imageName = join(mediaDir, "test.jpg")
# VideoName = join(mediaDir, "curl.mp4")
# cap = cv2.VideoCapture(VideoName)
detector = pm.PoseDetector()

while True:
    # success, img = cap.read()
    # img = cv2.resize(img, (1280,720))
    img = cv2.imread(imageName)
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img,draw=False)
    if lmList:
        # Braço direito
        detector.findAngle(img, 12, 14, 16)
        # Braço esquerdo
        # detector.findAngle(img, 11, 13, 15)


    cv2.imshow("Image", img)
    cv2.waitKey(1)