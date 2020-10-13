from MySQL_Connector import MySQL
from ClassDatos import Datos
from datetime import date
import time
import logging
import cv2
from imutils import paths
import numpy as np

conexion = MySQL()
dato_obj = Datos()
dato_obj.fecha = date.today()
status, err = conexion.conectar()
image_input = cv2.imread("imagen_1.png", cv2.IMREAD_COLOR)
image = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
#status, err = conexion.set_mision(dato_obj)
status, err = conexion.set_resutados(image,dato_obj)
resultados = conexion.get_resultados()
if not status: print(err)
print(resultados)
cv2.imshow('Imagen',resultados[1])
cv2.waitKey()
time.sleep(3)


status, err = conexion.desconectar()
if not status: print(err)