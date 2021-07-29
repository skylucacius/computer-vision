from time import time
import mediapipe as mp
import cv2
from os.path import dirname, join

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
        lmList = []
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
        return lmList


def main():
    filename = join(dirname(__file__),'PoseVideos','1.mp4')
    cap = cv2.VideoCapture(filename)
    pTime = time()
    detector = PoseDetector()


    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw = False)
        if lmList:
            print(lmList[0])
            cv2.circle(img, (lmList[0][1], lmList[0][2]), 15, (255,0,0), cv2.FILLED)

        cTime = time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()