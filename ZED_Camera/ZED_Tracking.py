import pyzed.sl as sl
# Initialize and open the camera
zed = sl.Camera()
zed.open()

# Enable Positional Tracking and create a pose variable
zed.enable_positional_tracking()
zed_pose = sl.Pose()

while True :
    # Grab a frame and get the current camera position
    zed.grab()
    zed.get_position(zed_pose, sl.REFERENCE_FRAME.WORLD)