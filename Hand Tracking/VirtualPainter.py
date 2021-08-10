import cv2, numpy as np, time, HandTrackingModule as htm
from os.path import join, dirname
from os import listdir

folderPath = join(dirname(__file__),"Header")
myList = listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(join(folderPath,imPath))
    overlayList.append(image)

header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector = htm.handDetector(detectionConfidence=0.85)

while True:
    # 1. Definir a imagem (fonte = webcam)
    success, img = cap.read()
    img = cv2.flip(img, 1) # para facilitar a interação

    # 2. Identificar os pontos das coordenadas de mãos (landmarks)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if (lmList):
        # print(lmList)

        x1, y1 = lmList[8][1:] # coordenadas do dedo polegar
        x2, y2 = lmList[12][1:] # coordenadas do dedo indicador


    # 3. Verificar quais dedos estão levantados

    # 4. Modo de seleção: se dois dedos estiverem levantados

    # 5. Modo de denho: se o dedo indicador estiver levantado


    # Configurar a imagem de cabeçalho (header)
    img[0:120, 0:640] = header

    cv2.imshow("Image", img)
    cv2.waitKey(1)