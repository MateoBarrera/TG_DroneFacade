#!/usr/bin/env python3

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
import pandas as pd

#Class ROS services
class Matrice100Services:
    def __init__(self):
        self.MissionTask = []
        pass

    def getSDKControl(self):
        rospy.wait_for_service('dji_sdk/sdk_control_authority')
        try:
            Control = rospy.ServiceProxy('dji_sdk/sdk_control_authority', dji_sdk.srv.SDKControlAuthority)
            Control(1)
            return True
        except rospy.ServiceException as e:
            rospy.logerr("Service Control Authority call failed: %s"%e)
            return False

    def releaseSDKControl(self):
        rospy.wait_for_service('dji_sdk/sdk_control_authority')
        try:
            Control = rospy.ServiceProxy('dji_sdk/sdk_control_authority', dji_sdk.srv.SDKControlAuthority)
            Control(0)
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
        try:
            rospy.wait_for_service('dji_sdk/set_local_pos_ref')
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

    def set_local_pos(self):
        rospy.wait_for_service('/dji_sdk/set_local_pos_ref')
        try:
            LocalPos = rospy.ServiceProxy('/dji_sdk/set_local_pos_ref', dji_sdk.srv.SetLocalPosRef)
        except rospy.ServiceException as e:
            rospy.logerr("Service set Local Pos call failed: %s"%e)

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
    
    def waypoint_mission(self, coord):
        #Configuración de la Misión
        MissionTask = MissionWaypointTask()
        MissionTask.velocity_range = 10
        MissionTask.idle_velocity = 5
        #Acción después del final: 0 Sin acción 1 Regreso al origen 2 Aterrizaje automático 3 Regreso a un punto determinado 4 Modo sin fin, no salir
        MissionTask.action_on_finish = 1 
        #Veces que se ejecuta 
        MissionTask.mission_exec_times = 1 
        # Dirección: 0 modo automático (apuntando al siguiente waypoint) 1 bloquear el valor inicial 2 controlar con el mando a distancia 3 adoptar el ángulo de guiñada del waypoint
        MissionTask.yaw_mode = 1  
        MissionTask.trace_mode = 0 
        # Desconeción del remoto 
        MissionTask.action_on_rc_lost = 1 
        MissionTask.gimbal_pitch_mode = 0
        wps = []
        for coordinate in coord.itertuples():
            wp = self.set_waypoints(coordinate[1],coordinate[2],coordinate[3])
            wps.append(wp)
            
        print("done")
        MissionTask.mission_waypoint = wps
        self.MissionTask = MissionTask

    def set_waypoints(self, latitude, longitude, altitude):
        hovertime = 5
        wp = MissionWaypoint()
        wp.latitude = latitude
        wp.longitude = longitude
        wp.altitude = altitude
        wp.damping_distance = 0 
        wp.target_yaw = 0  
        wp.target_gimbal_pitch = 0
        wp.turn_mode = 0  
        wp.has_action = 1
        wp.action_time_limit = 5000
        wp.waypoint_action.action_repeat = 1
        '''
        wp.waypoint_action.command_list = "\0"*16
        wp.waypoint_action.command_parameter[0] = hovertime * 1000 '''

        return wp

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
        self.flight_status = None
        self.flightStatus()
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
            sub = rospy.wait_for_message('dji_sdk/local_position', PointStamped)
            return sub  
        except rospy.ServiceException as e:
            print("Failed to subscribe GPS position: %s"%e)
            return None

    def flightStatus(self):
        try:
            sub = rospy.Subscriber('/dji_sdk/flight_status', UInt8, self.flightCB)
        except rospy.SubscriberExeption as e:
            print("Failed to subscribe GPS position: %s"%e)

    def flightCB(self, data):
        self.flight_status = data

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
 
    status = service.setLocalPosition()
    if status:
        position = rospy.wait_for_message('dji_sdk/gps_position', NavSatFix)
    print(position.latitude,position.longitude,position.altitude)
    
    coordenadas = pd.DataFrame(columns=['latitude','longitude','altitude'],)
    coordenadas = coordenadas.append({'latitude': position.latitude, 'longitude': position.longitude, 'altitude': position.altitude+24 },ignore_index=True)
    coordenadas = coordenadas.append({'latitude': position.latitude+0.0002, 'longitude': position.longitude, 'altitude': position.altitude+24 },ignore_index=True)
    coordenadas = coordenadas.append({'latitude': position.latitude+0.0002, 'longitude': position.longitude, 'altitude': position.altitude+18},ignore_index=True)
    coordenadas = coordenadas.append({'latitude': position.latitude, 'longitude': position.longitude, 'altitude': position.altitude+18 },ignore_index=True)
    coordenadas = coordenadas.append({'latitude': position.latitude, 'longitude': position.longitude, 'altitude': position.altitude+12},ignore_index=True)
    coordenadas = coordenadas.append({'latitude': position.latitude+0.0002, 'longitude': position.longitude, 'altitude': position.altitude+12 },ignore_index=True) 
    
    print(coordenadas)
    
    # ROS main loop
    rospy.loginfo("Generando misión")
    service.waypoint_mission(coordenadas)
    service.uploadMission()
    rospy.loginfo("Carga Correcta!")

    rospy.loginfo("get Control")
    status = service.getSDKControl()
    if status:
        while True: 
            print(topic.flight_status)
            if topic.flight_status == 3:
                
                break 
        rospy.loginfo("start Mission")
        try:
            service.startMission()
        except keyboardInterrupt as e:
            pass
        else:
            rospy.loginfo("landing")
            service.landing()
            while True: 
                if topic.flight_status == 5:
                    break 
            rospy.loginfo("realse Control")
            service.releaseSDKControl()
    


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass