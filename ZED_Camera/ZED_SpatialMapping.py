import pyzed.sl as sl
# Initialize and open the camera
zed = sl.Camera()
zed.open()

# Enable Spatial Mapping
zed.enable_spatial_mapping()
i = 0

# Map the scene for 1000 frames
while i < 1000:
    i=i+1
    zed.grab()

# Extract and save the map as a mesh
mesh = sl.Mesh()
zed.extract_whole_spatial_map(mesh)
mesh.save("mesh.obj")