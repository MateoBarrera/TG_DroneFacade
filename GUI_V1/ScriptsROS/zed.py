import numpy as np
import cv2

cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FPS, 60)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
s,orignal = cam.read()
height, width, channels = orignal.shape
print(width)
print(height)
while(1):
    s,orignal = cam.read()
    #left=orignal[0:height,0:int(width/2)]
    #right=orignal[0:height,int(width/2):(width)]
    cv2.imshow('left',orignal)
    #cv2.imshow('Right',right)
 
    if cv2.waitKey(1) & 0xFF == ord('w'):

        break


cam.release()
cv2.destroyAllWindows() 
"""
import cv2
import numpy as np
from flir

Boson = flirpy.camera.boson

with Boson() as camera:
    while True:
        img = camera.grab().astype(np.float32)

        # Rescale to 8 bit
        img = 255*(img - img.min())/(img.max()-img.min())

        cv2.imshow('Boson', img.astype(np.uint8))
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        
cv2.destroyAllWindows()"""