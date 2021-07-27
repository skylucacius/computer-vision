import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
success, img = cap.read()
print(success)
print(cap.isOpened())

# while True:
#     sucess, img = cap.read()

#     print(sucess)

    # cv2.imshow("Image", img)
    # cv2. waitKey(1)


cap.release()
cv2.destroyAllWindows()
