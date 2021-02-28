""" from PyAccessPoint import pyaccesspoint
import time

access_point = pyaccesspoint.AccessPoint()
access_point.start()
time.sleep(10)
access_point.stop()
 """
""" import base64
import paramiko
from paramiko import SSHClient
import time

# Iniciamos un cliente SSH
ssh = paramiko.SSHClient()
# Agregamos el listado de host conocidos
ssh.load_system_host_keys()
# Si no encuentra el host, lo agrega automáticamente  
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
ssh.connect('10.42.0.227', username='jetsonnano', password='Jetson3744')  # Iniciamos la conexión.

stdin, stdout, stderr = ssh.exec_command('nohup python3 ZED.py &\necho $!')


for line in stdout:
    print("linea" +str(line))
    break
ssh.close() """

"""
from fabric import *
import time 
import os


c = Connection(
    host="10.42.0.227",
    user="jetsonnano",
    connect_kwargs={
        "password": "Jetson3744",
    },
)
c.open()
c.run('chmod +x prueba.py')
result = c.run('nohup python3 prueba.py &')
c.run('exit')
#print(result.stdout)
time.sleep(5)

c.close()"""

"""
import numpy as np
import cv2 
from imutils import paths

fx= 699.8400268554688
fy= 699.8400268554688
cx= 675.9600219726562
cy= 348.0130004882812
k1= -0.17087399959564
k2= 0.023340599611402
p1= 0
p2= 0
camera_matrix = np.array([[float(fx),0,float(cx)],[0,float(fy),float(cy)],[0,0,1]])
distortion_coefficients= np.array([float(k1),float(k2),float(p1),float(p2)])
width = 1280
height = 720
scaled_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, distortion_coefficients, (width,height), 1, (width,height))
roi_x, roi_y, roi_w, roi_h = roi


imagenes_entrada = []
imagen_entrada_index = 0
directorioImagenes = '/home/mateo/Documentos/Dataset1'
imagePaths = sorted(list(paths.list_images(directorioImagenes)))
directorioImagenes=directorioImagenes
i=0 
for imagePath in imagePaths:
    image_input = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
    i = i+1
    imagenes_entrada.append(image_input)
i=1
for frame in imagenes_entrada:
    print(i)
    #frame = img[0:height,0:int(width)]
    dst = cv2.undistort(frame, camera_matrix, distortion_coefficients, None, None)
    #mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coefficients, None, scaled_camera_matrix, (width,height), 5)
    #dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    #cropped_frame = undistorted_frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    #dst= dst.get()
    crop = dst[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    cropped_frame = cv2.UMat(crop)
    pts1 = np.float32([[0, 100], [1280, 0], [0, 620], [1280, 720]]) 
    pts2 = np.float32([[0, 0], [1280, 0], [0, 720], [1280, 720]]) 
      
    # Apply Perspective Transform Algorithm 
    matrix = cv2.getPerspectiveTransform(pts1, pts2) 
    for val in pts1:
        cv2.circle(frame,(val[0],val[1]),5,(0,255,0),-1)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(dst,M,(1280,720))
    gamma = 0.75
    lookUpTable = np.empty((1,256), np.uint8)
    for k in range(256):
        lookUpTable[0,k] = np.clip(pow(k / 255.0, gamma) * 255.0, 0, 255)
    res = cv2.LUT(dst, lookUpTable)
  
    cv2.imshow('mxasa',frame)
    cv2.imshow('ma',res)
    while(1):
        if cv2.waitKey(1) & 0xFF == ord('w'):

            break
    
    cv2.imwrite("/home/mateo/Documentos/DataSet1_rect/imagen"+str(i)+".jpg",dst)

    i=i+1
"""
"""
img = cv2.imread ( 'ScriptsROS/modo1.png' , cv2.IMREAD_COLOR)
# crear un objeto CLAHE (los argumentos son opcionales).
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
lab_planes = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=1.0,tileGridSize=(8,8))
lab_planes[0] = clahe.apply(lab_planes[0])
lab = cv2.merge(lab_planes)
bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


cv2.imshow( 'ScriptsROS/modo1_mod.png' , bgr)
while(1):
    if cv2.waitKey(1) & 0xFF == ord('w'):

        break
"""
import time
from MySQL_Connector import MySQL

conector = MySQL()
conector.conectar()
conector.get_mision(1)
time.sleep(2)
conector.desconectar()