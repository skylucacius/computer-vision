import cv2
import mediapipe as mp
import time
from os.path import realpath, join, dirname

class FaceMeshDetector():
    def __init__(self, staticMode = False, maxFaces = 2, minDetectionCon = 0.5, minTrackingConf = 0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackingConf = minTrackingConf

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=2)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    def findFaceMesh(self, img, draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)
        faces = []
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                            img, 
                            faceLms, 
                            self.mpFaceMesh.FACE_CONNECTIONS, 
                            self.drawSpec, 
                            self.drawSpec)
                face = []

                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x,y = int(lm.x * iw), int(lm.y * ih)
                    # cv2.putText(img, f'{str(id)}', (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
                    face.append([x,y])
                faces.append(face)
        return img, faces

def main():

    filename = join(realpath(dirname(__file__)),"..","Face Detection","Videos/1.mp4")
    cap = cv2.VideoCapture(filename)
    pTime = 0
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img,True)
        # if faces:
        #     print(len(faces))
                

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()