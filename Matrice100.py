#!/usr/bin/env python

# ROS python API
import rospy
import time
# Joy message structure
from std_msgs.msg import UInt8
from sensor_msgs.msg import BatteryState, NavSatFix, Imu
# 3D point & Stamped Pose msgs
from geometry_msgs.msg import PointStamped
# import all mavros messages and services
from dji_sdk.msg import *
from dji_sdk.srv import *

#Class ROS services
class Matrice100Services:
    def __init__(self):
        self.MissionTask = MissionWaypointTask()
        pass

    def getSDKControl(self):
        rospy.wait_for_service('dji_sdk/sdk_control_authority')
        try:
            GetControl = rospy.ServiceProxy('dji_sdk/sdk_control_authority', dji_sdk.srv.con)
            GetControl(1)
        except rospy.ServiceException as e:
            rospy.logerr("Service Control Authority call failed: %s"%e)

    def releaceSDKControl(self):
        rospy.wait_for_service('dji_sdk/sdk_control_authority')
        try:
            GetControl = rospy.ServiceProxy('dji_sdk/sdk_control_authority', dji_sdk.srv.con)
            GetControl(0)
        except rospy.ServiceException as e:
            rospy.logerr("Service Control Authority call failed: %s"%e)

    def setArm(self):
        rospy.wait_for_service('dji_sdk/drone_arm_control')
        try:
            armService = rospy.ServiceProxy('dji_sdk/drone_arm_control', dji_sdk.srv.DroneArmControl)
            armService(True)
        except rospy.ServiceException as e:
            rospy.logerr("Service arming call failed: %s"%e)

    def setDisarm(self):
        rospy.wait_for_service('dji_sdk/drone_arm_control')
        try:
            armService = rospy.ServiceProxy('dji_sdk/drone_arm_control', dji_sdk.srv.DroneArmControl)
            armService(False)
        except rospy.ServiceException as e:
            rospy.logerr("Service disarming call failed: %s"%e)

    def setLocalPosition(self):
        rospy.wait_for_service('dji_sdk/set_local_pos_ref')
        try:
            armService = rospy.ServiceProxy('dji_sdk/set_local_pos_ref', dji_sdk.srv.SetLocalPosRef)
            return True
        except rospy.ServiceException as e:
            rospy.logerr("Service arming call failed: %s"%e) 
            return False       

    def takeoff(self):
        rospy.wait_for_service('dji_sdk/drone_task_control')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/drone_task_control', dji_sdk.srv.DroneTaskControl)
            TaskService(4)
        except rospy.ServiceException as e:
            rospy.logerr("Service Takeoff call failed: %s"%e)

    def landing(self):
        rospy.wait_for_service('dji_sdk/drone_task_control')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/drone_task_control', dji_sdk.srv.DroneTaskControl)
            TaskService(6)
        except rospy.ServiceException as e:
            rospy.logerr("Service Landing call failed: %s"%e)

    def goHome(self):
        rospy.wait_for_service('dji_sdk/drone_task_control')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/drone_task_control', dji_sdk.srv.DroneTaskControl)
            TaskService(1)
        except rospy.ServiceException as e:
            rospy.logerr("Service Go Home call failed: %s"%e)

    def startMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_action')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_action', dji_sdk.srv.MissionWpAction)
            TaskService(0)
        except rospy.ServiceException as e:
            rospy.logerr("Service Start WP Mission call failed: %s"%e)

    def stopMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_action')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_action', dji_sdk.srv.MissionWpAction)
            TaskService(1)
        except rospy.ServiceException as e:
            rospy.logerr("Service Stop WP Mission call failed: %s"%e)

    def pauseMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_action')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_action', dji_sdk.srv.MissionWpAction)
            TaskService(2)
        except rospy.ServiceException as e:
            rospy.logerr("Service Pause WP Mission call failed: %s"%e)

    def resumeMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_action')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_action', dji_sdk.srv.MissionWpAction)
            TaskService(0)
        except rospy.ServiceException as e:
            rospy.logerr("Service Resume WP Mission call failed: %s"%e)

    def uploadMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_upload')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_upload', dji_sdk.srv.MissionWpUpload)
            TaskService(self.MissionTask)
        except rospy.ServiceException as e:
            rospy.logerr("Service Upload WP Mission call failed: %s"%e)

    def getInfoMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_getInfo')
        try:
            MissionInfoMessage = rospy.ServiceProxy('dji_sdk/mission_waypoint_getInfo', dji_sdk.srv.MissionWpGetInfo)
            return MissionInfoMessage
        except rospy.ServiceException as e:
            rospy.logerr("Service Get Mission WP Info Mission call failed: %s"%e)
            return None

    def getSpeedMission(self):
        rospy.wait_for_service('dji_sdk/mission_waypoint_getSpeed')
        try:
            speed = rospy.ServiceProxy('dji_sdk/mission_waypoint_getSpeed', dji_sdk.srv.MissionWpGetSpeed)  
            return speed
        except rospy.ServiceException as e:
            rospy.logerr("Service Get Speed WP Mission call failed: %s"%e)
            return None

    def setSpeedMission(self, speed):
        rospy.wait_for_service('dji_sdk/mission_waypoint_setSpeed')
        try:
            TaskService = rospy.ServiceProxy('dji_sdk/mission_waypoint_setSpeed', dji_sdk.srv.MissionWpSetSpeed)  
            TaskService(speed)
        except rospy.ServiceException as e:
            rospy.logerr("Service Set Speed WP Mission call failed: %s"%e)

