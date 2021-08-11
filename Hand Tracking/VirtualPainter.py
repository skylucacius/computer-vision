import cv2, numpy as np, time, HandTrackingModule as htm
from os.path import join, dirname
from os import listdir
# from cv2.cv2 import bitwise_and, bitwise_or, cvtcolor

################################################################

brushThickness = 15
eraserThickness = 100

################################################################


folderPath = join(dirname(__file__),"Header")
myList = listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv2.imread(join(folderPath,imPath))
    overlayList.append(image)

header = overlayList[0]
drawColor = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = htm.handDetector(detectionConfidence=0.65)
xp, yp = 0,0
imgCanvas = np.zeros((480, 640, 3), np.uint8)

while True:
    # 1. Definir a imagem (fonte = webcam)
    success, img = cap.read()
    img = cv2.flip(img, 1) # para facilitar a interação

    # 2. Identificar os pontos das coordenadas de mãos (landmarks)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if (lmList):
        # print(lmList)
        xp, yp = 0,0

        x1, y1 = lmList[8][1:] # coordenadas do dedo polegar
        x2, y2 = lmList[12][1:] # coordenadas do dedo indicador


        # 3. Verificar quais dedos estão levantados
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. Modo de seleção: se dois dedos estiverem levantados
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)
            # print("Modo de seleção")
            # Verificar o click
            if y1 < 120:
                if 140 < x1 < 233:
                    header = overlayList[0]
                    drawColor = (255,0,255)
                elif 255 < x1 < 340:
                    header = overlayList[1]
                    drawColor = (255,0,0)
                elif 380 < x1 < 464:
                    header = overlayList[2]
                    drawColor = (0,255,0)
                elif 509 < x1 < 603:
                    header = overlayList[3]
                    drawColor = (0,0,0)

        # 5. Modo de denho: se o dedo indicador estiver levantado
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Modo de desenho")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1,y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1,y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1,y1), drawColor, brushThickness)
                
            xp, yp = x1, y1
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR) # possui fundo branco e traços pretos
    img = cv2.bitwise_and(img,imgInv) # o AND faz prevalecer os bits não brancos. Portanto, manterá o fundo e criará traços pretos
    img = cv2.bitwise_or(img,imgCanvas) # o OR 



    # Configurar a imagem de cabeçalho (header)
    img[0:120, 0:640] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inverse", imgInv)
    cv2.waitKey(1)