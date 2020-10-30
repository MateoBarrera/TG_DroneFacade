from PyAccessPoint import pyaccesspoint
import time

access_point = pyaccesspoint.AccessPoint()
access_point.start()
time.sleep(10)
access_point.stop()
