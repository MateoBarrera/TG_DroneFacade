#!/usr/bin/env python3
import sys
import rospy
import roslib
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import cv2 
import cv2.cv2 as cv
import numpy as np

class image_subscriber:
    def __init__(self):
        #self.listener()
        rospy.loginfo(" Press CTRL+c to stop SJTU_DRONE")
        self.image_sub = rospy.Subscriber('/zed/zed_node/left/image_rect_color/compressed', CompressedImage, self.image_callback)
        rospy.spin()
     
    
    def image_callback(self,data):
        #print(data.header)
        np_arr = np.fromstring(data.data , np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #Visualizacion en OpenCV
        cv2.imshow("Image",image_np)
        cv2.waitKey(1) 
    



if __name__ == '__main__':
    try:
        node = rospy.init_node('Camera_info_topic', anonymous=True)
        suscripcion = image_subscriber()
    except rospy.ROSInterruptException as e:
        print(e)
        

