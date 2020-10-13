#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage, Image
import cv2
import numpy as np

def talker():

    #Parametros de la camara
    fx= 681.70635986328
    fy= 681.70635986328
    cx= 678.88836669921
    cy= 352.25689697265
    k1= 0
    k2= 0
    p1= 0
    p2= 0
    camera_matrix = np.array([[float(fx),0,float(cx)],[0,float(fy),float(cy)],[0,0,1]])
    distortion_coefficients= np.array([float(k1),float(k2),float(p1),float(p2)])
    print(camera_matrix)

    #pub = rospy.Publisher('image', CompressedImage, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    #rate = rospy.Rate(10) # 10hz

    ##Captura de video
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 60)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    s,orignal = capture.read()
    height, width = orignal.shape[:2]
    width =int(width/2)
    frame = orignal[0:height,0:int(width)]
    ##Matriz Rectificada
    scaled_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, distortion_coefficients, (width,height), 1, (width,height))
    roi_x, roi_y, roi_w, roi_h = roi
    msg = CompressedImage()
    print(scaled_camera_matrix)
    leftCam = cv2.undistort(orignal, camera_matrix, distortion_coefficients, None, None)
    """
    while not rospy.is_shutdown():
        [status, img] = capture.read()
        if status == True :
            print("publicando..")
            frame = img[0:height,0:int(width)]
            distorted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            undistorted_frame = cv2.undistort(
            distorted_frame, camera_matrix, distortion_coefficients, None, scaled_camera_matrix)
            mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coefficients, None, scaled_camera_matrix, (width,height), 5)
            dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            #cropped_frame = undistorted_frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
            cropped_frame = cv2.UMat(dst,[roi_y , roi_y + roi_h], [roi_x , roi_x + roi_w])
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
            pub.publish(msg)
        rate.sleep()"""

if __name__ == '__main__':
    try:
        talker()

    except rospy.ROSInterruptException:
        pass
""" 
s,orignal = capture.read()
    height, width = orignal.shape[:2]
    width =int(width/2)
    scaled_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, distortion_coefficients, (width,height), 1, (width,height))
    roi_x, roi_y, roi_w, roi_h = roi
    msg = CompressedImage()
   
    while not rospy.is_shutdown():
        [status, img] = capture.read()
        if status == True :
            print("publicando..")
            frame = img[0:height,0:int(width)]
            distorted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            undistorted_frame = cv2.undistort(
            distorted_frame, camera_matrix, distortion_coefficients, None, scaled_camera_matrix)
            mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coefficients, None, scaled_camera_matrix, (width,height), 5)
            dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            #cropped_frame = undistorted_frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
            cropped_frame = cv2.UMat(dst,[roi_y , roi_y + roi_h], [roi_x , roi_x + roi_w])
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
            pub.publish(msg)
        rate.sleep() """
