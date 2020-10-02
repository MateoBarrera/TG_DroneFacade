import pyzed.sl as sl
# Initialize and open the camera
zed = sl.Camera()
zed.open()

# Create matrices to store the depth and point cloud
depth = sl.Mat()
point_cloud = sl.Mat()

while True :
    # Grab a frame and retrieve depth and point cloud
    zed.grab()
    zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
    zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)