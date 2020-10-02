import numpy as np
import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 120)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
s,orignal = cam.read()
height, width, channels = orignal.shape
print(width)
print(height)
while(1):
    s,orignal = cam.read()
    left=orignal[0:height,0:int(width/2)]
    right=orignal[0:height,int(width/2):(width)]
    cv2.imshow('left',left)
    cv2.imshow('Right',right)
 
    if cv2.waitKey(1) & 0xFF == ord('w'):

        break


cam.release()
cv2.destroyAllWindows()