import pyzed.sl as sl
# Initialize and open the camera
zed = sl.Camera()
zed.open()

# Enable Object Detection and create a variable for storage
zed.enable_object_detection()
objects = sl.Objects()

while True :
    # Grab a frame, retrieve the detected objects and print their 3D location
    zed.grab()
    zed.retrieve_objects(objects)
    for object in objects.object_list:
        print(object.position)