#Class ROS Topics
class Matrice100Topics:
    def __init__(self):
        self.battery = None
        self.gps = None
        self.position_status = None
        self.position = None
        self.position_covariance = None
        self.imu_orientation = None
        self.imu_velocity = None
        self.imu_acceleration = None
        self.local = None
        pass

    def batteryState(self):
        try:
            sub = rospy.Subscriber('dji_sdk/battery_state', BatteryState, self.batteryCB)  
        except rospy.ServiceException as e:
            print("Failed to subscribe battery state: %s"%e)

    def batteryCB(self, data):
        self.battery = 100*(data.percentage)

    def gpsHealth(self):
        try:
            sub = rospy.Subscriber('dji_sdk/gps_health', UInt8, self.gpsCB)  
        except rospy.ServiceException as e:
            print("Failed to subscribe GPS health: %s"%e)

    def gpsCB(self, data):
        self.gps = data

    def gpsPosition(self):
        try:
            sub = rospy.Subscriber('dji_sdk/gps_position', NavSatFix, self.gpsPositionCB)  
        except rospy.ServiceException as e:
            print("Failed to subscribe GPS position: %s"%e)

    def gpsPositionCB(self, data):
        self.position_status = data.status
        self.position = (data.latitud, data.longitude, data.altitude)
        self.position_covariance = data.postion_covariance

    def imu(self):
        try:
            sub = rospy.Subscriber('dji_sdk/imu', Imu, self.imuCB)  
        except rospy.ServiceException as e:
            print("Failed to subscribe GPS position: %s"%e)

    def imuCB(self, data):
        self.imu_orientation = data.orientation_covariance
        self.imu_velocity = data.angular_velocity_covariance
        self.imu_acceleration = data.linear_acceleration_covariance

    def localPosition(self):
        try:
            sub = rospy.Subscriber('dji_sdk/local_position', PointStamped, self.localPositionCB)  
        except rospy.ServiceException as e:
            print("Failed to subscribe GPS position: %s"%e)

    def localPositionCB(self, data):
        self.local = data.Point

# Main function
def main():

    # initiate node
    ros_node = rospy.init_node('setpoints_node', anonymous=True)

    # flight mode object
    
    service = Matrice100Services()
    topic = Matrice100Topics()
    # ROS loop rate, [Hz]
    rate = rospy.Rate(20.0)



    # ROS main loop
    while not rospy.is_shutdown():
        rospy.loginfo("arm")

        rospy.loginfo("takeoff")
        service.takeoff()
        time.sleep(5)
        rospy.loginfo("landing")
        service.landing()

        service.setDisarm()

        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass