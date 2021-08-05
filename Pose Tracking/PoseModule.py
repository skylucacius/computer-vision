from time import time
import mediapipe as mp
import cv2
from os.path import dirname, join
from math import atan2, degrees

class PoseDetector():
    def __init__(self, mode = False, complexity = 1, smooth = True, detectionConf = 0.5, trackCon = 0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detectionConf = detectionConf
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detectionConf, self.trackCon)

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True): # calcula o ângulo de (P1,P2,P3) com P2
        # Pegar as coordenadas dos pontos
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calcular o ângulo entre 3 pontos num sistema de coordenadas bidimensional. 
        # Aqui foi usado raciocínio semelhante ao presente em
        # https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
        
        # Ou seja, dados 3 pontos (P1, P2, P3) é realizada uma translação a P2 e calcula-se a diferença 
        # entre os ângulos de P3 e P1 relação ao eixo x, que agora tem origem em P2. 

        # Obs: O ponto em que a translação for realizada será aquele que o ângulo será computado.Nesse caso, P2.
        # Finalmente, é realizada uma conversão de radianos para graus de modo a exibir seu valor na tela.
        angle = degrees(atan2(y3 - y2, x3 - x2) - atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle += 360
        # print(angle)

        # Desenhá-los, se solicitado
        if draw:
            cv2.line(img, (x1,y1), (x2,y2), (255,255,255,3))
            cv2.line(img, (x2,y2), (x3,y3), (255,255,255,3))
            cv2.circle(img, (x1,y1), 10, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x1,y1), 15, (0,0,255), 2)
            cv2.circle(img, (x2,y2), 10 , (0,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15 , (0,0,255), 2)
            cv2.circle(img, (x3,y3), 10 , (0,0,255), cv2.FILLED)
            cv2.circle(img, (x3,y3), 15 , (0,0,255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)


def main():
    filename = join(dirname(__file__),'Media','1.mp4')
    cap = cv2.VideoCapture(filename)
    pTime = time()
    detector = PoseDetector()


    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw = False)
        # if lmList:
        #     print(lmList[0])
        #     cv2.circle(img, (lmList[0][1], lmList[0][2]), 15, (255,0,0), cv2.FILLED)

        cTime = time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()