#!/usr/bin/env python

import roslib; #roslib.load_manifest('sjtu_drone')
import rospy
import sys
import cv2
import cv2.cv2 as cv
import numpy as np
from geometry_msgs.msg import Pose
from sensor_msgs.msg import CameraInfo,CompressedImage, Image
import math 
from cv_bridge import CvBridge, CvBridgeError
def callback(data):

    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Camera_info_topic', anonymous=True)
    #camera_info = rospy.Subscriber('zed/zed_node/left/camera_info', CameraInfo, callback)
    camera_image = rospy.Subscriber('/drone/front_camera/image_raw', Image, callback)
    #camera_image = rospy.Subscriber('/zed/zed_node/left/image_rect_color', Image, callback)
    #camera_info.rate(1)
    #camera_info = rospy.wait_for_message('zed/zed_node/left/camera_info', CameraInfo)
    #print(camera_info)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def cleanup(self):
    print ("Shutting down vision node.")
    cv.destroyAllWindows()

if __name__ == '__main__':
    bridge = CvBridge()
    listener()
