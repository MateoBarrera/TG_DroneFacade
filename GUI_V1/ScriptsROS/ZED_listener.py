#!/usr/bin/env python

import roslib
import rospy
import sys
import cv2
import cv2.cv2 as cv
import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import CameraInfo
import math 
import time

class ZED_ROS():
    def __init__(self):
        super().__init__()
        rospy.init_node('Zed_info_Subscriber', anonymous=True)
        self.camera_info()
        self.listener()

    def camera_info(self):
        info = rospy.wait_for_message('zed/zed_node/left/camera_info', CameraInfo)
        print(info)
        
    def pose_callback(self,data):
        posicion = (data.pose.position.x,data.pose.position.y,data.pose.position.z)
        orientacion = (data.pose.orientation.x,data.pose.orientation.y,data.pose.orientation.z, data.pose.orientation.w)
        print(posicion)
        print(orientacion)
        #rospy.loginfo("receiving pose"+str(data.position.y))
        #rospy.loginfo("receiving pose"+str(data.position.x))

    def listener(self):
        pose = rospy.wait_for_message('zed/zed_node/pose', PoseStamped)
        print(pose)
        self.pose_callback(pose)
        #camera_info.rate(1)
        #camera_info = rospy.wait_for_message('zed/zed_node/left/camera_info', CameraInfo)
        #print(camera_info)
        # spin() simply keeps python from exiting until this node is stopped
        #rospy.spin()

if __name__ == "__main__":
    import  sys
    ZED_ROS()
     