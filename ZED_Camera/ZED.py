import numpy as np
import cv2
import time

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
s,orignal = cam.read()
height, width, channels = orignal.shape
print(width)
print(height)
cam_output_l = cv2.VideoWriter('/home/jetsonnano/Desktop/Jetson/TG_DroneFacade/ZED_Camera/Captura/video_l.avi', cv2.VideoWriter_fourcc('M','J','P','G'),20.0,(int(width/2),height))
cam_output_r = cv2.VideoWriter('/home/jetsonnano/Desktop/Jetson/TG_DroneFacade/ZED_Camera/Captura/video_r.avi', cv2.VideoWriter_fourcc('M','J','P','G'),20.0,(int(width/2),height))

path = '/home/jetsonnano/Desktop/Jetson/TG_DroneFacade/ZED_Camera/Captura/'
i = 1
while(1):
    s,orignal = cam.read()
    right=orignal[0:height,0:int(width/2)]
    left=orignal[0:height,int(width/2):(width)]
    left = cv2.rotate(left, cv2.ROTATE_180)
    right = cv2.rotate(right, cv2.ROTATE_180)
    cv2.imshow('left',left)
    cv2.imshow('Right',right)
    filename = "imagen_"+str(i)
    cam_output_l.write(left)
    cam_output_r.write(left)
    if cv2.waitKey(1) & 0xFF == ord('w'):

        break


cam.release()
cam_output_l.release()
cam_output_r.release()
cv2.destroyAllWindows()